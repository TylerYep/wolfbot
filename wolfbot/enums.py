from __future__ import annotations

import functools
from enum import Enum, IntEnum, auto, unique
from typing import Any, Callable, TypeVar, cast

T = TypeVar("T")
CACHED_FUNCTIONS = set()


def lru_cache(func: Callable[..., T]) -> functools._lru_cache_wrapper[T]:
    """Allows lru_cache to type check correctly."""
    new_func = functools.lru_cache(func)
    CACHED_FUNCTIONS.add(new_func)
    return new_func


@unique
@functools.total_ordering
class Role(Enum):
    """Role Type."""

    DOPPELGANGER = "Doppelganger"
    DRUNK = "Drunk"
    HUNTER = "Hunter"
    INSOMNIAC = "Insomniac"
    MASON = "Mason"
    MINION = "Minion"
    NONE = ""
    ROBBER = "Robber"
    SEER = "Seer"
    TANNER = "Tanner"
    TROUBLEMAKER = "Troublemaker"
    WOLF = "Wolf"
    VILLAGER = "Villager"

    def __lt__(self, other: object) -> bool:
        """This function is necessary to make Role sortable alphabetically."""
        if isinstance(other, Role):
            result = self.value < other.value
            return result
        return NotImplemented

    def __repr__(self) -> str:
        return cast(str, self.value)

    def __format__(self, formatstr: str) -> str:
        del formatstr
        return cast(str, self.value)

    def json_repr(self) -> dict[str, Any]:
        """Gets JSON representation of a Role enum."""
        return {"type": "Role", "data": self.value}


@unique
class SwitchPriority(IntEnum):
    """Priorities for switch actions, in order that they are performed."""

    ROBBER, TROUBLEMAKER, DRUNK = 1, 2, 3


@unique
class StatementLevel(IntEnum):
    """Statement Priority Levels. Only the order of the values matters."""

    NOT_YET_SPOKEN = -1
    NO_INFO = 0
    SOME_INFO = 5
    PRIMARY = 10


@unique
class Team(Enum):
    """Team names, order doesn't matter."""

    VILLAGE, TANNER, WEREWOLF = auto(), auto(), auto()

    def json_repr(self) -> dict[str, Any]:
        """Gets JSON representation of a Role enum."""
        return {"type": "Team", "data": self.value}


class UnhandledEnumValueError(Exception):
    """Unhandled enum value exception."""

    message = "Encountered unhandled enum value."
