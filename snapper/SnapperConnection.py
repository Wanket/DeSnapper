from enum import Enum
from typing import List, Dict, NewType, Callable

from _dbus_glib_bindings import DBusGMainLoop
from dbus import SystemBus, Interface

from snapper.BaseHandler import BaseHandler, FunctionType
from snapper.types.Config import Config
from snapper.types.File import File
from snapper.types.Snapshot import Snapshot


class SnapperConnection:
    r"""
    Documentation of this class is based on this documentation:
    https://github.com/openSUSE/snapper/blob/504886a124d6773abb8cc218d57f2753967a0522/doc/dbus-protocol.txt

    Filenames do not include the subvolume.

    Strings are UTF-8. Other characters (e.g. in filenames) must be encoded
    hexadecimal as "\x??". As a consequence "\" must be encoded as "\\".

    Due to security concerns there are no methods to get, compare or revert
    files. This can be done in the client.

    Some snapshots cannot be deleted (current, default and active). Delete
    requests for these are ignored."""

    SnapshotNumber = NewType("SnapshotNumber", int)

    PathStr = NewType("PathStr", str)

    NumFiles = NewType("NumFiles", int)

    ConfigName = NewType("ConfigName", str)

    def __init__(self):
        DBusGMainLoop(set_as_default=True)

        bus = SystemBus()

        self.__interface = Interface(bus.get_object("org.opensuse.Snapper", "/org/opensuse/Snapper"),
                                     dbus_interface="org.opensuse.Snapper")

        self.config_created = self.__register_handler("ConfigCreated",
                                                      BaseHandler[Callable[[SnapperConnection.ConfigName], None]]())
        self.config_deleted = self.__register_handler("ConfigModified",
                                                      BaseHandler[Callable[[SnapperConnection.ConfigName], None]]())
        self.config_modified = self.__register_handler("ConfigDeleted",
                                                       BaseHandler[Callable[[SnapperConnection.ConfigName], None]]())

        self.snapshot_created = self.__register_handler("SnapshotCreated", BaseHandler[
            Callable[[SnapperConnection.ConfigName, SnapperConnection.SnapshotNumber], None]]())
        self.snapshot_deleted = self.__register_handler("SnapshotModified", BaseHandler[
            Callable[[SnapperConnection.ConfigName, SnapperConnection.SnapshotNumber], None]]())
        self.snapshot_modified = self.__register_handler("SnapshotsDeleted", BaseHandler[
            Callable[[SnapperConnection.ConfigName, List[SnapperConnection.SnapshotNumber]], None]]())

    # region ConfigData
    def list_configs(self) -> List[Config]:
        return [Config(x) for x in self.__interface.ListConfigs()]

    def get_config(self, config_name: str) -> Config:
        return Config(self.__interface.GetConfig(config_name))

    def set_config(self, config_name: str, attrs: Dict[str, str]) -> None:
        return self.__interface.SetConfig(config_name, attrs)

    # endregion

    # region Create/Delete config
    def create_config(self, config_name: str, sub_volume: str, fs_type: str, template_name: str) -> None:
        return self.__interface.CreateConfig(config_name, sub_volume, fs_type, template_name)

    def delete_config(self, config_name: str) -> None:
        return self.__interface.DeleteConfig(config_name)

    # endregion

    # region Lock config
    """
    Locking disallows other clients to delete the config and delete snapshots for the config but not to create new 
    snapshots for the config. Several clients can lock the same config."""

    def lock_config(self, config_name: str) -> None:
        return self.__interface.LockConfig(config_name)

    def unlock_config(self, config_name: str) -> None:
        return self.__interface.UnlockConfig(config_name)

    # endregion

    # region SnapshotsData
    def list_snapshots(self, config_name: str) -> List[Snapshot]:
        return [Snapshot(x) for x in self.__interface.ListSnapshots(config_name)]

    def get_snapshot(self, config_name: str, number: int) -> Snapshot:
        return Snapshot(self.__interface.GetSnapshot(config_name, number))

    def set_snapshot(self, snapshot: Snapshot) -> None:
        return self.__interface.SetSnapshot(snapshot.number, snapshot.description, snapshot.cleanup, snapshot.user_data)

    # endregion

    # region Create/Delete snapshot

    def create_single_snapshot(self, config_name: str, description: str, cleanup: str,
                               user_data: str) -> SnapshotNumber:
        return self.__interface.CreateSingleSnapshot(config_name, description, cleanup, user_data)

    def create_single_snapshot_v2(self, config_name: str, parent_number: int, read_only: bool, description: str,
                                  cleanup: str, user_data: str) -> SnapshotNumber:
        return self.__interface.CreateSingleSnapshot(config_name, parent_number, read_only, description, cleanup,
                                                     user_data)

    def create_single_snapshot_of_default(self, config_name: str, read_only: bool, description: str, cleanup: str,
                                          user_data: str) -> SnapshotNumber:
        return self.__interface.CreateSingleSnapshot(config_name, read_only, description, cleanup, user_data)

    def create_pre_snapshot(self, config_name, description, cleanup, user_data) -> SnapshotNumber:
        return self.__interface.CreatePreSnapshot(config_name, description, cleanup, user_data)

    def create_post_snapshot(self, config_name, pre_number, description, cleanup, user_data) -> SnapshotNumber:
        return self.__interface.CreatePreSnapshot(config_name, pre_number, description, cleanup, user_data)

    def delete_snapshots(self, config_name, numbers: List[int]) -> None:
        return self.__interface.DeleteSnapshots(config_name, numbers)

    # endregion

    # TODO these methods will be in 20.04
    # method GetDefaultSnapshot config-name -> bool number
    # method GetActiveSnapshot config-name -> bool number

    # method CalculateUsedSpace config-name (experimental)
    # method GetUsedSpace config-name number -> number (experimental)

    # region (un)mount
    """Snapshots mounted with user-request set to false will be unmounted (delayed) after the client disconnects."""

    def mount_snapshot(self, config_name: str, number: int, user_request: bool) -> PathStr:
        return self.__interface.MountSnapshot(config_name, number, user_request)

    def unmount_snapshot(self, config_name: str, number: int, user_request: bool) -> None:
        return self.__interface.UmountSnapshot(config_name, number, user_request)

    def get_mount_point(self, config_name, number) -> PathStr:
        return self.__interface.GetMountPoint(config_name, number)

    # endregion

    def sync(self, config_name: str) -> None:
        return self.__interface.Sync(config_name)

    # region Comparison
    def create_comparison(self, config_name: str, number1: int, number2: int) -> NumFiles:
        return self.__interface.CreateComparison(config_name, number1, number2)

    def delete_comparison(self, config_name: str, number1: int, number2: int) -> None:
        return self.__interface.DeleteComparison(config_name, number1, number2)

    def get_files(self, config_name: str, number1: int, number2: int) -> List[File]:
        """The following command require a successful CreateComparison in advance."""

        return self.__interface.GetFiles(config_name, number1, number2)

    # endregion

    # region Signals
    def __register_handler(self, signal_mame, handler: BaseHandler[FunctionType]) -> BaseHandler[FunctionType]:
        self.__interface.connect_to_signal(signal_mame, lambda *args, **kwargs: handler.emit(args, kwargs))

        return handler
    # endregion
