from PyQt5.QtWidgets import QDialog

from snapper.SnapperConnection import SnapperConnection
from snapper.types.Config import Config
from widgets.windows.EditConfigWindow.Ui_EditConfigWindow import Ui_EditConfigWindow


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
            self.__ui.configSettingsWidget.setup_qgroups(data.get("SUBVOLUME", ""))

        self.__ui.configSettingsWidget.fill_from_dict(data)

    def __setup_listeners(self) -> None:
        self.__ui.editPushButton.pressed.connect(self.__on_click_edit_push_button)

    def __on_click_edit_push_button(self) -> None:
        self.__conn.set_config(self.__config.name, self.__ui.configSettingsWidget.get_data())

        self.close()
