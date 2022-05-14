"""The objects that can come into play as a little pieces"""
from dataclasses import dataclass
from functools import total_ordering
from typing import List


@dataclass
@total_ordering
class WorkHeaders:
    """Represent a task with characteristics"""
    uuid: str  # maybe uuid type?
    descr: str
    price: str
    util_info: str
    source: str

    def __ge__(self, other):
        """Make items self-measurable"""
        # TODO regex digits at least
        price2num = int(self.price.replace(' ', ''))
        price2num0 = int(other.price.replace(' ', ''))
        return price2num0 < price2num

    def __eq__(self, other):
        """When work is same in practice"""
        return self.price == other.price and self.descr == other.descr

    def __str__(self):
        """Easy human-readable representaion of class objects"""
        return f'You do: {self.descr}, for price: {self.price}. {self.util_info}.'

@dataclass
class HabrWorkHeader(WorkHeaders):
    tags: List[str]
