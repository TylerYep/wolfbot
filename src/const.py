""" const.py """
from __future__ import annotations

import argparse
import functools
import logging
import random
import sys
from collections import Counter
from enum import Enum, IntEnum, auto, unique
from typing import Any, Callable, Dict, Sequence, TypeVar, cast

from src.log import OneNightLogger

# TODO https://github.com/PyCQA/pylint/issues/3401
T = TypeVar("T")  # pylint: disable=invalid-name
CACHED_FUNCTIONS = []


def lru_cache(  # pylint: disable=protected-access
    func: Callable[..., T]
) -> functools._lru_cache_wrapper[T]:
    """ Allows lru_cache to type check correctly. """
    new_func = functools.lru_cache()(func)
    CACHED_FUNCTIONS.append(new_func)
    return new_func


def init_program(is_unit_test: bool) -> argparse.Namespace:
    """ Command Line Arguments """
    parser = argparse.ArgumentParser(description="config constants for main.py")
    # fmt: off
    parser.add_argument("--num_games", "-n", type=int, default=1,
                        help="specify number of games")
    parser.add_argument("--log_level", "-l", type=str,
                        choices=["trace", "debug", "info", "warn"],
                        help="set logging level")
    parser.add_argument("--replay", "-r", action="store_true", default=False,
                        help="replay previous game")
    parser.add_argument("--seed", "-s",
                        help="specify game seed")
    parser.add_argument("--user", "-u", action="store_true", default=False,
                        help="enable interactive mode")
    # fmt: on
    return parser.parse_args("" if is_unit_test else sys.argv[1:])


def get_counts(arr: Sequence[T]) -> Dict[T, int]:
    """
    Returns a dict of counts of each item in a list.
    When there are fewer than ~40 items, using a regular
    dictionary is faster than using a Counter.
    """
    if len(arr) < 40:
        counts: Dict[T, int] = {}
        for item in arr:
            if item in counts:
                counts[item] += 1
            else:
                counts[item] = 1
        return counts

    return dict(Counter(arr))


@unique
@functools.total_ordering
class Role(Enum):
    """ Role Type. """

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
        """ This function is necessary to make Role sortable alphabetically. """
        if not isinstance(other, Role):
            raise NotImplementedError
        result = self.value < other.value  # pylint: disable=comparison-with-callable
        return cast(bool, result)

    @lru_cache
    def __repr__(self) -> str:  # pylint: disable=invalid-repr-returned
        return cast(str, self.value)

    @lru_cache
    def __format__(  # pylint: disable=invalid-format-returned
        self, formatstr: str
    ) -> str:
        del formatstr
        return cast(str, self.value)

    def json_repr(self) -> Dict[str, Any]:
        """ Gets JSON representation of a Role enum. """
        return {"type": "Role", "data": self.value}


ARGS = init_program("pytest" in sys.modules)
if ARGS.seed:
    random.seed(ARGS.seed)

# Game Constants
# These are the player roles used in a game.
ROLES = (
    Role.DRUNK,
    Role.INSOMNIAC,
    Role.HUNTER,
    Role.MASON,
    Role.MASON,
    Role.MINION,
    Role.ROBBER,
    Role.SEER,
    Role.TANNER,
    Role.TROUBLEMAKER,
    Role.WOLF,
    Role.WOLF,
    Role.VILLAGER,
    Role.VILLAGER,
    Role.VILLAGER,
)
NUM_CENTER = 3
# Randomize or use literally the order of the ROLES constant above.
RANDOMIZE_ROLES = True
# Enable multi-statement rounds.
MULTI_STATEMENT = True

""" Simulation Constants """
NUM_GAMES = ARGS.num_games
MAX_LOG_GAMES = 10
FIXED_WOLF_INDEX = -1
SAVE_REPLAY = NUM_GAMES < MAX_LOG_GAMES
REPLAY_FILE = "data/replay.json"
REPLAY_STATE = "data/replay_state.json"
REPLAY = ARGS.replay

""" Util Constants """
ROLE_SET = frozenset(ROLES)
SORTED_ROLE_SET = sorted(ROLE_SET)
NUM_ROLES = len(ROLES)
ROLE_COUNTS = get_counts(ROLES)  # Dict of {Role.VILLAGER: 3, Role.WOLF: 2, ... }
NUM_PLAYERS = NUM_ROLES - NUM_CENTER

""" Game Rules """
AWAKE_ORDER = (
    Role.WOLF,
    Role.MINION,
    Role.MASON,
    Role.SEER,
    Role.ROBBER,
    Role.TROUBLEMAKER,
    Role.DRUNK,
    Role.INSOMNIAC,
)
VILLAGE_ROLES = (
    frozenset(
        {
            Role.VILLAGER,
            Role.MASON,
            Role.SEER,
            Role.ROBBER,
            Role.TROUBLEMAKER,
            Role.DRUNK,
            Role.INSOMNIAC,
            Role.HUNTER,
        }
    )
    & ROLE_SET
)
EVIL_ROLES = frozenset({Role.TANNER, Role.WOLF, Role.MINION}) & ROLE_SET

""" Village Players """
CENTER_SEER_PROB = 0.9
SMART_VILLAGERS = True

""" Werewolf Players """
# Basic Wolf Player (Pruned statement set)
USE_REG_WOLF = True
INCLUDE_STATEMENT_RATE = 0.7

# Expectimax Wolf, Minion, Tanner
EXPECTIMAX_WOLF = False
EXPECTIMAX_DEPTH = 1
BRANCH_FACTOR = 5
EXPECTIMAX_TANNER = False
EXPECTIMAX_MINION = EXPECTIMAX_WOLF

# Reinforcement Learning Wolf
RL_WOLF = False
EXPERIENCE_PATH = "src/learning/simulations/wolf.json"

""" Interactive Game Constants """
INTERACTIVE_MODE = ARGS.user
IS_USER = [False] * NUM_ROLES
USER_ROLE = Role.NONE
NUM_OPTIONS = 5
INFLUENCE_PROB = 0.1

""" Logging """
logger = OneNightLogger()

if ARGS.log_level:
    log_levels = {
        "trace": logger.trace_level,
        "debug": logging.DEBUG,
        "info": logging.INFO,
        "warn": logging.WARNING,
    }
    logger.set_level(log_levels[ARGS.log_level])
elif INTERACTIVE_MODE:
    logger.set_level(logging.INFO)

if sys.version_info < (3, 9):
    sys.stdout.write("Python " + sys.version)
    sys.stdout.write("\n\nWolfBot requires Python 3.9+ to work!\n\n")
    sys.exit()


@unique
class SwitchPriority(IntEnum):
    """ Priorities for switch actions, in order that they are performed. """

    ROBBER, TROUBLEMAKER, DRUNK = 1, 2, 3


@unique
class StatementLevel(IntEnum):
    """ Statement Priority Levels. Only the order of the values matters. """

    NOT_YET_SPOKEN = -1
    NO_INFO = 0
    SOME_INFO = 5
    PRIMARY = 10


@unique
class Team(Enum):
    """ Team names, order doesn't matter. """

    VILLAGE, TANNER, WEREWOLF = auto(), auto(), auto()

    def json_repr(self) -> Dict[str, Any]:
        """ Gets JSON representation of a Role enum. """
        return {"type": "Team", "data": self.value}
