from dataclasses import dataclass


@dataclass
class WorkHeaders:
    id: str
    descr: str
    price: str
    util_info: str
