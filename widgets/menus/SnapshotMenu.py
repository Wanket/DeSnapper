from typing import Optional, List

from PyQt5.QtWidgets import QWidget

from snapper.types.Snapshot import Snapshot
from widgets.ActionsMenu import ActionsMenuMeta


class SnapshotMenu(metaclass=ActionsMenuMeta):
    _actions = ["Create snapshot", "Create pre snapshot", "Create post snapshot", "Edit snapshot", "Delete snapshot"]

    def __init__(self, parent: QWidget, snapshots: List[Snapshot] = None):
        super().__init__(parent)

        self.addAction(self._actions[0])
        self.addAction(self._actions[1])

        if len(snapshots) == 1:
            if snapshots[0].type == Snapshot.Types.Pre:
                self.addAction(self._actions[2])

            self.addAction(self._actions[3])

        if len(snapshots) != 0:
            self.addAction(self._actions[4])
