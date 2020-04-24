""" savedgames.py """
from typing import Tuple

import pytest

from src import const
from src.const import Priority
from src.roles import Drunk, Hunter, Mason, Minion, Robber, Seer, Tanner, Villager, Wolf
from src.statements import Statement
from src.stats import SavedGame


@pytest.fixture
def example_small_saved_game(small_game_roles: Tuple[str, ...]) -> SavedGame:
    return SavedGame(
        ("Villager", "Robber", "Seer"),
        ["Villager", "Seer", "Robber"],
        [
            Statement("I am a Villager.", [(0, {"Villager"})], [], "Villager"),
            Statement(
                "I am a Robber and I swapped with Player 2. I am now a Seer.",
                [(1, {"Robber"}), (2, {"Seer"})],
                [(Priority.ROBBER, 1, 2)],
                "Robber",
            ),
            Statement(
                "I am a Seer and I saw that Player 1 was a Robber.",
                [(2, {"Seer"}), (1, {"Robber"})],
                [],
                "Seer",
            ),
        ],
        [Villager(0), Robber(1, 2, "Seer"), Seer(2, (1, "Robber"), (None, None))],
    )


@pytest.fixture
def example_medium_saved_game(medium_game_roles: Tuple[str, ...]) -> SavedGame:
    return SavedGame(
        ("Seer", "Wolf", "Drunk", "Robber", "Minion", "Troublemaker"),
        ["Seer", "Wolf", "Troublemaker", "Drunk", "Minion", "Robber"],
        [
            Statement(
                "I am a Seer and I saw that Player 2 was a Drunk.",
                [(0, {"Seer"}), (2, {"Drunk"})],
                [],
                "Seer",
            ),
            Statement(
                "I am a Robber and I swapped with Player 0. I am now a Seer.",
                [(1, {"Robber"}), (0, {"Seer"})],
                [(Priority.ROBBER, 1, 0)],
                "Robber",
            ),
            Statement(
                "I am a Drunk and I swapped with Center 0.",
                [(2, {"Drunk"})],
                [(Priority.DRUNK, 2, 5)],
                "Drunk",
            ),
            Statement(
                "I am a Robber and I swapped with Player 2. I am now a Drunk.",
                [(3, {"Robber"}), (2, {"Drunk"})],
                [(Priority.ROBBER, 3, 2)],
                "Robber",
            ),
            Statement(
                "I am a Seer and I saw that Player 3 was a Robber.",
                [(4, {"Seer"}), (3, {"Robber"})],
                [],
                "Seer",
            ),
        ],
        [
            Seer(0, (2, "Drunk"), (None, None)),
            Wolf(1, [1], 5, "Troublemaker"),
            Drunk(2, 5),
            Robber(3, 2, "Drunk"),
            Minion(4, [1]),
        ],
    )


@pytest.fixture
def example_large_saved_game(large_game_roles: Tuple[str, ...]) -> SavedGame:
    mason_roles = [(i, const.ROLE_SET - {"Mason"}) for i in range(const.NUM_PLAYERS) if i != 2]
    return SavedGame(
        (
            "Villager",
            "Drunk",
            "Mason",
            "Tanner",
            "Villager",
            "Robber",
            "Seer",
            "Wolf",
            "Minion",
            "Villager",
            "Wolf",
            "Hunter",
            "Troublemaker",
            "Mason",
            "Insomniac",
        ),
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
            Statement("I am a Villager.", [(0, {"Villager"})], [], "Villager"),
            Statement(
                "I am a Drunk and I swapped with Center 2.",
                [(1, {"Drunk"})],
                [(Priority.DRUNK, 1, 14)],
                "Drunk",
            ),
            Statement(
                "I am a Mason. The other Mason is not present.",
                [(2, {"Mason"})] + mason_roles,
                [],
                "Mason",
            ),
            Statement(
                "I am a Robber and I swapped with Player 10. I am now a Insomniac.",
                [(3, {"Robber"}), (10, {"Insomniac"})],
                [(Priority.ROBBER, 3, 10)],
                "Robber",
            ),
            Statement("I am a Villager.", [(4, {"Villager"})], [], "Villager"),
            Statement(
                "I am a Robber and I swapped with Player 1. I am now a Drunk.",
                [(5, {"Robber"}), (1, {"Drunk"})],
                [(Priority.ROBBER, 5, 1)],
                "Robber",
            ),
            Statement(
                (
                    "I am a Seer and I saw that Center 1 was a Mason and that "
                    "Center 0 was a Troublemaker."
                ),
                [(6, {"Seer"}), (13, {"Mason"}), (12, {"Troublemaker"})],
                [],
                "Seer",
            ),
            Statement(
                "I am a Seer and I saw that Player 3 was a Robber.",
                [(7, {"Seer"}), (3, {"Robber"})],
                [],
                "Seer",
            ),
            Statement(
                "I am a Troublemaker and I swapped Player 0 and Player 1.",
                [(8, {"Troublemaker"})],
                [(Priority.TROUBLEMAKER, 0, 1)],
                "Troublemaker",
            ),
            Statement("I am a Villager.", [(9, {"Villager"})], [], "Villager"),
            Statement(
                "I am a Troublemaker and I swapped Player 3 and Player 4.",
                [(10, {"Troublemaker"})],
                [(Priority.TROUBLEMAKER, 3, 4)],
                "Troublemaker",
            ),
            Statement("I am a Hunter.", [(11, {"Hunter"})], [], "Hunter"),
        ],
        [
            Villager(0),
            Drunk(1, 14),
            Mason(2, [2]),
            Tanner(3),
            Villager(4),
            Robber(5, 1, "Drunk"),
            Seer(6, (13, "Mason"), (12, "Troublemaker")),
            Wolf(7, [7, 10], None, None),
            Minion(8, [7, 10]),
            Villager(9),
            Wolf(10, [7, 10], None, None),
            Hunter(11),
        ],
    )
