from typing import Dict

from PyQt5.QtWidgets import QMenu, QAction, QWidget
from sip import wrappertype


class ActionMenuBase(QMenu):
    _actions = list()

    def __init__(self, parent: QWidget):
        super().__init__(parent)

        actions = list()

        for (name, attr_name) in self.__class__._actions:
            action = QAction(name)

            setattr(self, attr_name, action.triggered)
            actions.append(action)

        self._actions = actions


class ActionsMenuMeta(wrappertype):
    def __new__(cls, name: str, bases: tuple, attrs: Dict):
        bases += (ActionMenuBase,)

        actions = list()

        for item in attrs["_actions"]:
            attr_name = f"action_{item.replace(' ', '_').lower()}"

            actions.append((item, attr_name))

        attrs["_actions"] = actions

        return super().__new__(cls, name, bases, attrs)
