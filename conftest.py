""" conftest.py """
import random
from collections import Counter
from typing import List, Tuple

import pytest

from fixtures import *
from src import const


@pytest.fixture(autouse=True)
def reset_const():
    const.logger.setLevel(const.TRACE)
    const.ROLES = (
        "Insomniac",
        "Villager",
        "Robber",
        "Villager",
        "Drunk",
        "Wolf",
        "Wolf",
        "Seer",
        "Tanner",
        "Mason",
        "Minion",
        "Troublemaker",
        "Villager",
        "Mason",
        "Hunter",
    )
    const.ROLE_SET = set(const.ROLES)
    const.ROLE_COUNTS = dict(Counter(const.ROLES))
    const.NUM_ROLES = len(const.ROLES)
    const.NUM_PLAYERS = 12
    const.NUM_CENTER = 3
    const.CENTER_SEER_PROB = 0.9
    const.VILLAGE_ROLES = {
        "Villager",
        "Mason",
        "Seer",
        "Robber",
        "Troublemaker",
        "Drunk",
        "Insomniac",
        "Hunter",
    }
    const.EVIL_ROLES = {"Tanner", "Wolf", "Minion"}
    const.USE_VOTING = True
    const.USE_REG_WOLF = False
    const.USE_EXPECTIMAX_WOLF = False
    random.seed(0)


@pytest.fixture
def small_game_roles() -> Tuple[str, ...]:
    const.ROLES = ("Villager", "Seer", "Robber")
    const.ROLE_SET = set(const.ROLES)
    const.ROLE_COUNTS = dict(Counter(const.ROLES))
    const.NUM_ROLES = len(const.ROLES)
    const.NUM_PLAYERS = 3
    const.NUM_CENTER = 0
    const.VILLAGE_ROLES &= const.ROLE_SET
    const.EVIL_ROLES &= const.ROLE_SET
    return const.ROLES


@pytest.fixture
def medium_game_roles() -> Tuple[str, ...]:
    const.ROLES = ("Robber", "Drunk", "Wolf", "Troublemaker", "Seer", "Minion")
    const.ROLE_SET = set(const.ROLES)
    const.ROLE_COUNTS = dict(Counter(const.ROLES))
    const.NUM_ROLES = len(const.ROLES)
    const.NUM_PLAYERS = 5
    const.NUM_CENTER = 1
    const.VILLAGE_ROLES &= const.ROLE_SET
    const.EVIL_ROLES &= const.ROLE_SET
    return const.ROLES


@pytest.fixture
def large_game_roles() -> Tuple[str, ...]:
    const.ROLES = (
        "Wolf",
        "Villager",
        "Robber",
        "Seer",
        "Villager",
        "Tanner",
        "Mason",
        "Wolf",
        "Minion",
        "Mason",
        "Drunk",
        "Villager",
        "Troublemaker",
        "Insomniac",
        "Hunter",
    )
    const.ROLE_SET = set(const.ROLES)
    const.ROLE_COUNTS = dict(Counter(const.ROLES))
    const.NUM_ROLES = len(const.ROLES)
    const.NUM_PLAYERS = 12
    const.NUM_CENTER = 3
    const.VILLAGE_ROLES &= const.ROLE_SET
    const.EVIL_ROLES &= const.ROLE_SET
    return const.ROLES


@pytest.fixture
def standard_game_roles() -> Tuple[str, ...]:
    const.ROLES = (
        "Villager",
        "Villager",
        "Villager",
        "Seer",
        "Wolf",
        "Wolf",
        "Troublemaker",
        "Mason",
        "Mason",
        "Drunk",
    )
    const.ROLE_SET = set(const.ROLES)
    const.ROLE_COUNTS = dict(Counter(const.ROLES))
    const.NUM_ROLES = len(const.ROLES)
    const.NUM_PLAYERS = 7
    const.NUM_CENTER = 3
    const.VILLAGE_ROLES &= const.ROLE_SET
    const.EVIL_ROLES &= const.ROLE_SET
    return const.ROLES


@pytest.fixture
def large_individual_preds() -> List[List[str]]:
    # fmt: off
    return [['Villager', 'Mason', 'Mason', 'Minion', 'Villager', 'Drunk', 'Tanner', 'Troublemaker',
             'Villager', 'Wolf', 'Wolf', 'Hunter', 'Insomniac', 'Seer', 'Robber'],
            ['Villager', 'Insomniac', 'Mason', 'Tanner', 'Villager', 'Drunk', 'Seer', 'Minion',
             'Wolf', 'Villager', 'Wolf', 'Hunter', 'Troublemaker', 'Mason', 'Robber'],
            ['Villager', 'Insomniac', 'Mason', 'Tanner', 'Villager', 'Drunk', 'Seer', 'Wolf',
             'Minion', 'Villager', 'Wolf', 'Hunter', 'Troublemaker', 'Mason', 'Robber'],
            ['Villager', 'Insomniac', 'Mason', 'Wolf', 'Villager', 'Wolf', 'Seer', 'Minion',
             'Robber', 'Villager', 'Tanner', 'Hunter', 'Troublemaker', 'Mason', 'Drunk'],
            ['Villager', 'Insomniac', 'Mason', 'Wolf', 'Villager', 'Drunk', 'Seer', 'Wolf',
             'Tanner', 'Villager', 'Minion', 'Hunter', 'Troublemaker', 'Mason', 'Robber'],
            ['Villager', 'Insomniac', 'Mason', 'Tanner', 'Villager', 'Drunk', 'Minion',
             'Troublemaker', 'Villager', 'Wolf', 'Wolf', 'Hunter', 'Seer', 'Mason', 'Robber'],
            ['Villager', 'Insomniac', 'Mason', 'Wolf', 'Villager', 'Drunk', 'Seer', 'Wolf',
             'Minion', 'Villager', 'Tanner', 'Hunter', 'Troublemaker', 'Mason', 'Robber'],
            ['Villager', 'Mason', 'Mason', 'Wolf', 'Villager', 'Drunk', 'Tanner', 'Troublemaker',
             'Villager', 'Minion', 'Wolf', 'Hunter', 'Insomniac', 'Seer', 'Robber'],
            ['Villager', 'Wolf', 'Mason', 'Minion', 'Villager', 'Tanner', 'Wolf', 'Troublemaker',
             'Villager', 'Seer', 'Mason', 'Robber', 'Hunter', 'Drunk', 'Insomniac'],
            ['Villager', 'Insomniac', 'Mason', 'Tanner', 'Villager', 'Drunk', 'Minion',
             'Troublemaker', 'Villager', 'Wolf', 'Wolf', 'Hunter', 'Mason', 'Seer', 'Robber'],
            ['Villager', 'Troublemaker', 'Mason', 'Wolf', 'Villager', 'Wolf', 'Minion', 'Tanner',
             'Robber', 'Villager', 'Seer', 'Hunter', 'Insomniac', 'Mason', 'Drunk'],
            ['Villager', 'Insomniac', 'Mason', 'Minion', 'Villager', 'Drunk', 'Seer', 'Tanner',
             'Wolf', 'Villager', 'Wolf', 'Hunter', 'Troublemaker', 'Mason', 'Robber']]
    # fmt: on


def debug_spacing_issues(captured: str, expected: str) -> None:
    """ Helper method for debugging print differences. """
    print(len(captured), len(expected))
    for i, captured_char in enumerate(captured):
        if captured_char != expected[i]:
            print("INCORRECT: ", i, captured_char, "vs", expected[i])
        else:
            print(" " * 10, i, captured_char, "vs", expected[i])
