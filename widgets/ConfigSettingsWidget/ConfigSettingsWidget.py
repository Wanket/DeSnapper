from errno import ENOTTY
from grp import getgrall, struct_group
from os import strerror
from pwd import getpwall, struct_passwd
from typing import Optional, Dict, List

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QSizePolicy, QApplication, QListWidget

try:
    from DeSnapper_btrfs import get_qgroups
except ImportError:
    get_qgroups = None

from widgets.ConfigSettingsWidget.Ui_ConfigSettingsWidget import Ui_ConfigSettingsWidget


class ConfigSettingsWidget(QWidget):
    is_enable_btrfs = property()

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)

        self.__ui = Ui_ConfigSettingsWidget()

        self.__ui.setupUi(self)

        self.__setup_listeners()

        self.__update_sizes(0)

        self.__setup_ui()

    @is_enable_btrfs.getter
    def is_enable_btrfs(self):
        return self.__ui.btrfsTab.isEnabled()

    @is_enable_btrfs.setter
    def is_enable_btrfs(self, value):
        self.__ui.btrfsTab.setEnabled(value)

    def setup_qgroups(self, path: Optional[str]) -> None:
        if get_qgroups is not None:
            result = get_qgroups(path)

            if result[0] != 0 and result[0] != -ENOTTY:
                raise EnvironmentError(result[0], strerror(result[0]))

            self.__ui.qgroupComboBox.clear()
            self.__ui.qgroupComboBox.addItem("None")

            self.__ui.qgroupComboBox.addItems([f"{level}/{subvolume_id}" for level, subvolume_id in result[1]])

    def fill_from_dict(self, data: Dict[str, str]) -> None:
        if data.get("FSTYPE", "") == "btrfs":
            self.__ui.spaceLimitSpinBox.setValue(int(float(data.get("SPACE_LIMIT", "0.5")) * 100))

            if get_qgroups is not None:
                self.__ui.qgroupComboBox.setCurrentText(data.get("QGROUP", "None"))

        self.__enable_elements_in_list_widget(data.get("ALLOW_USERS", "").split(), self.__ui.allowUsersListWidget)
        self.__enable_elements_in_list_widget(data.get("ALLOW_GROUPS", "").split(), self.__ui.allowGroupsListWidget)
        self.__ui.syncAclCheckBox.setChecked(data.get("SYNC_ACL", "no") == "yes")
        self.__ui.backgruondComparisonCheckBox.setChecked(data.get("BACKGROUND_COMPARISON", "yes") == "yes")
        self.__ui.timelineCreateCheckBox.setChecked(data.get("TIMELINE_CREATE", "no") == "yes")

        self.__ui.numberCleanupGroupBox.setChecked(data.get("NUMBER_CLEANUP", "no") == "yes")
        self.__ui.numberMinAgeSpinBox.setValue(int(data.get("NUMBER_MIN_AGE", "1800")))
        self.__ui.numberLimitSpinBox.set_value_from_str(data.get("NUMBER_LIMIT", "50"))
        self.__ui.numberLimitImportantSpinBox.set_value_from_str(data.get("NUMBER_LIMIT_IMPORTANT", "10"))

        self.__ui.timelineCleanupGroupBox.setChecked(data.get("TIMELINE_CLEANUP", "no") == "yes")
        self.__ui.timelineMinAgeSpinBox.setValue(int(data.get("TIMELINE_MIN_AGE", "1800")))
        self.__ui.timelineLimitHourlySpinBox.set_value_from_str(data.get("TIMELINE_LIMIT_HOURLY", "10"))
        self.__ui.timelineLimitDailySpinBox.set_value_from_str(data.get("TIMELINE_LIMIT_DAILY", "10"))
        self.__ui.timelineLimitWeeklySpinBox.set_value_from_str(data.get("TIMELINE_LIMIT_WEEKLY", "0"))
        self.__ui.timelineLimitMonthlySpinBox.set_value_from_str(data.get("TIMELINE_LIMIT_MONTHLY", "10"))
        self.__ui.timelineLimitYearlySpinBox.set_value_from_str(data.get("TIMELINE_LIMIT_YEARLY", "10"))

        self.__ui.emptyPrePostClenupGroupBox.setChecked(data.get("EMPTY_PRE_POST_CLEANUP", "no") == "yes")
        self.__ui.emptyPrePostMinAgeSpinBox.setValue(int(data.get("EMPTY_PRE_POST_MIN_AGE", "1800")))

    def get_data(self) -> Dict[str, str]:
        return {
            "SPACE_LIMIT": str(self.__ui.spaceLimitSpinBox.value() / 100),
            "QGROUP": self.__ui.qgroupComboBox.currentText() if self.__ui.qgroupComboBox.currentIndex() != 0 else str(),

            "ALLOW_USERS": " ".join(self.__get_enabled_elements_in_list_widget(self.__ui.allowUsersListWidget)),
            "ALLOW_GROUPS": " ".join(self.__get_enabled_elements_in_list_widget(self.__ui.allowGroupsListWidget)),
            "SYNC_ACL": "yes" if self.__ui.syncAclCheckBox.isChecked() else "no",
            "BACKGROUND_COMPARISON": "yes" if self.__ui.backgruondComparisonCheckBox.isChecked() else "no",
            "TIMELINE_CREATE": "yes" if self.__ui.timelineCreateCheckBox.isChecked() else "no",

            "NUMBER_CLEANUP": "yes" if self.__ui.numberCleanupGroupBox.isChecked() else "no",
            "NUMBER_MIN_AGE": str(self.__ui.numberMinAgeSpinBox.value()),
            "NUMBER_LIMIT": str(self.__ui.numberLimitSpinBox),
            "NUMBER_LIMIT_IMPORTANT": str(self.__ui.numberLimitImportantSpinBox),

            "TIMELINE_CLEANUP": "yes" if self.__ui.timelineCleanupGroupBox.isChecked() else "no",
            "TIMELINE_MIN_AGE": str(self.__ui.timelineMinAgeSpinBox.value()),
            "TIMELINE_LIMIT_HOURLY": str(self.__ui.timelineLimitHourlySpinBox),
            "TIMELINE_LIMIT_DAILY": str(self.__ui.timelineLimitDailySpinBox),
            "TIMELINE_LIMIT_WEEKLY": str(self.__ui.timelineLimitWeeklySpinBox),
            "TIMELINE_LIMIT_MONTHLY": str(self.__ui.timelineLimitMonthlySpinBox),
            "TIMELINE_LIMIT_YEARLY": str(self.__ui.timelineLimitYearlySpinBox),

            "EMPTY_PRE_POST_CLEANUP": "yes" if self.__ui.emptyPrePostClenupGroupBox.isChecked() else "no",
            "EMPTY_PRE_POST_MIN_AGE": str(self.__ui.emptyPrePostMinAgeSpinBox.value())
        }

    def __setup_listeners(self) -> None:
        self.__ui.settingsTabWidget.currentChanged.connect(self.__update_sizes)

    def update_sizes(self) -> None:
        self.__update_sizes(self.__ui.settingsTabWidget.currentIndex())

    def __update_sizes(self, widget_index: int) -> None:
        for i in range(self.__ui.settingsTabWidget.count()):
            self.__ui.settingsTabWidget.widget(i).setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)

        self.__ui.settingsTabWidget.widget(widget_index).setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        QApplication.processEvents()

        self.adjustSize()

        if self.parent() is not None:
            self.parent().adjustSize()

    def __setup_ui(self) -> None:
        self.__setup_users_ui()
        self.__setup_groups_ui()
        self.__setup_qgruops_ui()

    def __setup_users_ui(self) -> None:
        user: struct_passwd
        for user in getpwall():
            self.__ui.allowUsersListWidget.addItem(user.pw_name)

    def __setup_groups_ui(self) -> None:
        group: struct_group
        for group in getgrall():
            self.__ui.allowGroupsListWidget.addItem(group.gr_name)

    def __setup_qgruops_ui(self) -> None:
        if get_qgroups is None:
            self.__ui.qgroupComboBox.setEnabled(False)

    @staticmethod
    def __enable_elements_in_list_widget(elements: List[str], list_widget: QListWidget) -> None:
        elements.sort()
        list_widget.sortItems()

        i = 0
        j = 0

        while i < len(elements) and j < list_widget.count():
            item = list_widget.item(j)

            if item.text() == elements[i]:
                item.setCheckState(Qt.Checked)
                i += 1
                j += 1
            elif item.text() < elements[i]:
                j += 1
            else:
                i += 1

    @staticmethod
    def __get_enabled_elements_in_list_widget(list_widget: QListWidget) -> List[str]:
        result = list()

        for i in range(list_widget.count()):
            item = list_widget.item(i)

            if item.checkState() == Qt.Checked:
                result.append(item.text())

        return result
