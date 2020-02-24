from enum import Flag


class File:
    class StatusFlags(Flag):
        created = 1
        deleted = 2
        type = 4
        content = 8
        permissions = 16
        owner = 32
        # user = 32 deprecated
        group = 64
        xattrs = 128
        acl = 256

        def __str__(self):
            return ", ".join([x for x in super().__str__().split(".")[1].split("|")])

    def __init__(self, raw_object):
        self.path: str = raw_object[0]
        self.status = File.StatusFlags(raw_object[1])
