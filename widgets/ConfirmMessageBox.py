from PyQt5.QtWidgets import QMessageBox, QWidget


class ConfirmMessageBox(QMessageBox):
    def __init__(self, parent: QWidget, text: str):
        super().__init__(parent, text=text)

        self.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
