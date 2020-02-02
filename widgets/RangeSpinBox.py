from _testcapi import INT_MAX
from typing import Optional

from PyQt5.QtCore import QRegularExpression
from PyQt5.QtGui import QRegularExpressionValidator
from PyQt5.QtWidgets import QWidget, QAbstractSpinBox


class RangeSpinBox(QAbstractSpinBox):
    __validator = QRegularExpressionValidator(QRegularExpression("^[0-9]+|[0-9]+-[0-9]+"))

    left_value = property()
    right_value = property()

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)

        self.__left_value: Optional[int] = None
        self.__right_value: int = 0

        self.lineEdit().setValidator(RangeSpinBox.__validator)

        self.__update_values()

        self.__setup_listeners()

    def set_value_from_str(self, text) -> None:
        self.lineEdit().setText(text)

        self.__on_editing_finished()

    def __str__(self):
        return self.text()

    # @left_value.setter
    # def left_value(self, value: Optional[int]):
    #     self.__left_value = value
    #
    # @left_value.getter
    # def left_value(self) -> Optional[int]:
    #     return self.__left_value
    #
    # @right_value.setter
    # def right_value(self, value: int):
    #     self.__right_value = value
    #
    # @right_value.getter
    # def right_value(self) -> int:
    #     return self.__right_value

    def __setup_listeners(self) -> None:
        self.editingFinished.connect(self.__on_editing_finished)

    def __on_editing_finished(self) -> None:
        text = self.text()

        if len(text) == 0:
            self.__left_value = None
            self.__right_value = 0
        elif text[len(text) - 1] == "-":
            self.__left_value = int(text[:-1])
            self.__right_value = self.__left_value
        else:
            numbers = text.split("-")

            if len(numbers) == 2:
                self.__left_value = int(numbers[0])
                self.__right_value = int(numbers[1])

                self.__check_range_and_fix()
            else:
                self.__left_value = None
                self.__right_value = int(numbers[0])

        self.__update_values()

    def __update_values(self) -> None:
        self.lineEdit().setText(
            f"{self.__left_value}-{self.__right_value}" if self.__left_value is not None else str(self.__right_value))

    def stepBy(self, steps: int) -> None:
        self.__right_value += steps

        if self.__right_value < 0:
            self.__right_value = 0
        elif self.__right_value > INT_MAX:
            self.__right_value = INT_MAX

        self.__check_range_and_fix()

        self.lineEdit().setText(
            f"{self.__left_value}-{self.__right_value}" if self.__left_value is not None else str(self.__right_value))

    def __check_range_and_fix(self) -> None:
        if self.__left_value is not None and self.__right_value < self.__left_value:
            self.__left_value = self.__right_value

    def stepEnabled(self) -> QAbstractSpinBox.StepEnabled:
        result = QAbstractSpinBox.StepNone

        if self.__right_value != 0:
            result |= QAbstractSpinBox.StepDownEnabled

        if self.__right_value != INT_MAX:
            result |= QAbstractSpinBox.StepUpEnabled

        return result
