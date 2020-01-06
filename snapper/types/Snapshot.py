from typing import Dict


class Snapshot:
    def __init__(self, raw_object):
        self.type: int = raw_object[0]
        self.number: int = raw_object[1]
        self.pre_number: int = raw_object[2]
        self.date_time: int = raw_object[3]
        self.user_id: int = raw_object[4]
        self.description: str = raw_object[5]
        self.cleanup: str = raw_object[6]
        self.user_data: Dict[str, str] = raw_object[7]
