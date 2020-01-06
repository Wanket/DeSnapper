from typing import Dict


class Config:
    def __init__(self, raw_object):
        self.name: str = raw_object[0]
        self.path: str = raw_object[1]
        self.attrs: Dict[str, str] = raw_object[2]
