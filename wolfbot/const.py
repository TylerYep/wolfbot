from __future__ import annotations

import argparse
import logging
import random
import sys
from collections import Counter
from collections.abc import Sequence
from typing import TypeVar

from wolfbot.enums import Role
from wolfbot.log import logger

# TODO https://github.com/PyCQA/pylint/issues/3401
T = TypeVar("T")  # pylint: disable=invalid-name


def init_program(is_tests: bool) -> argparse.Namespace:
    """Command Line Arguments"""
    parser = argparse.ArgumentParser(description="config constants for main.py")
    # fmt: off
    parser.add_argument("--num_games", "-n", type=int, default=1,
                        help="specify number of games")
    parser.add_argument("--log_level", "-l", type=str,
                        choices=["trace", "debug", "info", "warn"],
                        help="set logging level")
    parser.add_argument("--replay", "-r", action="store_true",
                        help="replay previous game")
    parser.add_argument("--seed", "-s",
                        help="specify game seed")
    parser.add_argument("--user", "-u", action="store_true",
                        help="enable interactive mode")
    # fmt: on
    return parser.parse_args("" if is_tests else sys.argv[1:])


def get_counts(arr: Sequence[T], use_counter_threshold: int = 40) -> dict[T, int]:
    """
    Returns a dict of counts of each item in a list.
    When there are fewer than ~40 items, using a regular
    dictionary is faster than using a Counter.
    """
    if len(arr) < use_counter_threshold:
        counts: dict[T, int] = {}
        for item in arr:
            if item in counts:
                counts[item] += 1
            else:
                counts[item] = 1
        return counts

    return dict(Counter(arr))


ARGS = init_program("pytest" in sys.modules)
if ARGS.seed:
    random.seed(ARGS.seed)

# Game Constants
# These are the player roles used in a game.
ROLES: tuple[Role, ...] = (
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
NUM_ROLES = len(ROLES)
NUM_CENTER = 3 if NUM_ROLES > 8 else 0
# Randomize or use literally the order of the ROLES constant above.
RANDOMIZE_ROLES = True
# Enable multi-statement rounds.
MULTI_STATEMENT = False

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
USE_RELAXED_SOLVER = False
MAX_RELAXED_SOLVER_SOLUTIONS = 5  # len(const.VILLAGE_ROLES)

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
EXPERIENCE_PATH = "wolfbot/learning/simulations/wolf.json"

""" Interactive Game Constants """
INTERACTIVE_MODE = ARGS.user
IS_USER = [False] * NUM_ROLES
USER_ROLE = Role.NONE
NUM_OPTIONS = 5
INFLUENCE_PROB = 0.1

""" Logging """
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

if sys.version_info < (3, 10):
    print(f"Python {sys.version}\n\nWolfBot requires Python 3.10+ to work!\n")
    sys.exit()
