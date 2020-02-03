from typing import Optional

from PyQt5.QtWidgets import QMessageBox, QWidget


class ErrorMessageBox(QMessageBox):
    def __init__(self, text: str, parent: Optional[QWidget] = None):
        super().__init__(text=text, parent=parent)

        self.setWindowTitle("Error")
