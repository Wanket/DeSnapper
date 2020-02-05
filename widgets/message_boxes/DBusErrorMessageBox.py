from typing import Optional

from PyQt5.QtWidgets import QWidget
from dbus import DBusException

from widgets.message_boxes.ErrorMessageBox import ErrorMessageBox


class DBusErrorMessageBox(ErrorMessageBox):
    def __init__(self, exception: DBusException, parent: Optional[QWidget] = None):
        dbus_name = exception.get_dbus_name()
        error_strs = dbus_name.split(".")

        super().__init__(error_strs[1].replace("_", " ").capitalize() if len(error_strs) > 1 else dbus_name, parent)
