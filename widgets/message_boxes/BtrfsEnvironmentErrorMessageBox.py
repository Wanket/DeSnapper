from typing import Optional

from PyQt5.QtWidgets import QWidget

from widgets.message_boxes.ErrorMessageBox import ErrorMessageBox


class BtrfsEnvironmentErrorMessageBox(ErrorMessageBox):
    def __init__(self, exception: EnvironmentError, parent: Optional[QWidget] = None):
        super().__init__(f"Error while load btrfs quota information: {exception.strerror}", parent)
