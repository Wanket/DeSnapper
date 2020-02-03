from typing import Optional

from PyQt5.QtWidgets import QWidget
from dbus import DBusException

from widgets.message_boxes.ErrorMessageBox import ErrorMessageBox


class DBusErrorMessageBox(ErrorMessageBox):
    def __init__(self, exception: DBusException, parent: Optional[QWidget] = None):
        super().__init__(exception.get_dbus_name().split(".")[1].replace("_", " ").capitalize(), parent)
