from datetime import datetime
from enum import Enum
from pwd import getpwuid
from typing import Dict, Tuple

from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem

from snapper.types.Cleanup import Cleanup


class Snapshot:
    def __init__(self, raw_object):
        self.number: int = raw_object[0]
        self.type = Snapshot.Types(raw_object[1])
        self.pre_number: int = raw_object[2]
        self.date_time: int = raw_object[3]
        self.user_id: int = raw_object[4]
        self.description: str = raw_object[5]
        self.cleanup: Cleanup = Cleanup.from_str(raw_object[6])
        self.user_data: Dict[str, str] = raw_object[7]

    class Types(Enum):
        Single = 0
        Pre = 1
        Post = 2

    def to_tree_widget_item_array(self) -> Tuple[str, str, str, str, str, str, str]:
        number = str(self.number)
        snapshot_type = self.type.name
        pre_number = str(self.pre_number) if self.pre_number != 0 else ""
        date_time = str(datetime.fromtimestamp(self.date_time)) if self.date_time != -1 else ""

        try:
            user_id = getpwuid(self.user_id).pw_name
        except KeyError:
            user_id = "$Unknown"

        cleanup = str(self.cleanup)

        return number, snapshot_type, pre_number, date_time, user_id, cleanup, self.description

    def fill_user_data_table(self, user_data_table_widget: QTableWidget) -> None:
        user_data_table_widget.setRowCount(0)

        for key, value in self.user_data.items():
            index = user_data_table_widget.rowCount()

            user_data_table_widget.insertRow(index)

            user_data_table_widget.setItem(index, 0, QTableWidgetItem(key))
            user_data_table_widget.setItem(index, 1, QTableWidgetItem(value))

    @staticmethod
    def user_data_from_table(user_data_table_widget: QTableWidget) -> Dict[str, str]:
        user_data = dict()
        for i in range(user_data_table_widget.rowCount()):
            key_item = user_data_table_widget.item(i, 0)
            value_item = user_data_table_widget.item(i, 1)

            if key_item is not None:
                user_data[key_item.text()] = value_item.text() if value_item is not None else str()

        return user_data
