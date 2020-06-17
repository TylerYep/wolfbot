""" gameresults.py """
# pylint: skip-file
from typing import Tuple

import pytest

from src.stats import GameResult


@pytest.fixture
def example_small_game_result(small_game_roles: Tuple[str, ...]) -> GameResult:
    return GameResult(["Villager", "Seer", "Robber"], ["Villager", "Seer", "Robber"], [], "Village")


@pytest.fixture
def example_medium_game_result(medium_game_roles: Tuple[str, ...]) -> GameResult:
    return GameResult(
        ["Seer", "Wolf", "Troublemaker", "Drunk", "Minion", "Robber"],
        ["Seer", "Wolf", "Troublemaker", "Drunk", "Minion", "Robber"],
        [1],
        "Village",
    )


@pytest.fixture
def example_large_game_result(large_game_roles: Tuple[str, ...]) -> GameResult:
    return GameResult(
        [
            "Villager",
            "Insomniac",
            "Mason",
            "Tanner",
            "Villager",
            "Drunk",
            "Seer",
            "Wolf",
            "Minion",
            "Villager",
            "Wolf",
            "Hunter",
            "Troublemaker",
            "Mason",
            "Robber",
        ],
        [
            "Villager",
            "Insomniac",
            "Mason",
            "Minion",
            "Villager",
            "Drunk",
            "Seer",
            "Tanner",
            "Wolf",
            "Villager",
            "Wolf",
            "Hunter",
            "Troublemaker",
            "Mason",
            "Robber",
        ],
        [7, 10],
        "Werewolf",
    )
