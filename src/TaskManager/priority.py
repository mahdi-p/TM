"""User defined Enum type."""

from enum import auto, Enum


class Priority(Enum):
    low    = auto()  # 1
    medium = auto()  # 2
    high   = auto()  # 3

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented
