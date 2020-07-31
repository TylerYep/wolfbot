""" conftest.py """
# pylint: disable=missing-function-docstring, unused-import
import csv
import os
import random
from typing import Callable, Dict, List, Tuple

import pytest
from _pytest.logging import LogCaptureFixture

from fixtures import (
    example_large_game_result,
    example_large_saved_game,
    example_large_solverstate,
    example_medium_game_result,
    example_medium_saved_game,
    example_medium_solved_list,
    example_medium_solverstate,
    example_medium_solverstate_list,
    example_medium_solverstate_solved,
    example_small_game_result,
    example_small_saved_game,
    example_small_solverstate,
    example_small_solverstate_solved,
    example_statement,
    large_knowledge_base,
    large_statement_list,
    medium_knowledge_base,
    medium_statement_list,
    small_knowledge_base,
    small_statement_list,
)
from src import const
from src.const import Role


def set_roles(*roles: Role) -> None:
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
    const.EVIL_ROLES = frozenset({Role.TANNER, Role.WOLF, Role.MINION})

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
        Role.INSOMNIAC,
        Role.VILLAGER,
        Role.ROBBER,
        Role.VILLAGER,
        Role.DRUNK,
        Role.WOLF,
        Role.WOLF,
        Role.SEER,
        Role.TANNER,
        Role.MASON,
        Role.MINION,
        Role.TROUBLEMAKER,
        Role.VILLAGER,
        Role.MASON,
        Role.HUNTER,
    )

    for cached_function in const.CACHED_FUNCTIONS:
        cached_function.cache_clear()


@pytest.fixture
def small_game_roles() -> Tuple[Role, ...]:
    const.NUM_PLAYERS = 3
    const.NUM_CENTER = 0
    set_roles(Role.VILLAGER, Role.SEER, Role.ROBBER)
    return const.ROLES


@pytest.fixture
def medium_game_roles() -> Tuple[Role, ...]:
    const.NUM_PLAYERS = 5
    const.NUM_CENTER = 1
    set_roles(Role.ROBBER, Role.DRUNK, Role.WOLF, Role.TROUBLEMAKER, Role.SEER, Role.MINION)
    return const.ROLES


@pytest.fixture
def large_game_roles() -> Tuple[Role, ...]:
    const.NUM_PLAYERS = 12
    const.NUM_CENTER = 3
    set_roles(
        Role.WOLF,
        Role.VILLAGER,
        Role.ROBBER,
        Role.SEER,
        Role.VILLAGER,
        Role.TANNER,
        Role.MASON,
        Role.WOLF,
        Role.MINION,
        Role.MASON,
        Role.DRUNK,
        Role.VILLAGER,
        Role.TROUBLEMAKER,
        Role.INSOMNIAC,
        Role.HUNTER,
    )
    return const.ROLES


@pytest.fixture
def standard_game_roles() -> Tuple[Role, ...]:
    const.NUM_PLAYERS = 7
    const.NUM_CENTER = 3
    set_roles(
        Role.VILLAGER,
        Role.VILLAGER,
        Role.VILLAGER,
        Role.SEER,
        Role.WOLF,
        Role.WOLF,
        Role.TROUBLEMAKER,
        Role.MASON,
        Role.MASON,
        Role.DRUNK,
    )
    return const.ROLES


@pytest.fixture(scope="session")
def large_individual_preds() -> Tuple[Tuple[Role, ...], ...]:
    # fmt: off
    return (
        (Role.VILLAGER, Role.MASON, Role.MASON, Role.MINION, Role.VILLAGER, Role.DRUNK,
            Role.TANNER, Role.TROUBLEMAKER, Role.VILLAGER, Role.WOLF, Role.WOLF,
            Role.HUNTER, Role.INSOMNIAC, Role.SEER, Role.ROBBER),
        (Role.VILLAGER, Role.INSOMNIAC, Role.MASON, Role.TANNER, Role.VILLAGER, Role.DRUNK,
            Role.SEER, Role.MINION, Role.WOLF, Role.VILLAGER, Role.WOLF, Role.HUNTER,
            Role.TROUBLEMAKER, Role.MASON, Role.ROBBER),
        (Role.VILLAGER, Role.INSOMNIAC, Role.MASON, Role.TANNER, Role.VILLAGER, Role.DRUNK,
            Role.SEER, Role.WOLF, Role.MINION, Role.VILLAGER, Role.WOLF, Role.HUNTER,
            Role.TROUBLEMAKER, Role.MASON, Role.ROBBER),
        (Role.VILLAGER, Role.INSOMNIAC, Role.MASON, Role.WOLF, Role.VILLAGER, Role.WOLF,
            Role.SEER, Role.MINION, Role.ROBBER, Role.VILLAGER, Role.TANNER, Role.HUNTER,
            Role.TROUBLEMAKER, Role.MASON, Role.DRUNK),
        (Role.VILLAGER, Role.INSOMNIAC, Role.MASON, Role.WOLF, Role.VILLAGER, Role.DRUNK,
            Role.SEER, Role.WOLF, Role.TANNER, Role.VILLAGER, Role.MINION, Role.HUNTER,
            Role.TROUBLEMAKER, Role.MASON, Role.ROBBER),
        (Role.VILLAGER, Role.INSOMNIAC, Role.MASON, Role.TANNER, Role.VILLAGER, Role.DRUNK,
            Role.MINION, Role.TROUBLEMAKER, Role.VILLAGER, Role.WOLF, Role.WOLF, Role.HUNTER,
            Role.SEER, Role.MASON, Role.ROBBER),
        (Role.VILLAGER, Role.INSOMNIAC, Role.MASON, Role.WOLF, Role.VILLAGER, Role.DRUNK,
            Role.SEER, Role.WOLF, Role.MINION, Role.VILLAGER, Role.TANNER, Role.HUNTER,
            Role.TROUBLEMAKER, Role.MASON, Role.ROBBER),
        (Role.VILLAGER, Role.MASON, Role.MASON, Role.WOLF, Role.VILLAGER, Role.DRUNK,
            Role.TANNER, Role.TROUBLEMAKER, Role.VILLAGER, Role.MINION, Role.WOLF,
            Role.HUNTER, Role.INSOMNIAC, Role.SEER, Role.ROBBER),
        (Role.VILLAGER, Role.WOLF, Role.MASON, Role.MINION, Role.VILLAGER, Role.TANNER,
            Role.WOLF, Role.TROUBLEMAKER, Role.VILLAGER, Role.SEER, Role.MASON,
            Role.ROBBER, Role.HUNTER, Role.DRUNK, Role.INSOMNIAC),
        (Role.VILLAGER, Role.INSOMNIAC, Role.MASON, Role.TANNER, Role.VILLAGER, Role.DRUNK,
            Role.MINION, Role.TROUBLEMAKER, Role.VILLAGER, Role.WOLF, Role.WOLF, Role.HUNTER,
            Role.MASON, Role.SEER, Role.ROBBER),
        (Role.VILLAGER, Role.TROUBLEMAKER, Role.MASON, Role.WOLF, Role.VILLAGER, Role.WOLF,
            Role.MINION, Role.TANNER, Role.ROBBER, Role.VILLAGER, Role.SEER, Role.HUNTER,
            Role.INSOMNIAC, Role.MASON, Role.DRUNK),
        (Role.VILLAGER, Role.INSOMNIAC, Role.MASON, Role.MINION, Role.VILLAGER, Role.DRUNK,
            Role.SEER, Role.TANNER, Role.WOLF, Role.VILLAGER, Role.WOLF, Role.HUNTER,
            Role.TROUBLEMAKER, Role.MASON, Role.ROBBER)
    )
    # fmt: on


def override_input(inputs: List[str]) -> Callable[[str], str]:
    """
    Returns a new input() function that accepts a string and repeatedly pops strings from
    the front the provided list and returns them as calls to input().
    """

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
        expected = tuple(output_file.read().split("\n"))
    verify_output(caplog, expected)


def verify_output(caplog: LogCaptureFixture, expected: Tuple[str, ...]) -> None:
    """ Helper method for debugging print differences. """
    captured = list(map(lambda x: x.getMessage(), caplog.records))
    assert "\n".join(captured) == "\n".join(expected)


def verify_output_string(caplog: LogCaptureFixture, expected: str) -> None:
    """ Helper method for debugging print differences. """
    assert caplog.records[0].getMessage() == expected
