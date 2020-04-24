""" gameresults.py """
from typing import Tuple

import pytest

from src.stats import GameResult


@pytest.fixture
def example_small_game_result(small_game_roles: Tuple[str, ...]) -> GameResult:
    return GameResult(
        ["Villager", "Seer", "Robber"], ["Villager", "Seer", "Robber"], [], "Villager"
    )


@pytest.fixture
def example_medium_game_result(medium_game_roles: Tuple[str, ...]) -> GameResult:
    return GameResult(
        ["Seer", "Wolf", "Troublemaker", "Drunk", "Minion", "Robber"],
        ["Seer", "Wolf", "Troublemaker", "Drunk", "Minion", "Robber"],
        [1],
        "Villager",
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
            "Mason",
            "Mason",
            "Minion",
            "Villager",
            "Drunk",
            "Tanner",
            "Troublemaker",
            "Villager",
            "Wolf",
            "Wolf",
            "Hunter",
            "Insomniac",
            "Seer",
            "Robber",
        ],
        [7, 10],
        "Villager",
    )
