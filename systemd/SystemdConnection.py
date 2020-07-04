from typing import List

from dbus import SystemBus, Interface


class SystemdConnection:
    def __init__(self):
        bus = SystemBus()

        self.__interface = Interface(bus.get_object("org.freedesktop.systemd1", "/org/freedesktop/systemd1"),
                                     dbus_interface="org.freedesktop.systemd1.Manager")

    def get_unit_file_state(self, unit_name: str) -> bool:
        return self.__interface.GetUnitFileState(unit_name) == "enabled"

    def enable_unit_files(self, unit_names: List[str]) -> None:
        self.__interface.EnableUnitFiles(unit_names, False, False)

    def disable_unit_files(self, unit_names: List[str]) -> None:
        self.__interface.DisableUnitFiles(unit_names, False)
