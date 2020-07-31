""" gameresults.py """
# pylint: disable=missing-function-docstring
from typing import Tuple

import pytest

from src.const import Role
from src.stats import GameResult


@pytest.fixture
def example_small_game_result(small_game_roles: Tuple[Role, ...]) -> GameResult:
    return GameResult(
        (Role.VILLAGER, Role.SEER, Role.ROBBER),
        (Role.VILLAGER, Role.SEER, Role.ROBBER),
        (),
        "Village",
    )


@pytest.fixture
def example_medium_game_result(medium_game_roles: Tuple[Role, ...]) -> GameResult:
    return GameResult(
        (Role.SEER, Role.WOLF, Role.TROUBLEMAKER, Role.DRUNK, Role.MINION, Role.ROBBER),
        (Role.SEER, Role.MINION, Role.TROUBLEMAKER, Role.DRUNK, Role.WOLF, Role.ROBBER),
        (1,),
        "Werewolf",
    )


@pytest.fixture
def example_large_game_result(large_game_roles: Tuple[Role, ...]) -> GameResult:
    return GameResult(
        (
            Role.VILLAGER,
            Role.INSOMNIAC,
            Role.MASON,
            Role.TANNER,
            Role.VILLAGER,
            Role.DRUNK,
            Role.SEER,
            Role.WOLF,
            Role.MINION,
            Role.VILLAGER,
            Role.WOLF,
            Role.HUNTER,
            Role.TROUBLEMAKER,
            Role.MASON,
            Role.ROBBER,
        ),
        (
            Role.VILLAGER,
            Role.MASON,
            Role.MASON,
            Role.MINION,
            Role.VILLAGER,
            Role.DRUNK,
            Role.WOLF,
            Role.WOLF,
            Role.SEER,
            Role.VILLAGER,
            Role.TANNER,
            Role.HUNTER,
            Role.INSOMNIAC,
            Role.TROUBLEMAKER,
            Role.ROBBER,
        ),
        (7, 10),
        "Village",
    )
