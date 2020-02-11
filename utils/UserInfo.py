from getpass import getuser
from grp import getgrall

from snapper.types.Config import Config


class UserInfo:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls, *args, **kwargs)

        return cls.__instance

    def __init__(self):
        self.user = getuser()
        self.groups = set([group.gr_name for group in getgrall() if self.user in group.gr_mem])

    def is_root(self) -> bool:
        return self.user == "root"

    def check_permissions(self, config: Config) -> bool:
        if self.is_root():
            return True

        if self.user in config.attrs["ALLOW_USERS"].split():
            return True
        else:
            for group in config.attrs["ALLOW_GROUPS"].split():
                if group in self.groups:
                    return True

        return False
