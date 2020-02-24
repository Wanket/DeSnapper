from typing import Optional

from PyQt5.QtGui import QTextBlockFormat, QColor, QFont, QTextCursor
from PyQt5.QtWidgets import QWidget, QPlainTextEdit, QHBoxLayout
from sxsdiff.calculator import DiffCalculator, LineChange, Element


class DiffWidget(QWidget):
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)

        self.__left_widget = QPlainTextEdit(self)
        self.__right_widget = QPlainTextEdit(self)

        self.__default_format = self.__left_widget.textCursor().blockFormat()

        self.__red_format = QTextBlockFormat()
        self.__red_format.setBackground(QColor.fromRgba(0x11ff001e))

        self.__green_format = QTextBlockFormat()
        self.__green_format.setBackground(QColor.fromRgba(0x1900ff47))

        self.__void_format = QTextBlockFormat()
        self.__void_format.setBackground(QColor.fromRgba(0x08007efc))

        self.__setup_ui()

        self.__setup_listeners()

    def __setup_ui(self) -> None:
        layout = QHBoxLayout(self)

        layout.addWidget(self.__left_widget)
        layout.addWidget(self.__right_widget)

        self.setLayout(layout)

        self.__left_widget.setLineWrapMode(QPlainTextEdit.NoWrap)
        self.__right_widget.setLineWrapMode(QPlainTextEdit.NoWrap)

        font = QFont("monospace")

        self.__left_widget.setFont(font)
        self.__right_widget.setFont(font)

        self.__left_widget.setReadOnly(True)
        self.__right_widget.setReadOnly(True)

    def __setup_listeners(self) -> None:
        self.__left_widget.verticalScrollBar().valueChanged.connect(self.__right_widget.verticalScrollBar().setValue)
        self.__right_widget.verticalScrollBar().valueChanged.connect(self.__left_widget.verticalScrollBar().setValue)

        self.__left_widget.horizontalScrollBar().valueChanged.connect(
            self.__right_widget.horizontalScrollBar().setValue)
        self.__right_widget.horizontalScrollBar().valueChanged.connect(
            self.__left_widget.horizontalScrollBar().setValue)

    def clear(self):
        self.__left_widget.clear()
        self.__right_widget.clear()

    def fill_diff(self, text1, text2) -> None:
        self.clear()

        for diff_line in DiffCalculator().run(text1, text2):
            if diff_line.left:
                line = DiffWidget.__generate_line(diff_line, "ff001d", "- ", diff_line.left_no)

                for diff_element in diff_line.left.elements:
                    line += DiffWidget.__generate_element(diff_element, "fd001d", -1)

                self.__append_html(self.__left_widget, line, self.__red_format, diff_line)
            else:
                self.__append_void(self.__left_widget)

            if diff_line.right:
                line = DiffWidget.__generate_line(diff_line, "00f23b", "+ ", diff_line.right_no)

                for diff_element in diff_line.right.elements:
                    line += DiffWidget.__generate_element(diff_element, "00f23b", 1)

                self.__append_html(self.__right_widget, line, self.__green_format, diff_line)
            else:
                self.__append_void(self.__right_widget)

        self.__left_widget.moveCursor(QTextCursor.Start)
        self.__right_widget.moveCursor(QTextCursor.Start)

    def __append_void(self, text_edit: QPlainTextEdit) -> None:
        text_edit.appendPlainText("")
        text_edit.textCursor().setBlockFormat(self.__void_format)

    def __append_html(self, text_edit: QPlainTextEdit, line: str, text_block_format: QTextBlockFormat,
                      diff_line: LineChange) -> None:
        text_edit.appendHtml(line)
        text_edit.textCursor().setBlockFormat(text_block_format if diff_line.changed else self.__default_format)

    @staticmethod
    def __generate_element(diff_element: Element, color: str, flag: int) -> None:
        return f'<span style="background-color: #39{color}">{diff_element.text}</span>' if diff_element.flag == flag \
            else diff_element.text

    @staticmethod
    def __generate_line(diff_line: LineChange, color: str, prefix: str, number: Optional[int]) -> str:
        return f'<span style="background-color: #{"14" if diff_line.changed else "00"}{color}">' \
               f'{DiffWidget.__generate_int_str(number)}</span>&nbsp;{prefix if diff_line.changed else "&nbsp;&nbsp;"}'

    @staticmethod
    def __generate_int_str(integer: int) -> str:
        return "&nbsp;" * (4 - len(str(integer))) + str(integer) + "&nbsp;"
