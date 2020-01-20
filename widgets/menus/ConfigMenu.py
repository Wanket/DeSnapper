from typing import Optional, List

from PyQt5.QtWidgets import QWidget

from snapper.types.Config import Config
from widgets.ActionsMenu import ActionsMenuMeta


class ConfigMenu(metaclass=ActionsMenuMeta):
    _actions = ["Create config", "Edit config", "Delete config"]

    def __init__(self, parent: QWidget, configs: List[Config]):
        super().__init__(parent)

        self.addAction(self._actions[0])

        if len(configs) != 0:
            if len(configs) == 1:
                self.addAction(self._actions[1])

            self.addAction(self._actions[2])
