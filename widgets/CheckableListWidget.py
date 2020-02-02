import typing

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QListWidget, QListWidgetItem


class CheckableListWidget(QListWidget):

    @typing.overload
    def addItem(self, aitem: QListWidgetItem) -> None: ...

    @typing.overload
    def addItem(self, label: str) -> None: ...

    def addItem(self, item) -> None:
        if isinstance(item, str):
            item = QListWidgetItem(item, self)

        item.setCheckState(Qt.Unchecked)

        super().addItem(item)
