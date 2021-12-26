from __future__ import annotations

import functools
from enum import Enum, IntEnum, auto, unique
from typing import Any, Callable, TypeVar, cast

# TODO https://github.com/PyCQA/pylint/issues/3401
T = TypeVar("T")  # pylint: disable=invalid-name
CACHED_FUNCTIONS = []


def lru_cache(func: Callable[..., T]) -> functools._lru_cache_wrapper[T]:
    """Allows lru_cache to type check correctly."""
    new_func = functools.lru_cache(func)
    CACHED_FUNCTIONS.append(new_func)
    return new_func


@unique
@functools.total_ordering
class Role(Enum):
    """Role Type."""

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

    @lru_cache
    def __lt__(self, other: object) -> bool:
        """This function is necessary to make Role sortable alphabetically."""
        if isinstance(other, Role):
            result = self.value < other.value
            return cast(bool, result)
        return NotImplemented

    @lru_cache
    def __repr__(self) -> str:
        return cast(str, self.value)

    @lru_cache
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
