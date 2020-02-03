from os import listdir
from os.path import isfile, join
from re import compile
from typing import NewType, Dict

from PyQt5.QtCore import QRegularExpression
from PyQt5.QtGui import QRegularExpressionValidator
from PyQt5.QtWidgets import QDialog, QMessageBox

from snapper.SnapperConnection import SnapperConnection
from widgets.windows.CreateConfigWindow.Ui_CreateConfigWindow import Ui_CreateConfigWindow

FileSystemPath = NewType("FileSystemPath", str)
FileSystemType = NewType("FileSystemType", str)


class CreateConfigWindow(QDialog):
    __lvm_regexp = compile("^lvm\\(([_a-z0-9]+)\\)$")

    __config_name_validator = QRegularExpressionValidator(QRegularExpression("[^, \t]+"))

    def __init__(self, connection: SnapperConnection):
        super().__init__()

        self.__ui = Ui_CreateConfigWindow()
        self.__ui.setupUi(self)

        self.__conn = connection

        self.__filesystems = self.__get_filesystems()

        self.__setup_ui()

        self.__setup_listeners()

    def exec(self) -> int:
        if len(self.__filesystems) == 0:
            message_box = QMessageBox(text="No available volumes to create config")
            message_box.setWindowTitle("Create config")

            return message_box.exec()

        return super().exec()

    def __setup_ui(self) -> None:
        self.__ui.volumeComboBox.addItems(self.__filesystems.keys())
        self.__ui.configSettingsWidget.fill_from_dict(dict())

        self.__ui.configNameLineEdit.setValidator(CreateConfigWindow.__config_name_validator)

        self.__setup_templates()

    def __setup_listeners(self) -> None:
        self.__ui.volumeComboBox.currentTextChanged.connect(self.__on_change_mount_point)

        self.__ui.createPushButton.clicked.connect(self.__on_click_create_push_button)

    def __setup_templates(self) -> None:
        self.__ui.templateComboBox.addItems([file_name for file_name in listdir("/etc/snapper/config-templates/") if
                                             isfile(join("/etc/snapper/config-templates/", file_name))])

    def __on_change_mount_point(self, path: str) -> None:
        self.__ui.configSettingsWidget.is_enable_btrfs = self.__filesystems[path] == "btrfs"

        if self.__ui.configSettingsWidget.is_enable_btrfs:
            self.__ui.configSettingsWidget.setup_qgroups(path)

    def __get_filesystems(self) -> Dict[FileSystemType, FileSystemPath]:
        result = dict()

        with open("/etc/mtab", "r") as file:
            for line in file.readlines():
                mount_item = line.split()

                fs_type = mount_item[2]

                if fs_type == "ext4dev":
                    fs_type = "ext4"

                if fs_type == "btrfs" or fs_type == "ext4" or CreateConfigWindow.__lvm_regexp.match(fs_type):
                    result[mount_item[1]] = fs_type

        for config in self.__conn.list_configs():
            if config.path in result:
                result.pop(config.path)

        return result

    def __on_click_create_push_button(self):
        sub_volume = self.__ui.volumeComboBox.currentText()
        template_name = self.__ui.templateComboBox.currentText() if self.__ui.templateGroupBox.isChecked() else ""
        config_name = self.__ui.configNameLineEdit.text()

        self.__conn.create_config(config_name, sub_volume, self.__filesystems[sub_volume], template_name)

        print(template_name)

        if len(template_name) == 0:
            self.__conn.set_config(config_name, self.__ui.configSettingsWidget.get_data())

        self.close()
