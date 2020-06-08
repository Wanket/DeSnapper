from collections import deque
from os.path import isfile, isdir, islink, realpath
from pathlib import Path
from subprocess import Popen
from typing import Dict, Optional, Tuple, Deque

import sip
from PyQt5.QtCore import Qt, QTemporaryFile
from PyQt5.QtWidgets import QDialog, QTreeWidgetItem, QMessageBox
from chardet import detect
from dbus import DBusException

from snapper.SnapperConnection import SnapperConnection
from snapper.types.File import File
from snapper.types.Snapshot import Snapshot
from widgets.message_boxes.ConfirmMessageBox import ConfirmMessageBox
from widgets.message_boxes.DBusErrorMessageBox import DBusErrorMessageBox
from widgets.message_boxes.ErrorMessageBox import ErrorMessageBox
from widgets.windows.DiffWindow.Ui_DiffWindow import Ui_DiffWindow


# TODO: Rewrite making filesystem tree functions when (if?) issue https://github.com/openSUSE/snapper/issues/176
#  will be closed

class DiffWindow(QDialog):
    def __init__(self, config_name: str, snapshots: Dict[SnapperConnection.SnapshotNumber, Snapshot],
                 connection: SnapperConnection):
        super().__init__()

        self.__ui = Ui_DiffWindow()

        self.__ui.setupUi(self)

        self.__config_name = config_name

        self.__snapshots = snapshots

        self.__conn = connection

        self.__comparison_pair: Optional[Tuple[SnapperConnection.SnapshotNumber, SnapperConnection.SnapshotNumber]] = \
            None

        self.__paths: Dict[str, File.StatusFlags] = dict()

        self.__current_path: Optional[str] = None

        self.__setup_listeners()

        self.__setup_ui()

    def __del__(self):
        if self.__comparison_pair is not None:
            try:
                self.__conn.delete_comparison(self.__config_name, self.__comparison_pair[0], self.__comparison_pair[1])
            except DBusException:
                pass

    # region Common functions

    def exec(self) -> int:
        self.__ui.fileWidget.hide()

        result = super().exec()

        return result

    def __setup_listeners(self) -> None:
        self.__ui.comparePushButton.clicked.connect(self.__on_compare_push_button_clicked)

        self.__ui.pathsTreeWidget.itemChanged.connect(self.__on_tree_item_changed)
        self.__ui.pathsTreeWidget.itemSelectionChanged.connect(self.__on_tree_item_selection_changed)

        self.__ui.undoPushButton.clicked.connect(self.__on_undo_push_button_clicked)

        self.__ui.forceDiffPushButton.clicked.connect(self.__on_force_diff_push_button_clicked)

    def __setup_ui(self) -> None:
        snapshot_numbers = [str(snapshot_number) for snapshot_number in self.__snapshots.keys()]

        self.__ui.firstSnapshotComboBox.addItems(snapshot_numbers)
        self.__ui.secondSnapshotComboBox.addItems(snapshot_numbers)

    # endregion

    # region Slots

    def __on_compare_push_button_clicked(self) -> None:
        first_number = int(self.__ui.firstSnapshotComboBox.currentText())
        second_number = int(self.__ui.secondSnapshotComboBox.currentText())

        if first_number == second_number:
            ErrorMessageBox("Snapshot must not be same").exec()

            return

        first_snapshot = self.__snapshots[first_number]
        second_snapshot = self.__snapshots[second_number]

        if first_snapshot.number == second_snapshot.pre_number or \
                second_snapshot.number == first_snapshot.pre_number or \
                ConfirmMessageBox(self, "Compare snapshot",
                                  "Compare not pre-post pair snapshots may be long. Continue?").exec() == \
                QMessageBox.Ok:
            if self.__comparison_pair is not None:
                try:
                    self.__conn.delete_comparison(self.__config_name, self.__comparison_pair[0],
                                                  self.__comparison_pair[1])
                except DBusException:
                    pass

                self.__ui.pathsTreeWidget.clear()
                self.__ui.pathsTreeWidget.headerItem().setText(0, "File system")

                self.__ui.fileWidget.hide()

            try:
                self.__conn.create_comparison(self.__config_name, first_number, second_number)
            except DBusException as e:
                DBusErrorMessageBox(e).exec()

                return

            self.__comparison_pair = (first_number, second_number)

            self.__fill_tree()

    def __on_tree_item_selection_changed(self) -> None:
        items = self.__ui.pathsTreeWidget.selectedItems()

        if len(items) == 0:
            return

        item = items[0]

        paths = deque()

        paths.appendleft(item.text(0))

        parent = item.parent()

        while parent is not None:
            paths.appendleft(parent.text(0))

            parent = parent.parent()

        paths.popleft()
        paths.appendleft("")

        path = "/".join(paths)

        if path not in self.__paths:
            self.__ui.fileWidget.hide()

            return

        self.__ui.changedLabel.setText(str(self.__paths[path]))

        self.__ui.fileWidget.show()
        self.__ui.forceDiffWidget.hide()

        self.__current_path = path

        self.__try_fast_diff()

    def __on_tree_item_changed(self, item: QTreeWidgetItem, _: int) -> None:
        self.__ui.pathsTreeWidget.blockSignals(True)

        items_queue: Deque[QTreeWidgetItem] = deque()

        items_queue.append(item)

        state = item.checkState(0)

        while len(items_queue) != 0:
            queue_item = items_queue.popleft()

            for i in range(queue_item.childCount()):
                child = queue_item.child(i)

                if child.checkState(0) != state:
                    child.setCheckState(0, state)

                    items_queue.append(child)

        parent = item.parent()

        while parent is not None:
            count_checked = 0

            parent_state = Qt.Unchecked

            for i in range(parent.childCount()):
                child = parent.child(i)

                state = child.checkState(0)

                if state == Qt.PartiallyChecked:
                    parent_state = Qt.PartiallyChecked

                    break

                count_checked += state == Qt.Checked

            if count_checked == parent.childCount():
                parent_state = Qt.Checked
            elif count_checked > 0:
                parent_state = Qt.PartiallyChecked

            parent.setCheckState(0, parent_state)

            parent = parent.parent()

        self.__ui.pathsTreeWidget.blockSignals(False)

    def __on_undo_push_button_clicked(self) -> None:
        files = QTemporaryFile()

        files.open()

        selected_items = list()

        items: Deque[Tuple[QTreeWidgetItem, str]] = deque()

        items.append((self.__ui.pathsTreeWidget.topLevelItem(0), ""))

        while len(items) != 0:
            item, path = items.popleft()

            selected_items.append(item)

            if item.checkState(0) == Qt.Checked and path in self.__paths:
                files.write(bytes(path, encoding="utf-8"))
                files.write(bytes("\n", encoding="utf-8"))

            for i in range(item.childCount()):
                child = item.child(i)

                items.append((child, f"{path}/{child.text(0)}"))

        del items

        files.close()

        print(files.fileName())

        first_number, second_number = self.__comparison_pair

        snapper_proc = Popen(["snapper", "undochange", "-i", files.fileName(), f"{first_number}..{second_number}"])
        snapper_proc.wait()

        files.remove()

        success = snapper_proc.returncode == 0

        message = QMessageBox(text=f"Undo change selected files has finished" if success
                              else f"Undo change has been finished with errors")
        message.setWindowTitle("Undo change")

        if success:
            for item in selected_items:
                try:
                    sip.delete(item)
                except RuntimeError:
                    pass
        else:
            self.__ui.pathsTreeWidget.clear()
            self.__ui.pathsTreeWidget.headerItem().setText(0, "File system")

            self.__fill_tree()

        message.exec()

    def __on_force_diff_push_button_clicked(self):
        first_number, second_number = self.__comparison_pair

        self.__diff(self.__get_real_path(first_number, self.__current_path),
                    self.__get_real_path(second_number, self.__current_path))

    # endregion

    def __fill_tree(self) -> None:
        self.__ui.pathsTreeWidget.blockSignals(True)

        first_number, second_number = self.__comparison_pair

        try:
            files = self.__conn.get_files(self.__config_name, first_number, second_number)
        except DBusException as e:
            DBusErrorMessageBox(e).exec()

            self.__ui.pathsTreeWidget.blockSignals(False)

            return

        root_item = QTreeWidgetItem(self.__ui.pathsTreeWidget, ["/"])
        root_item.setCheckState(0, Qt.Unchecked)

        self.__ui.pathsTreeWidget.addTopLevelItem(root_item)

        for file in files:
            self.__paths[file.path] = file.status

            split_path = file.path.split("/")

            current_item = root_item

            for i in range(1, len(split_path) - 1):
                found = False

                for j in range(current_item.childCount()):
                    child = current_item.child(j)

                    if child.text(0) == split_path[i]:
                        current_item = child

                        found = True

                        break

                if not found:
                    current_item = QTreeWidgetItem(current_item, [split_path[i]])
                    current_item.setCheckState(0, Qt.Unchecked)

            current_item = QTreeWidgetItem(current_item, [split_path[len(split_path) - 1]])
            current_item.setCheckState(0, Qt.Unchecked)

        self.__ui.pathsTreeWidget.headerItem().setText(0, f"File system ({first_number}-{second_number})")

        self.__ui.pathsTreeWidget.blockSignals(False)

    def __get_real_path(self, snapshot_number: int, path: str) -> str:
        result_path = self.__conn.get_mount_point(self.__config_name, snapshot_number) + path

        while islink(result_path):
            path = realpath(result_path)

            result_path = self.__conn.get_mount_point(self.__config_name, snapshot_number) + path

        return result_path

    # region Diff functions

    def __try_fast_diff(self) -> None:
        self.__ui.diffWidget.clear()

        if not (self.__paths[self.__current_path] &
                (File.StatusFlags.content | File.StatusFlags.created | File.StatusFlags.deleted)).value:
            return

        first_number, second_number = self.__comparison_pair

        first_path = self.__get_real_path(first_number, self.__current_path)
        second_path = self.__get_real_path(second_number, self.__current_path)

        if isdir(first_path) or isdir(second_path):
            return

        is_file_first = isfile(first_path)
        is_file_second = isfile(second_path)

        first_size = Path(first_path).stat().st_size if is_file_first else 0

        second_size = Path(second_path).stat().st_size if is_file_second else 0

        if max(first_size, second_size) > 20_480:
            self.__ui.forceDiffWidget.show()

            return

        self.__diff(first_path, second_path)

    def __diff(self, real_first_path: str, real_second_path: str):
        is_file_first = isfile(real_first_path)
        is_file_second = isfile(real_second_path)

        try:
            first_text = DiffWindow.__read_file(real_first_path) if is_file_first else ""
            second_text = DiffWindow.__read_file(real_second_path) if is_file_second else ""
        except (UnicodeDecodeError, TypeError):
            first_text = f"{self.__current_path} is a binary file"

            second_text = first_text

        if first_text == "" and second_text == "":
            return

        self.__ui.diffWidget.fill_diff(first_text, second_text)

        self.__ui.forceDiffWidget.hide()

    # endregion

    @staticmethod
    def __read_file(path: str) -> str:
        with open(path, "rb") as file:
            raw_data = file.read()

            return raw_data.decode(detect(raw_data)["encoding"])
