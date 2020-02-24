from typing import Optional

from PyQt5.QtWidgets import QWidget
from dbus import DBusException

from widgets.message_boxes.ErrorMessageBox import ErrorMessageBox


class DBusErrorMessageBox(ErrorMessageBox):
    def __init__(self, exception: DBusException, parent: Optional[QWidget] = None):
        super().__init__(f"DBus error: {exception.get_dbus_name()}\n{exception.get_dbus_message()}", parent)
