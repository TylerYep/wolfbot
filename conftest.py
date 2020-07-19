""" conftest.py """
# pylint: skip-file
import csv
import os
import random
from typing import Callable, Dict, List, Tuple

import pytest
from _pytest.logging import LogCaptureFixture

from fixtures import *
from src import const
from src.roles import Drunk, Hunter, Insomniac, Mason, Robber, Seer, Troublemaker, Villager


def set_roles(roles: Tuple[str, ...]) -> None:
    """ Changes to ROLES should propagate to all of its descendants. """
    const.ROLES = roles  # type: ignore
    const.ROLE_SET = frozenset(const.ROLES)
    const.SORTED_ROLE_SET = sorted(const.ROLE_SET)
    const.ROLE_COUNTS = const.get_counts(const.ROLES)
    const.NUM_ROLES = len(const.ROLES)
    const.VILLAGE_ROLES &= const.ROLE_SET
    const.EVIL_ROLES &= const.ROLE_SET
    const.IS_USER = [False] * const.NUM_ROLES


@pytest.fixture(autouse=True)
def reset_const() -> None:
    const.logger.set_level(0)
    const.NUM_PLAYERS = 12
    const.NUM_CENTER = 3
    const.VILLAGE_ROLES = frozenset(
        {"Villager", "Mason", "Seer", "Robber", "Troublemaker", "Drunk", "Insomniac", "Hunter"}
    )
    const.EVIL_ROLES = frozenset({"Tanner", "Wolf", "Minion"})

    # Game Modes
    const.RANDOMIZE_ROLES = True
    const.MULTI_STATEMENT = False
    const.INTERACTIVE_MODE = False

    # Player Settings
    const.CENTER_SEER_PROB = 0.9
    const.SMART_VILLAGERS = True
    const.USE_REG_WOLF = False
    const.EXPECTIMAX_WOLF = False
    const.EXPECTIMAX_MINION = False
    const.EXPECTIMAX_TANNER = False

    const.REPLAY_FILE = "unit_test/test_data/replay.json"
    random.seed(0)
    set_roles(
        (
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
    )
    Drunk.get_all_statements.cache_clear()
    Seer.get_all_statements.cache_clear()
    Robber.get_all_statements.cache_clear()

    Drunk.get_drunk_statements.cache_clear()
    Seer.get_seer_statements.cache_clear()
    Robber.get_robber_statements.cache_clear()


@pytest.fixture
def small_game_roles() -> Tuple[str, ...]:
    const.NUM_PLAYERS = 3
    const.NUM_CENTER = 0
    set_roles(("Villager", "Seer", "Robber"))
    return const.ROLES


@pytest.fixture
def medium_game_roles() -> Tuple[str, ...]:
    const.NUM_PLAYERS = 5
    const.NUM_CENTER = 1
    set_roles(("Robber", "Drunk", "Wolf", "Troublemaker", "Seer", "Minion"))
    return const.ROLES


@pytest.fixture
def large_game_roles() -> Tuple[str, ...]:
    const.NUM_PLAYERS = 12
    const.NUM_CENTER = 3
    set_roles(
        (
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
    )
    return const.ROLES


@pytest.fixture
def standard_game_roles() -> Tuple[str, ...]:
    const.NUM_PLAYERS = 7
    const.NUM_CENTER = 3
    set_roles(
        (
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
    )
    return const.ROLES


@pytest.fixture
def large_individual_preds() -> List[Tuple[str, ...]]:
    # fmt: off
    return [('Villager', 'Mason', 'Mason', 'Minion', 'Villager', 'Drunk', 'Tanner', 'Troublemaker',
             'Villager', 'Wolf', 'Wolf', 'Hunter', 'Insomniac', 'Seer', 'Robber'),
            ('Villager', 'Insomniac', 'Mason', 'Tanner', 'Villager', 'Drunk', 'Seer', 'Minion',
             'Wolf', 'Villager', 'Wolf', 'Hunter', 'Troublemaker', 'Mason', 'Robber'),
            ('Villager', 'Insomniac', 'Mason', 'Tanner', 'Villager', 'Drunk', 'Seer', 'Wolf',
             'Minion', 'Villager', 'Wolf', 'Hunter', 'Troublemaker', 'Mason', 'Robber'),
            ('Villager', 'Insomniac', 'Mason', 'Wolf', 'Villager', 'Wolf', 'Seer', 'Minion',
             'Robber', 'Villager', 'Tanner', 'Hunter', 'Troublemaker', 'Mason', 'Drunk'),
            ('Villager', 'Insomniac', 'Mason', 'Wolf', 'Villager', 'Drunk', 'Seer', 'Wolf',
             'Tanner', 'Villager', 'Minion', 'Hunter', 'Troublemaker', 'Mason', 'Robber'),
            ('Villager', 'Insomniac', 'Mason', 'Tanner', 'Villager', 'Drunk', 'Minion',
             'Troublemaker', 'Villager', 'Wolf', 'Wolf', 'Hunter', 'Seer', 'Mason', 'Robber'),
            ('Villager', 'Insomniac', 'Mason', 'Wolf', 'Villager', 'Drunk', 'Seer', 'Wolf',
             'Minion', 'Villager', 'Tanner', 'Hunter', 'Troublemaker', 'Mason', 'Robber'),
            ('Villager', 'Mason', 'Mason', 'Wolf', 'Villager', 'Drunk', 'Tanner', 'Troublemaker',
             'Villager', 'Minion', 'Wolf', 'Hunter', 'Insomniac', 'Seer', 'Robber'),
            ('Villager', 'Wolf', 'Mason', 'Minion', 'Villager', 'Tanner', 'Wolf', 'Troublemaker',
             'Villager', 'Seer', 'Mason', 'Robber', 'Hunter', 'Drunk', 'Insomniac'),
            ('Villager', 'Insomniac', 'Mason', 'Tanner', 'Villager', 'Drunk', 'Minion',
             'Troublemaker', 'Villager', 'Wolf', 'Wolf', 'Hunter', 'Mason', 'Seer', 'Robber'),
            ('Villager', 'Troublemaker', 'Mason', 'Wolf', 'Villager', 'Wolf', 'Minion', 'Tanner',
             'Robber', 'Villager', 'Seer', 'Hunter', 'Insomniac', 'Mason', 'Drunk'),
            ('Villager', 'Insomniac', 'Mason', 'Minion', 'Villager', 'Drunk', 'Seer', 'Tanner',
             'Wolf', 'Villager', 'Wolf', 'Hunter', 'Troublemaker', 'Mason', 'Robber')]
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


def write_results(stat_results: Dict[str, float], file_path: str) -> None:
    """ Writes stat_results to corresponding csv file. """
    sub_folder, filename = os.path.split(file_path)
    destination = os.path.join("integration_test", "results", sub_folder)
    if not os.path.isdir(destination):
        os.makedirs(destination)

    results_filename = os.path.join(destination, filename)
    with open(results_filename, "a+") as out_file:
        writer = csv.DictWriter(out_file, fieldnames=stat_results.keys())
        if os.path.getsize(results_filename) == 0:
            writer.writeheader()
        writer.writerow(stat_results)


def verify_output_file(caplog: LogCaptureFixture, filename: str) -> None:
    """ Helper method for debugging print differences using a file. """
    with open(filename) as output_file:
        expected = output_file.read().split("\n")
    verify_output(caplog, expected)


def verify_output(caplog: LogCaptureFixture, expected: List[str]) -> None:
    """ Helper method for debugging print differences. """
    captured = list(map(lambda x: x.getMessage(), caplog.records))  # type: ignore
    assert "\n".join(captured) == "\n".join(expected)


def verify_output_string(caplog: LogCaptureFixture, expected: str) -> None:
    """ Helper method for debugging print differences. """
    assert caplog.records[0].getMessage() == expected
