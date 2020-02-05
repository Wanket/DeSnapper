from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog
from dbus import DBusException

from snapper.SnapperConnection import SnapperConnection
from snapper.types.Cleanup import Cleanup
from snapper.types.Config import Config
from qt_snapper.types.Snapshot import Snapshot
from widgets.message_boxes.DBusErrorMessageBox import DBusErrorMessageBox
from widgets.windows.CreateSnapshotWindow.Ui_CreateSnapshotWindow import Ui_CreateSnapshotWindow


class CreateSnapshotWindow(QDialog):
    def __init__(self, connection: SnapperConnection, current_config: Config):
        super().__init__()

        self.__ui = Ui_CreateSnapshotWindow()
        self.__ui.setupUi(self)

        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)

        self.__connection = connection
        self.__current_config = current_config
        self.__list_snapshots = self.__connection.list_snapshots(self.__current_config.name)

        self.__setup_based_on_combo_box()

        self.__setup_listeners()

    def __setup_listeners(self) -> None:
        self.__ui.snapshotTypeComboBox.currentIndexChanged.connect(self.__on_snapshot_type_combo_box_value_changed)

        self.__ui.addPushButton.clicked.connect(self.__on_add_push_button_click)
        self.__ui.removePushButton.clicked.connect(self.__on_remove_push_button_click)

        self.__ui.createPushButton.clicked.connect(self.__on_create_push_button_click)

    def __setup_based_on_combo_box(self) -> None:
        self.__on_snapshot_type_combo_box_value_changed(0)

    def __on_create_push_button_click(self) -> None:
        try:
            snapshot_type = Snapshot.Types(self.__ui.snapshotTypeComboBox.currentIndex())

            config_name = self.__current_config.name
            description = self.__ui.descriptionLineEdit.text()
            cleanup = str(Cleanup(self.__ui.cleanupTypeComboBox.currentIndex()))

            user_data = Snapshot.user_data_from_table(self.__ui.userDataTableWidget)

            if snapshot_type == Snapshot.Types.Pre:
                self.__connection.create_pre_snapshot(config_name, description, cleanup, user_data)
            else:
                try:
                    parent_number = int(self.__ui.basedOnComboBox.currentText())
                except ValueError:
                    parent_number = 0

                if snapshot_type == Snapshot.Types.Post:
                    self.__connection.create_post_snapshot(config_name, parent_number, description, cleanup, user_data)
                else:
                    read_only = self.__ui.readOnlyCheckBox.isChecked()

                    self.__connection.create_single_snapshot_v2(config_name, parent_number, read_only, description,
                                                                cleanup, user_data)

            self.close()
        except DBusException as e:
            DBusErrorMessageBox(e).exec()

    def __on_add_push_button_click(self) -> None:
        self.__ui.userDataTableWidget.insertRow(self.__ui.userDataTableWidget.rowCount())

    def __on_remove_push_button_click(self) -> None:
        row_count = self.__ui.userDataTableWidget.rowCount()

        if row_count != 0:
            self.__ui.userDataTableWidget.removeRow(row_count - 1)

    def __on_snapshot_type_combo_box_value_changed(self, index: int) -> None:
        self.__ui.basedOnComboBox.clear()

        index = Snapshot.Types(index)

        is_single = index == Snapshot.Types.Single

        if not is_single:
            self.__ui.readOnlyCheckBox.setChecked(False)

        self.__ui.readOnlyCheckBox.setEnabled(is_single)

        self.__ui.basedOnComboBox.addItems([str(snapshot.number) for snapshot in self.__list_snapshots if
                                            index != Snapshot.Types.Post or snapshot.type == Snapshot.Types.Pre])

        if index != Snapshot.Types.Post:
            self.__ui.basedOnComboBox.setItemText(0, "0 (Current state)")
