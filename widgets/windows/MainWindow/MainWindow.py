from typing import Dict

from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QMainWindow, QTreeWidgetItem, QListWidgetItem, QAbstractItemView, QMenu

from snapper.SnapperConnection import SnapperConnection
from snapper.types.Config import Config
from snapper.types.Snapshot import Snapshot
from widgets.menus.ConfigMenu import ConfigMenu
from widgets.menus.SnapshotMenu import SnapshotMenu
from widgets.windows.MainWindow.Ui_MainWindow import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.__ui = Ui_MainWindow()
        self.__ui.setupUi(self)

        self.__snapper_connection = SnapperConnection()

        self.__configs: Dict[SnapperConnection.ConfigName, Config]
        self.__current_config_snapshots: Dict[SnapperConnection.SnapshotNumber, Snapshot]

        self.__configs = self.__get_configs()

        self.__setup_ui()

        self.__setup_listeners()

    def __get_configs(self) -> Dict[str, Config]:
        return {config.name: config for config in self.__snapper_connection.list_configs()}

    def __setup_ui(self) -> None:
        for config_name in self.__configs.keys():
            self.__ui.configsListWidget.addItem(QListWidgetItem(config_name))

    def __setup_listeners(self) -> None:
        self.__ui.configsListWidget.itemSelectionChanged.connect(self.__on_configs_list_changed)
        self.__ui.snapshotsTreeWidget.customContextMenuRequested.connect(
            self.__on_snapshots_tree_widget_context_menu_requested)
        self.__ui.configsListWidget.customContextMenuRequested.connect(
            self.__on_configs_list_widget_context_menu_requested)

    def __on_configs_list_changed(self):
        config_name = self.__ui.configsListWidget.currentItem().text()

        self.__current_config_snapshots = self.__get_snapshots(config_name)
        self.__setup_snapshots_view(config_name)

    def __get_snapshots(self, config_name: str) -> Dict[int, Snapshot]:
        return {snapshot.number: snapshot for snapshot in self.__snapper_connection.list_snapshots(config_name)}

    def __setup_snapshots_view(self, config_name: str):
        self.__ui.snapshotsTreeWidget.clear()

        top_level_item = QTreeWidgetItem([config_name])

        for snapshot in self.__current_config_snapshots.values():
            top_level_item.addChild(QTreeWidgetItem(snapshot.to_tree_widget_item_array()))

        self.__ui.snapshotsTreeWidget.addTopLevelItem(top_level_item)

        top_level_item.setFirstColumnSpanned(True)
        top_level_item.setExpanded(True)

    def __on_snapshots_tree_widget_context_menu_requested(self, pos: QPoint):
        items = self.__check_and_repair_items_focus(pos, self.__ui.snapshotsTreeWidget)

        snapshots = list()
        for item in items:
            if item is not None and item != self.__ui.snapshotsTreeWidget.topLevelItem(0):
                snapshots.append(self.__current_config_snapshots[int(item.text(0))])

        menu = SnapshotMenu(self, snapshots)
        menu.exec(QCursor.pos())

    def __on_configs_list_widget_context_menu_requested(self, pos: QPoint):
        items = self.__check_and_repair_items_focus(pos, self.__ui.configsListWidget)

        menu = ConfigMenu(self, [self.__configs[item.text()] for item in items])
        menu.exec(QCursor.pos())

    @staticmethod
    def __check_and_repair_items_focus(pos, widget: QAbstractItemView):
        items = widget.selectedItems()

        if widget.itemAt(pos) is None and len(items) != 0:
            widget.clearSelection()

            items = list()
        return items

    # def __on_create_config(self):
