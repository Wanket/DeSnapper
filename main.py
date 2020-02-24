#!/usr/bin/env python3

from os import getuid
from sys import argv

from PyQt5.QtWidgets import QApplication, QMessageBox

from widgets.windows.MainWindow.MainWindow import MainWindow

if __name__ == "__main__":
    app = QApplication(argv)

    QApplication.setApplicationName("DeSnapper")

    window = MainWindow()

    if getuid() != 0:
        message = QMessageBox(text="Program has been run without root access. Many features may not be available.")
        message.setWindowTitle("DeSnapper")

        window.setWindowTitle("DeSnapper (no root)")

        message.exec()

    window.show()

    exit(QApplication.exec())
