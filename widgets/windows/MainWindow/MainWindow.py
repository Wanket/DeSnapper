from typing import Dict, List, Optional, TypeVar

from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QMainWindow, QTreeWidgetItem, QListWidgetItem, QMessageBox, \
    QTreeWidget, QListWidget, QTableWidgetItem

from snapper.SnapperConnection import SnapperConnection
from snapper.types import Snapshot
from snapper.types.Config import Config
from snapper.types.Snapshot import Snapshot
from widgets.ConfirmMessageBox import ConfirmMessageBox
from widgets.menus.ConfigMenu import ConfigMenu
from widgets.menus.SnapshotMenu import SnapshotMenu
from widgets.windows.CreateSnapshotWindow.CreateSnapshotWindow import CreateSnapshotWindow
from widgets.windows.MainWindow.Ui_MainWindow import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.__ui = Ui_MainWindow()
        self.__ui.setupUi(self)

        self.__snapper_connection = SnapperConnection()

        self.__configs: Dict[SnapperConnection.ConfigName, Config]
        self.__current_config_snapshots: Dict[SnapperConnection.SnapshotNumber, Snapshot]

        self.__current_config: Optional[Config] = None

        self.__configs = self.__get_configs()

        self.__setup_ui()

        self.__setup_listeners()

    # region Startup functions
    def __get_configs(self) -> Dict[str, Config]:
        return {config.name: config for config in self.__snapper_connection.list_configs()}

    def __setup_ui(self) -> None:
        for config_name in self.__configs.keys():
            self.__ui.configsListWidget.addItem(QListWidgetItem(config_name))

    def __setup_listeners(self) -> None:
        self.__ui.configsListWidget.itemSelectionChanged.connect(self.__on_configs_list_selected_item_changed)
        self.__ui.snapshotsTreeWidget.customContextMenuRequested.connect(
            self.__on_snapshots_tree_widget_context_menu_requested)
        self.__ui.configsListWidget.customContextMenuRequested.connect(
            self.__on_configs_list_widget_context_menu_requested)

        self.__ui.snapshotsTreeWidget.itemClicked.connect(self.__on_snapshot_tree_widget_item_clicked)

        self.__snapper_connection.snapshot_created += self.__on_snapshot_created
        self.__snapper_connection.snapshots_deleted += self.__on_snapshots_deleted

    # endregion

    # region Configs/Snapshots view functions
    def __on_configs_list_selected_item_changed(self) -> None:
        config_name = self.__ui.configsListWidget.currentItem().text()

        if self.__current_config is not None and config_name == self.__current_config.name:
            return

        self.__current_config_snapshots = self.__get_snapshots(config_name)
        self.__setup_snapshots_view(config_name)

        self.__current_config = self.__configs[config_name]

    def __get_snapshots(self, config_name: str) -> Dict[int, Snapshot]:
        return {snapshot.number: snapshot for snapshot in self.__snapper_connection.list_snapshots(config_name)}

    def __setup_snapshots_view(self, config_name: str) -> None:
        self.__ui.snapshotsTreeWidget.clear()

        top_level_item = QTreeWidgetItem([config_name])

        for snapshot in self.__current_config_snapshots.values():
            top_level_item.addChild(QTreeWidgetItem(snapshot.to_tree_widget_item_array()))

        self.__ui.snapshotsTreeWidget.addTopLevelItem(top_level_item)

        top_level_item.setFirstColumnSpanned(True)
        top_level_item.setExpanded(True)

    def __on_snapshot_tree_widget_item_clicked(self, item: QTreeWidgetItem, _: int):
        snapshot = self.__current_config_snapshots[int(item.text(0))]

        self.__ui.userDataTableWidget.setRowCount(0)

        for key, value in snapshot.user_data.items():
            index = self.__ui.userDataTableWidget.rowCount()

            self.__ui.userDataTableWidget.insertRow(index)

            self.__ui.userDataTableWidget.setItem(index, 0, QTableWidgetItem(key))
            self.__ui.userDataTableWidget.setItem(index, 1, QTableWidgetItem(value))

        self.__ui.userDataDockWidget.setWindowTitle(f"User data of snapshot number {snapshot.number}")

    # endregion

    ItemView = TypeVar("ItemView", QTreeWidget, QListWidget)

    @staticmethod
    def __check_and_repair_items_focus(pos, widget: ItemView) -> List[ItemView]:
        items = widget.selectedItems()

        if widget.itemAt(pos) is None and len(items) != 0:
            widget.clearSelection()

            items = list()
        return items

    # region Snapshot context menu functions
    def __on_snapshots_tree_widget_context_menu_requested(self, pos: QPoint) -> None:
        if self.__current_config is None:
            return

        items = self.__check_and_repair_items_focus(pos, self.__ui.snapshotsTreeWidget)

        snapshots = list()
        for item in items:
            if item is not None and item != self.__ui.snapshotsTreeWidget.topLevelItem(0):
                snapshots.append(self.__current_config_snapshots[int(item.text(0))])

        menu = SnapshotMenu(self, snapshots)

        menu.action_delete_snapshot.connect(lambda: self.__on_delete_snapshots(snapshots))
        menu.action_create_snapshot.connect(self.__on_create_snapshot)

        menu.exec(QCursor.pos())

    # region Create snapshot functions
    def __on_create_snapshot(self) -> None:
        window = CreateSnapshotWindow(self.__snapper_connection, self.__current_config)
        window.exec()

    def __on_snapshot_created(self, config_name: str, snapshot_number: int) -> None:
        if self.__current_config is not None and self.__current_config.name == config_name:
            top_level_item = self.__ui.snapshotsTreeWidget.topLevelItem(0)

            snapshot = self.__snapper_connection.get_snapshot(config_name, snapshot_number)

            self.__current_config_snapshots[snapshot_number] = snapshot

            top_level_item.addChild(QTreeWidgetItem(snapshot.to_tree_widget_item_array()))

    # endregion

    # region Delete functions
    def __on_delete_snapshots(self, snapshots: List[Snapshot]) -> None:
        message_box = ConfirmMessageBox(self,
                                        f"Are you sure you want to delete {len(snapshots)} "
                                        f"{'snapshot' if len(snapshots) == 1 else 'snapshots'}", )

        if message_box.exec() == QMessageBox.Ok:
            self.__snapper_connection.delete_snapshots(self.__current_config.name,
                                                       [snapshot.number for snapshot in snapshots])

    def __on_snapshots_deleted(self, config_name: str, snapshot_numbers: List[int]) -> None:
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

    # endregion
    # endregion

    # region Configs context menu functions
    def __on_configs_list_widget_context_menu_requested(self, pos: QPoint) -> None:
        items = self.__check_and_repair_items_focus(pos, self.__ui.configsListWidget)

        menu = ConfigMenu(self, [self.__configs[item.text()] for item in items])
        menu.exec(QCursor.pos())
    # endregion
