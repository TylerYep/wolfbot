""" statements.py """
from __future__ import annotations

import math
from typing import Optional


class Bits:
    def __init__(self, val: str = "", length: Optional[int] = None) -> None:
        # assert all(ch in ("0", "1") for ch in val)
        self.val = int(val, 2) if val else -1  # -1 == 111111
        self.length = len(val) if length is None else length

    @staticmethod
    def binary_str(val: int, length: int) -> str:
        # return bin(val & (2 ** length - 1))
        coerced_positive_val = val & (2 ** length - 1)
        return f"{coerced_positive_val:0{length}b}"

    def __repr__(self) -> str:
        return self.binary_str(self.val, self.length)

    @classmethod
    def from_num(cls, val: int, length: int) -> Bits:
        return cls(f"{val:b}", length)

    def is_one(self, index: int) -> bool:
        """ Returns True if the bit at given index is 1. """
        return (self.val & (1 << index)) == 0

    def set_bit(self, index: int, new_val: bool) -> None:
        """ Mark an index as the given value of its current state. """
        reversed_index = self.length - index - 1
        if new_val:
            self.val |= (1 << reversed_index)
        else:
            self.val &= ~(1 << reversed_index)

    @property
    def is_solo(self) -> bool:
        return (self.val & (self.val - 1)) == 0

    @property
    def solo(self) -> int:
        """ Assumes is_solo is True. """
        assert self.is_solo
        return self.length - int(math.log2(self.val)) - 1

    def flip_index(self, index: int) -> Bits:
        """ Mark an index as opposite of its current state. """
        # TODO SHOULD THESE RETURN NEW STATES OR MODIFY OLD STATES IN PLACE
        reversed_index = self.length - index - 1
        new_val = self.val
        new_val &= ~(1 << reversed_index)
        if new_val == self.val:
            new_val |= (1 << reversed_index)
        return Bits.from_num(new_val, self.length)

    def __invert__(self) -> Bits:
        """ Inverts all bits. """
        return Bits.from_num(~self.val, self.length)

    def __and__(self, other: object) -> Bits:
        """ Intersection of two role sets. """
        assert isinstance(other, Bits)
        return Bits.from_num(self.val & other.val, self.length)


x = Bits.from_num(42, 10)
# print(x)

x = Bits.from_num(-42, 10)
# print(x)
# print(~x)

y = Bits("11001")
assert str(y) == "11001"
assert y.is_one(1) is True
assert y.is_one(0) is False
assert y.is_solo is False

assert str(~y) == "00110"

y.set_bit(3, True)
assert str(y) == "11011"
y.set_bit(3, False)
assert str(y) == "11001"
y.set_bit(0, False)
assert str(y) == "01001"
y.set_bit(4, False)
assert str(y) == "01000"

assert y.is_solo is True
print(y.solo)
assert y.solo == 1

new_y = y.flip_index(3)
assert str(new_y) == "01010"
