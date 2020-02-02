from typing import Optional

from PyQt5.QtWidgets import QWidget

from snapper.types.Config import Config
from widgets.menus.ActionsMenu import ActionsMenuMeta


class ConfigMenu(metaclass=ActionsMenuMeta):
    _actions = ["Create config", "Edit config", "Delete config"]

    def __init__(self, parent: QWidget, config: Optional[Config]):
        super().__init__(parent)

        self.addAction(self._actions[0])

        if config is not None:
            self.addAction(self._actions[1])
            self.addAction(self._actions[2])
