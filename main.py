#!/usr/bin/env python3

from os import getuid, system
from os.path import abspath
from sys import argv

from PyQt5.QtWidgets import QApplication

from widgets.windows.MainWindow.MainWindow import MainWindow

if __name__ == '__main__':
    if getuid() != 0:
        argv[0] = abspath(argv[0])
        system(f"pkexec env $(env | tr '\\n' ' ') {' '.join(argv)}")
        exit(0)

    app = QApplication(argv)

    window = MainWindow()
    window.show()

    exit(QApplication.exec())
