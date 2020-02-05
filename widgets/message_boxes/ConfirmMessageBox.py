from PyQt5.QtWidgets import QMessageBox, QWidget


class ConfirmMessageBox(QMessageBox):
    def __init__(self, parent: QWidget, title: str, text: str):
        super().__init__(parent, text=text)

        self.setWindowTitle(title)

        self.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
