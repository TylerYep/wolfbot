""" conftest.py """
import csv
import os
import random
from collections import Counter
from typing import Callable, Dict, FrozenSet, List, Set, Tuple

import pytest
from _pytest.logging import LogCaptureFixture

from fixtures import *
from src import const


def reset_misc_const_fields() -> None:
    """ Changes to ROLES should propagate to all of its descendants. """
    const.ROLE_SET = frozenset(const.ROLES)
    const.SORTED_ROLE_SET = sorted(const.ROLE_SET)
    const.ROLE_COUNTS = dict(Counter(const.ROLES))
    const.NUM_ROLES = len(const.ROLES)
    const.VILLAGE_ROLES &= const.ROLE_SET
    const.EVIL_ROLES &= const.ROLE_SET
    const.IS_USER = [False] * const.NUM_ROLES


@pytest.fixture(autouse=True)
def reset_const() -> None:
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
    const.NUM_PLAYERS = 12
    const.NUM_CENTER = 3
    const.CENTER_SEER_PROB = 0.9
    const.SMART_VILLAGERS = True
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
    const.EXPECTIMAX_PLAYER = False
    const.RANDOMIZE_ROLES = True
    const.MULTI_STATEMENT = False
    const.INTERACTIVE_MODE_ON = False
    const.REPLAY_FILE = "unit_test/test_data/replay.json"
    random.seed(0)
    reset_misc_const_fields()


@pytest.fixture
def small_game_roles() -> Tuple[str, ...]:
    const.ROLES = ("Villager", "Seer", "Robber")  # type: ignore
    const.NUM_PLAYERS = 3
    const.NUM_CENTER = 0
    reset_misc_const_fields()
    return const.ROLES


@pytest.fixture
def medium_game_roles() -> Tuple[str, ...]:
    const.ROLES = ("Robber", "Drunk", "Wolf", "Troublemaker", "Seer", "Minion")  # type: ignore
    const.NUM_PLAYERS = 5
    const.NUM_CENTER = 1
    reset_misc_const_fields()
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
    const.NUM_PLAYERS = 12
    const.NUM_CENTER = 3
    reset_misc_const_fields()
    return const.ROLES


@pytest.fixture
def standard_game_roles() -> Tuple[str, ...]:
    const.ROLES = (
        "Villager",  # type: ignore
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
    const.NUM_PLAYERS = 7
    const.NUM_CENTER = 3
    reset_misc_const_fields()
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


def override_input(inputs: List[str]) -> Callable[[str], str]:
    """
    Returns a new input() function that accepts a string and repeatedly pops strings from
    the front the provided list and returns them as calls to input().
    """
    inputs = list(map(str, inputs))

    def _input(prompt: str) -> str:
        """ The new input() function. Prints a prompt and then modifies the provided list. """
        print(prompt)
        if not inputs:
            raise RuntimeError("Not enough inputs provided.")
        return inputs.pop(0)

    return _input


def write_results(filename: str, stat_results: Dict[str, float]) -> None:
    """ Writes stat_results to corresponding csv file. """
    results_filename = os.path.join("integration_test/results/", filename)
    with open(results_filename, "a+") as out_file:
        writer = csv.DictWriter(out_file, fieldnames=stat_results.keys())
        if os.path.getsize(results_filename) == 0:
            writer.writeheader()
        writer.writerow(stat_results)


def verify_output(caplog: LogCaptureFixture, filename: str) -> None:
    """ Helper method for debugging print differences. """
    captured = list(map(lambda x: x.getMessage(), caplog.records))  # type: ignore
    with open(filename) as output_file:
        expected = output_file.read().split("\n")
    assert "\n".join(captured) == "\n".join(expected)


def debug_spacing_issues(captured: str, expected: str) -> None:
    """ Helper method for debugging print differences. """
    print(len(captured), len(expected))
    for i, captured_char in enumerate(captured):
        if captured_char != expected[i]:
            print("INCORRECT: ", i, captured_char, "vs", expected[i])
        else:
            print(" " * 10, i, captured_char, "vs", expected[i])
