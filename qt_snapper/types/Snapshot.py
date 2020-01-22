from typing import Dict

from PyQt5.QtWidgets import QTableWidgetItem, QTableWidget

from snapper.types.Snapshot import Snapshot as Snap


class Snapshot(Snap):
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
