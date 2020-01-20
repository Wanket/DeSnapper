from datetime import datetime
from enum import Enum
from pwd import getpwuid
from typing import Dict, Tuple


class Snapshot:
    def __init__(self, raw_object):
        self.number: int = raw_object[0]
        self.type = Snapshot.Types(raw_object[1])
        self.pre_number: int = raw_object[2]
        self.date_time: int = raw_object[3]
        self.user_id: int = raw_object[4]
        self.description: str = raw_object[5]
        self.cleanup: str = raw_object[6]
        self.user_data: Dict[str, str] = raw_object[7]

    class Types(Enum):
        Single = 0
        Pre = 1
        Post = 2

    def to_tree_widget_item_array(self) -> Tuple[str, str, str, str, str, str, str]:
        number = str(self.number)
        snapshot_type = self.type.name
        pre_number = str(self.pre_number) if self.pre_number != 0 else ""
        date_time = str(datetime.utcfromtimestamp(self.date_time)) if self.date_time != -1 else ""

        try:
            user_id = getpwuid(self.user_id).pw_name
        except KeyError:
            user_id = "$Unknown"

        return number, snapshot_type, pre_number, date_time, user_id, self.cleanup, self.description
