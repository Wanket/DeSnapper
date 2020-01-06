#!/usr/bin/env python3

from os import getuid, system
from os.path import abspath
from sys import argv

from PyQt5.QtWidgets import QApplication, QWidget

from snapper.SnapperConnection import SnapperConnection

if __name__ == '__main__':
    if getuid() != 0:
        argv[0] = abspath(argv[0])
        system(f"pkexec env $(env | tr '\\n' ' ') {' '.join(argv)}")
        exit(0)

    conn = SnapperConnection()

    app = QApplication(argv)

    widget = QWidget()
    widget.show()

    exit(app.exec())
