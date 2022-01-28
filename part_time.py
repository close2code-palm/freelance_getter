from dataclasses import dataclass


@dataclass
class WorkHeaders:
    id: str
    descr: str
    price: str
    util_info: str

    def __ge__(self, other):
        price2num = int(self.price.replace(' ', ''))
        price2num0 = int(other.price.replace(' ', ''))
        return price2num0 < price2num
