""" savedgames.py """
from typing import Tuple

import pytest

from src import const
from src.const import SwitchPriority
from src.roles import Drunk, Hunter, Mason, Minion, Robber, Seer, Tanner, Villager, Wolf
from src.statements import Statement
from src.stats import SavedGame


@pytest.fixture
def example_small_saved_game(small_game_roles: Tuple[str, ...]) -> SavedGame:
    return SavedGame(
        ("Villager", "Robber", "Seer"),
        ["Villager", "Seer", "Robber"],
        [
            Statement("I am a Villager.", ((0, frozenset({"Villager"})),)),
            Statement(
                "I am a Robber and I swapped with Player 2. I am now a Seer.",
                ((1, frozenset({"Robber"})), (2, frozenset({"Seer"})),),
                ((SwitchPriority.ROBBER, 1, 2),),
            ),
            Statement(
                "I am a Seer and I saw that Player 1 was a Robber.",
                ((2, frozenset({"Seer"})), (1, frozenset({"Robber"})),),
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
                ((0, frozenset({"Seer"})), (2, frozenset({"Drunk"})),),
            ),
            Statement(
                "I am a Robber and I swapped with Player 0. I am now a Seer.",
                ((1, frozenset({"Robber"})), (0, frozenset({"Seer"})),),
                ((SwitchPriority.ROBBER, 1, 0),),
            ),
            Statement(
                "I am a Drunk and I swapped with Center 0.",
                ((2, frozenset({"Drunk"})),),
                ((SwitchPriority.DRUNK, 2, 5),),
            ),
            Statement(
                "I am a Robber and I swapped with Player 2. I am now a Drunk.",
                ((3, frozenset({"Robber"})), (2, frozenset({"Drunk"})),),
                ((SwitchPriority.ROBBER, 3, 2),),
            ),
            Statement(
                "I am a Seer and I saw that Player 3 was a Robber.",
                ((4, frozenset({"Seer"})), (3, frozenset({"Robber"})),),
            ),
        ],
        [
            Seer(0, (2, "Drunk")),
            Wolf(1, [1], 5, "Troublemaker"),
            Drunk(2, 5),
            Robber(3, 2, "Drunk"),
            Minion(4, [1]),
        ],
    )


@pytest.fixture
def example_large_saved_game(large_game_roles: Tuple[str, ...]) -> SavedGame:
    mason_roles = tuple(
        [(i, const.ROLE_SET - frozenset({"Mason"})) for i in range(const.NUM_PLAYERS) if i != 2]
    )
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
            Statement("I am a Villager.", ((0, frozenset({"Villager"})),)),
            Statement(
                "I am a Drunk and I swapped with Center 2.",
                ((1, frozenset({"Drunk"})),),
                ((SwitchPriority.DRUNK, 1, 14),),
            ),
            Statement(
                "I am a Mason. The other Mason is not present.",
                ((2, frozenset({"Mason"})),) + mason_roles,
            ),
            Statement(
                "I am a Robber and I swapped with Player 10. I am now a Insomniac.",
                ((3, frozenset({"Robber"})), (10, frozenset({"Insomniac"})),),
                ((SwitchPriority.ROBBER, 3, 10),),
            ),
            Statement("I am a Villager.", ((4, frozenset({"Villager"})),)),
            Statement(
                "I am a Robber and I swapped with Player 1. I am now a Drunk.",
                ((5, frozenset({"Robber"})), (1, frozenset({"Drunk"})),),
                ((SwitchPriority.ROBBER, 5, 1),),
            ),
            Statement(
                (
                    "I am a Seer and I saw that Center 1 was a Mason and that "
                    "Center 0 was a Troublemaker."
                ),
                (
                    (6, frozenset({"Seer"})),
                    (13, frozenset({"Mason"})),
                    (12, frozenset({"Troublemaker"})),
                ),
            ),
            Statement(
                "I am a Seer and I saw that Player 3 was a Robber.",
                ((7, frozenset({"Seer"})), (3, frozenset({"Robber"})),),
            ),
            Statement(
                "I am a Troublemaker and I swapped Player 0 and Player 1.",
                ((8, frozenset({"Troublemaker"})),),
                ((SwitchPriority.TROUBLEMAKER, 0, 1),),
            ),
            Statement("I am a Villager.", ((9, frozenset({"Villager"})),)),
            Statement(
                "I am a Troublemaker and I swapped Player 3 and Player 4.",
                ((10, frozenset({"Troublemaker"})),),
                ((SwitchPriority.TROUBLEMAKER, 3, 4),),
            ),
            Statement("I am a Hunter.", ((11, frozenset({"Hunter"})),)),
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
