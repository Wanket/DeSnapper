#!/usr/bin/env python3

from os import getuid
from sys import argv

from PyQt5.QtWidgets import QApplication, QMessageBox

from widgets.message_boxes.windows.MainWindow.MainWindow import MainWindow

if __name__ == "__main__":
    app = QApplication(argv)

    window = MainWindow()

    if getuid() != 0:
        message = QMessageBox(text="Program has been run without root access. Not all features may be available.")
        message.setWindowTitle("DeSnapper")

        window.setWindowTitle("DeSnapper (no root)")

        message.exec()

    window.show()

    exit(QApplication.exec())
