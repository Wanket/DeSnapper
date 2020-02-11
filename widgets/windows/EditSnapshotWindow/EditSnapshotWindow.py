from copy import deepcopy

from PyQt5.QtWidgets import QDialog
from dbus import DBusException

from snapper.SnapperConnection import SnapperConnection
from snapper.types.Cleanup import Cleanup
from snapper.types.Config import Config
from qt_snapper.types.Snapshot import Snapshot
from widgets.message_boxes.DBusErrorMessageBox import DBusErrorMessageBox
from widgets.windows.EditSnapshotWindow.Ui_EditSnapshotWindow import Ui_EditSnapshotWindow


class EditSnapshotWindow(QDialog):
    def __init__(self, connection: SnapperConnection, current_config: Config, snapshot: Snapshot):
        super().__init__()

        self.__ui = Ui_EditSnapshotWindow()
        self.__ui.setupUi(self)

        self.__connection = connection
        self.__config = current_config
        self.__snapshot = deepcopy(snapshot)

        self.__ui.cleanupTypeComboBox.setCurrentIndex(snapshot.cleanup)
        self.__ui.descriptionLineEdit.setText(self.__snapshot.description)
        self.__snapshot.fill_user_data_table(self.__ui.userDataTableWidget)

        self.__setup_listeners()

    def __setup_listeners(self) -> None:
        self.__ui.editPushButton.clicked.connect(self.__on_edit_push_button_clicked)

    def __on_edit_push_button_clicked(self) -> None:
        self.__snapshot.description = self.__ui.descriptionLineEdit.text()
        self.__snapshot.cleanup = Cleanup(self.__ui.cleanupTypeComboBox.currentIndex())
        self.__snapshot.user_data = Snapshot.user_data_from_table(self.__ui.userDataTableWidget)

        try:
            self.__connection.set_snapshot(self.__config.name, self.__snapshot)

            self.close()
        except DBusException as e:
            DBusErrorMessageBox(e).exec()
