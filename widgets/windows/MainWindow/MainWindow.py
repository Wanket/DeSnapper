from os import access, R_OK
from os.path import isfile
from subprocess import Popen, PIPE
from typing import Dict, List, Optional, TypeVar, Set

from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QMainWindow, QTreeWidgetItem, QListWidgetItem, QMessageBox, QTreeWidget, QListWidget
from _dbus_glib_bindings import DBusGMainLoop
from dbus import DBusException

from qt_snapper.types.Snapshot import Snapshot
from snapper.SnapperConnection import SnapperConnection
from snapper.types.Config import Config
from systemd.SystemdConnection import SystemdConnection
from utils.ConfigFile import ConfigFile
from utils.UserInfo import UserInfo
from widgets.menus.ConfigMenu import ConfigMenu
from widgets.menus.SnapshotMenu import SnapshotMenu
from widgets.message_boxes.ConfirmMessageBox import ConfirmMessageBox
from widgets.message_boxes.DBusErrorMessageBox import DBusErrorMessageBox
from widgets.message_boxes.ErrorMessageBox import ErrorMessageBox
from widgets.windows.CreateConfigWindow.CreateConfigWindow import CreateConfigWindow
from widgets.windows.CreateSnapshotWindow.CreateSnapshotWindow import CreateSnapshotWindow
from widgets.windows.DiffWindow.DiffWindow import DiffWindow
from widgets.windows.EditConfigWindow.EditConfigWindow import EditConfigWindow
from widgets.windows.EditSnapshotWindow.EditSnapshotWindow import EditSnapshotWindow
from widgets.windows.MainWindow.Ui_MainWindow import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.__ui = Ui_MainWindow()
        self.__ui.setupUi(self)

        DBusGMainLoop(set_as_default=True)

        self.__snapper_connection = SnapperConnection(Snapshot)

        self.__systemd_connection = SystemdConnection()

        self.__configs: Dict[SnapperConnection.ConfigName, Config]
        self.__current_config_snapshots: Dict[SnapperConnection.SnapshotNumber, Snapshot]

        self.__current_config: Optional[Config] = None

        self.__configs = self.__get_configs()

        self.__mounted_snapshots: Dict[SnapperConnection.ConfigName, Set[SnapperConnection.SnapshotNumber]] = dict()

        self.__apt_config: Optional[ConfigFile] = self.__get_config("/etc/default/snapper") \
            if UserInfo().is_root() else None

        self.__setup_ui()

        self.__setup_listeners()

    def __del__(self):
        for config_name, snapshot_numbers in self.__mounted_snapshots.items():
            for snapshot_number in snapshot_numbers:
                try:
                    self.__snapper_connection.unmount_snapshot(config_name, snapshot_number, True)
                except DBusException:
                    pass

    # region Startup functions

    def __get_configs(self) -> Dict[str, Config]:
        return {config.name: config for config in self.__snapper_connection.list_configs()}

    def __setup_ui(self) -> None:
        for config_name in self.__configs.keys():
            self.__ui.configsListWidget.addItem(QListWidgetItem(config_name))

        if self.__apt_config is not None:
            try:
                self.__ui.actionEnable_auto_apt.setChecked(
                    self.__apt_config["DISABLE_APT_SNAPSHOT"] == "\"no\"")
            except KeyError:
                pass
        else:
            self.__ui.actionEnable_auto_apt.setEnabled(False)

        is_root = UserInfo().is_root()

        self.__ui.actionEnable_create_snapshot_on_boot.setEnabled(is_root)
        self.__ui.actionEnable_auto_Timeline_cleanup.setEnabled(is_root)
        self.__ui.actionEnable_auto_daily_cleanup.setEnabled(is_root)

        self.__ui.actionEnable_create_snapshot_on_boot.setChecked(
            self.__systemd_connection.get_unit_file_state(MainWindow.snapper_boot_unit[0]))
        self.__ui.actionEnable_auto_Timeline_cleanup.setChecked(
            self.__systemd_connection.get_unit_file_state(MainWindow.snapper_timeline_unit[0]))
        self.__ui.actionEnable_auto_daily_cleanup.setChecked(
            self.__systemd_connection.get_unit_file_state(MainWindow.snapper_cleanup_unit[0]))

    def __setup_listeners(self) -> None:
        self.__ui.configsListWidget.itemSelectionChanged.connect(self.__on_configs_list_selected_item_changed)
        self.__ui.snapshotsTreeWidget.customContextMenuRequested.connect(
            self.__on_snapshots_tree_widget_context_menu_requested)
        self.__ui.configsListWidget.customContextMenuRequested.connect(
            self.__on_configs_list_widget_context_menu_requested)

        self.__ui.snapshotsTreeWidget.itemClicked.connect(self.__on_snapshot_tree_widget_item_clicked)

        self.__snapper_connection.snapshot_created += self.__on_snapshot_created
        self.__snapper_connection.snapshot_modified += self.__on_snapshot_edited
        self.__snapper_connection.snapshots_deleted += self.__on_snapshots_deleted

        self.__snapper_connection.config_created += self.__on_config_created
        self.__snapper_connection.config_modified += self.__on_config_edited
        self.__snapper_connection.config_deleted += self.__on_config_deleted

        self.__ui.actionEnable_auto_apt.changed.connect(self.__on_enable_auto_apt_clicked)
        self.__ui.actionCompare_snapshots.triggered.connect(self.__on_compare_snapshots_clicked)

        self.__ui.actionNumberCleanup.triggered.connect(self.__on_number_cleanup_clicked)
        self.__ui.actionTimelineCleanup.triggered.connect(self.__on_number_timeline_clicked)
        self.__ui.actionEmpty_pre_postCleanup.triggered.connect(self.__on_number_empty_pre_post_clicked)

        self.__ui.actionEnable_create_snapshot_on_boot.changed.connect(self.__on_enable_create_snapshot_on_boot)
        self.__ui.actionEnable_auto_Timeline_cleanup.changed.connect(self.__on_enable_auto_timeline_cleanup)
        self.__ui.actionEnable_auto_daily_cleanup.changed.connect(self.__on_enable_auto_daily_cleanup)

    @staticmethod
    def __get_config(path: str) -> Optional[ConfigFile]:
        return ConfigFile(path) if isfile(path) else None

    # endregion

    # region Menu bar functions

    def __on_enable_auto_apt_clicked(self) -> None:
        self.__apt_config["DISABLE_APT_SNAPSHOT"] = "\"yes\"" \
            if not self.__ui.actionEnable_auto_apt.isChecked() else "\"no\""

        self.__apt_config.sync_to_file()

    # region Cleanup functions

    def __on_number_cleanup_clicked(self):
        MainWindow.__cleanup(self.__current_config.name, "number")

    def __on_number_timeline_clicked(self):
        MainWindow.__cleanup(self.__current_config.name, "timeline")

    def __on_number_empty_pre_post_clicked(self):
        MainWindow.__cleanup(self.__current_config.name, "empty-pre-post")

    @staticmethod
    def __cleanup(config_name: str, cleanup_name: str):
        snapper_proc = Popen(["snapper", "-c", config_name, "cleanup", cleanup_name], stderr=PIPE)
        snapper_proc.wait()

        message = QMessageBox(text=f"Cleanup algorithm {cleanup_name} has finished" if snapper_proc.returncode == 0
                              else f"Error: {snapper_proc.stderr.read().decode('utf-8')}")
        message.setWindowTitle("Cleanup")

        message.exec()

    # endregion

    # region Compare functions

    def __on_compare_snapshots_clicked(self):
        DiffWindow(self.__current_config.name, self.__current_config_snapshots, self.__snapper_connection).exec()

    # endregion

    # region SystemD functions

    snapper_boot_unit = ["snapper-boot.timer"]

    snapper_timeline_unit = ["snapper-timeline.timer"]

    snapper_cleanup_unit = ["snapper-cleanup.timer"]

    def __on_enable_create_snapshot_on_boot(self) -> None:
        self.__change_unit_state(self.__ui.actionEnable_create_snapshot_on_boot.isChecked(),
                                 MainWindow.snapper_boot_unit)

    def __on_enable_auto_timeline_cleanup(self) -> None:
        self.__change_unit_state(self.__ui.actionEnable_auto_Timeline_cleanup.isChecked(),
                                 MainWindow.snapper_timeline_unit)

    def __on_enable_auto_daily_cleanup(self) -> None:
        self.__change_unit_state(self.__ui.actionEnable_auto_daily_cleanup.isChecked(),
                                 MainWindow.snapper_cleanup_unit)

    def __change_unit_state(self, is_enable: bool, unit: List[str]) -> None:
        if is_enable:
            self.__systemd_connection.enable_unit_files(unit)
        else:
            self.__systemd_connection.disable_unit_files(unit)

    # endregion

    # endregion

    # region Configs/Snapshots view functions

    def __on_configs_list_selected_item_changed(self) -> None:
        config_name = self.__ui.configsListWidget.currentItem().text()

        config = self.__configs[config_name]

        if self.__current_config is not None and config_name == self.__current_config.name or \
                not UserInfo().check_permissions(config):
            return

        self.__current_config_snapshots = self.__get_snapshots(config_name)
        self.__setup_snapshots_view(config_name)

        self.__current_config = config

        self.__snapper_connection.lock_config(config.name)

        self.__ui.menuRun_cleanup_algorithm.setEnabled(True)
        self.__ui.actionCompare_snapshots.setEnabled(True)

    def __get_snapshots(self, config_name: str) -> Dict[int, Snapshot]:
        return {snapshot.number: snapshot for snapshot in self.__snapper_connection.list_snapshots(config_name)}

    def __setup_snapshots_view(self, config_name: str) -> None:
        self.__ui.snapshotsTreeWidget.clear()

        top_level_item = QTreeWidgetItem([config_name])

        top_level_item.addChildren(QTreeWidgetItem(snapshot.to_tree_widget_item_array()) for snapshot in
                                   self.__current_config_snapshots.values())

        self.__ui.snapshotsTreeWidget.addTopLevelItem(top_level_item)

        top_level_item.setFirstColumnSpanned(True)
        top_level_item.setExpanded(True)

    def __on_snapshot_tree_widget_item_clicked(self, item: QTreeWidgetItem, index: int) -> None:
        if index == 0:
            return

        snapshot = self.__current_config_snapshots[int(item.text(0))]

        snapshot.fill_user_data_table(self.__ui.userDataTableWidget)

        self.__ui.userDataDockWidget.setWindowTitle(f"User data of snapshot number {snapshot.number}")

    def __clean_user_data_table(self) -> None:
        self.__ui.userDataTableWidget.setRowCount(0)

        self.__ui.userDataDockWidget.setWindowTitle("User data")

    # endregion

    ItemView = TypeVar("ItemView", QTreeWidget, QListWidget)

    @staticmethod
    def __check_and_repair_items_focus(pos, widget: ItemView) -> List[ItemView]:
        items = widget.selectedItems()

        if widget.itemAt(pos) is None and len(items) != 0:
            widget.clearSelection()

            items = list()

        return items

    # region Snapshot context menu functions and callbacks

    def __on_snapshots_tree_widget_context_menu_requested(self, pos: QPoint) -> None:
        if self.__current_config is None:
            return

        items = self.__check_and_repair_items_focus(pos, self.__ui.snapshotsTreeWidget)

        snapshots = [self.__current_config_snapshots[int(item.text(0))] for item in items if
                     item is not None and item != self.__ui.snapshotsTreeWidget.topLevelItem(0)]

        menu = SnapshotMenu(self, snapshots)

        menu.action_create_snapshot.connect(self.__on_create_snapshot)
        menu.action_create_pre_and_post_snapshots_running_terminal_in_between.connect(
            self.__on_open_terminal_and_create_pre_post_clicked)
        menu.action_open_snapshot_folder.connect(lambda: self.__on_open_snapshot_folder(snapshots[0]))
        menu.action_edit_snapshot.connect(lambda: self.__on_edit_snapshot(snapshots[0]))
        menu.action_delete_snapshot.connect(lambda: self.__on_delete_snapshots(snapshots))

        menu.exec(QCursor.pos())

    def __add_snapshot_to_current_snapshots(self, config_name, snapshot_number) -> Snapshot:
        snapshot = self.__snapper_connection.get_snapshot(config_name, snapshot_number)

        self.__current_config_snapshots[snapshot_number] = snapshot

        return snapshot

    # region Create snapshot functions

    def __on_create_snapshot(self) -> None:
        CreateSnapshotWindow(self.__snapper_connection, self.__current_config).exec()

    def __on_snapshot_created(self, config_name: str, snapshot_number: int) -> None:
        if self.__current_config is not None and self.__current_config.name == config_name:
            top_level_item = self.__ui.snapshotsTreeWidget.topLevelItem(0)

            snapshot = self.__add_snapshot_to_current_snapshots(config_name, snapshot_number)

            top_level_item.addChild(QTreeWidgetItem(snapshot.to_tree_widget_item_array()))

    # endregion

    # region Open terminal and create pre-post functions

    def __on_open_terminal_and_create_pre_post_clicked(self):
        try:
            snapshot_number = self.__snapper_connection.create_pre_snapshot(self.__current_config.name,
                                                                            "DeSnapper terminal pre", "", {})

            Popen("x-terminal-emulator").wait()

            self.__snapper_connection.create_post_snapshot(self.__current_config.name, snapshot_number,
                                                           "DeSnapper terminal post", "", {})
        except DBusException as e:
            DBusErrorMessageBox(e).exec()

    # endregion

    # region Open snapshot folder functions

    def __on_open_snapshot_folder(self, snapshot: Snapshot) -> None:
        try:
            config_name = self.__current_config.name
            snapshot_number = snapshot.number

            if config_name not in self.__mounted_snapshots:
                self.__mounted_snapshots[config_name] = set()

            mounted_snapshots_set = self.__mounted_snapshots[config_name]

            if snapshot not in mounted_snapshots_set and snapshot.number != 0:
                mount_point = self.__snapper_connection.mount_snapshot(config_name, snapshot_number, True)

                mounted_snapshots_set.add(snapshot_number)
            else:
                mount_point = self.__snapper_connection.get_mount_point(config_name, snapshot_number)

            if not access(mount_point, R_OK):
                ErrorMessageBox(f"You have no permissions to access snapshot folder number {snapshot_number}. "
                                f"You can use ACL for get permissions").exec()

                return

            Popen(["xdg-open", mount_point])
        except DBusException as e:
            DBusErrorMessageBox(e).exec()

    # endregion

    # region Edit snapshot functions

    def __on_edit_snapshot(self, snapshot: Snapshot) -> None:
        EditSnapshotWindow(self.__snapper_connection, self.__current_config, snapshot).exec()

    def __on_snapshot_edited(self, config_name: str, snapshot_number: int) -> None:
        if self.__current_config is not None and self.__current_config.name == config_name:
            top_level_item = self.__ui.snapshotsTreeWidget.topLevelItem(0)

            snapshot = self.__add_snapshot_to_current_snapshots(config_name, snapshot_number)

            for i in range(top_level_item.childCount()):
                item = top_level_item.child(i)

                if int(item.text(0)) == snapshot.number:
                    top_level_item.removeChild(item)
                    top_level_item.insertChild(i, QTreeWidgetItem(snapshot.to_tree_widget_item_array()))

                    self.__clean_user_data_table()

                    break

    # endregion

    # region Delete snapshots functions

    def __on_delete_snapshots(self, snapshots: List[Snapshot]) -> None:
        if ConfirmMessageBox(self, "Delete snapshots",
                             f"Are you sure you want to delete {len(snapshots)} "
                             f"{'snapshot' if len(snapshots) == 1 else 'snapshots'}?").exec() == QMessageBox.Ok:
            try:
                self.__snapper_connection.delete_snapshots(self.__current_config.name,
                                                           [snapshot.number for snapshot in snapshots])
            except DBusException as e:
                DBusErrorMessageBox(e).exec()

    def __on_snapshots_deleted(self, config_name: str, snapshot_numbers: List[int]) -> None:
        if config_name in self.__mounted_snapshots:
            snapshot_numbers_set = self.__mounted_snapshots[config_name]

            for snapshot_number in snapshot_numbers:
                snapshot_numbers_set.discard(snapshot_number)

        if self.__current_config is not None and self.__current_config.name == config_name:
            top_level_item = self.__ui.snapshotsTreeWidget.topLevelItem(0)

            i = 0
            while i < top_level_item.childCount():
                item = top_level_item.child(i)

                if int(item.text(0)) in snapshot_numbers:
                    top_level_item.removeChild(item)
                else:
                    i += 1

            for snapshot_number in snapshot_numbers:
                self.__current_config_snapshots.pop(snapshot_number)

            self.__clean_user_data_table()

    # endregion
    # endregion

    # region Configs context menu functions and callbacks

    def __on_configs_list_widget_context_menu_requested(self, pos: QPoint) -> None:
        if not UserInfo().is_root():
            return

        item = self.__ui.configsListWidget.itemAt(pos)

        config = self.__configs[item.text()] if item is not None else None

        menu = ConfigMenu(self, config)

        menu.action_create_config.connect(self.__on_create_config)
        menu.action_delete_config.connect(lambda: self.__on_delete_config(config))
        menu.action_edit_config.connect(lambda: self.__on_edit_config(config))

        menu.exec(QCursor.pos())

    # region Delete configs functions

    def __on_delete_config(self, config: Config) -> None:
        if ConfirmMessageBox(self, "Delete config",
                             f"Are you sure you want to delete {config.name} config?").exec() == QMessageBox.Ok:
            try:
                self.__snapper_connection.delete_config(config.name)
            except DBusException as e:
                DBusErrorMessageBox(e).exec()

    def __on_config_deleted(self, config_name) -> None:
        if config_name in self.__mounted_snapshots:
            self.__mounted_snapshots.pop(config_name)

        if self.__current_config is not None and self.__current_config == config_name:
            self.__ui.snapshotsTreeWidget.clear()

            self.__snapper_connection.unlock_config(self.__current_config.name)

            self.__current_config = None

            self.__ui.menuRun_cleanup_algorithm.setDisabled(True)
            self.__ui.actionCompare_snapshots.setDisabled(True)

        for i in range(self.__ui.configsListWidget.count()):
            if self.__ui.configsListWidget.item(i).text() == config_name:
                self.__ui.configsListWidget.takeItem(i)

                break

        self.__configs.pop(config_name)

    # endregion

    # region Edit configs functions

    def __on_edit_config(self, config: Config) -> None:
        EditConfigWindow(self.__snapper_connection, config).exec()

    def __on_config_edited(self, config_name: str) -> None:
        self.__configs[config_name] = self.__snapper_connection.get_config(config_name)

    # endregion

    # region Create configs functions

    def __on_create_config(self) -> None:
        CreateConfigWindow(self.__snapper_connection).exec()

    def __on_config_created(self, config_name: str) -> None:
        self.__configs[config_name] = self.__snapper_connection.get_config(config_name)

        self.__ui.configsListWidget.addItem(config_name)

    # endregion
    # endregion
