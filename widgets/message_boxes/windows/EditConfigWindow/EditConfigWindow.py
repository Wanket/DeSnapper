from PyQt5.QtWidgets import QDialog
from dbus import DBusException

from snapper.SnapperConnection import SnapperConnection
from snapper.types.Config import Config
from widgets.message_boxes.DBusErrorMessageBox import DBusErrorMessageBox
from widgets.message_boxes.BtrfsEnvironmentErrorMessageBox import BtrfsEnvironmentErrorMessageBox
from widgets.message_boxes.windows.EditConfigWindow.Ui_EditConfigWindow import Ui_EditConfigWindow


class EditConfigWindow(QDialog):
    def __init__(self, connection: SnapperConnection, config: Config):
        super().__init__()

        self.__ui = Ui_EditConfigWindow()
        self.__ui.setupUi(self)

        self.__conn = connection
        self.__config = config

        self.__setup_ui()

        self.__setup_listeners()

    def __setup_ui(self) -> None:
        data = self.__config.attrs

        self.__ui.baseInfoLabel.setText(
            f"Editing config {self.__config.name} ({data.get('FSTYPE', '')} {data.get('SUBVOLUME', '')})")

        if data.get("FSTYPE", "") == "btrfs":
            try:
                self.__ui.configSettingsWidget.setup_qgroups(data.get("SUBVOLUME", ""))
            except EnvironmentError as e:
                BtrfsEnvironmentErrorMessageBox(e).exec()

        self.__ui.configSettingsWidget.fill_from_dict(data)

    def __setup_listeners(self) -> None:
        self.__ui.editPushButton.pressed.connect(self.__on_click_edit_push_button)

    def __on_click_edit_push_button(self) -> None:
        try:
            self.__conn.set_config(self.__config.name, self.__ui.configSettingsWidget.get_data())

            self.close()
        except DBusException as e:
            DBusErrorMessageBox(e).exec()
