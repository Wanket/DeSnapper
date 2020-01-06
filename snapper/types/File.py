from enum import Enum


class File:
    class StatusFlags(Enum):
        CREATED = 1
        DELETED = 2
        TYPE = 4
        CONTENT = 8
        PERMISSIONS = 16
        OWNER = 32
        USER = 32
        GROUP = 64
        XATTRS = 128
        ACL = 256

    def __init__(self, raw_object):
        self.path: str = raw_object[0]
        self.status: File.StatusFlags = raw_object[1]
