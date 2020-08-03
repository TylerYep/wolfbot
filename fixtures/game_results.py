""" gameresults.py """
# pylint: disable=missing-function-docstring
from typing import Tuple

import pytest

from src.const import Role, SwitchPriority, Team
from src.statements import Statement
from src.stats import GameResult


@pytest.fixture
def example_small_game_result(small_game_roles: Tuple[Role, ...]) -> GameResult:
    return GameResult(
        (Role.VILLAGER, Role.ROBBER, Role.SEER),
        (Role.VILLAGER, Role.ROBBER, Role.SEER),
        (),
        Team.VILLAGE,
        (
            Statement("I am a Villager.", ((0, frozenset({Role.VILLAGER})),)),
            Statement(
                "I am a Seer and I saw that Player 2 was a Robber.",
                ((1, frozenset({Role.SEER})), (2, frozenset({Role.ROBBER}))),
            ),
            Statement(
                "I am a Robber and I swapped with Player 1. I am now a Seer.",
                ((2, frozenset({Role.ROBBER})), (1, frozenset({Role.SEER}))),
                ((SwitchPriority.ROBBER, 2, 1),),
            ),
        ),
    )


@pytest.fixture
def example_medium_game_result(medium_game_roles: Tuple[Role, ...]) -> GameResult:
    return GameResult(
        (Role.SEER, Role.MINION, Role.WOLF, Role.TROUBLEMAKER, Role.DRUNK, Role.ROBBER),
        (Role.SEER, Role.MINION, Role.WOLF, Role.TROUBLEMAKER, Role.DRUNK, Role.ROBBER),
        (2,),
        Team.VILLAGE,
        (
            Statement(
                "I am a Robber and I swapped with Player 4. I am now a Seer.",
                ((0, frozenset({Role.ROBBER})), (4, frozenset({Role.SEER})),),
                ((SwitchPriority.ROBBER, 0, 4),),
            ),
            Statement(
                "I am a Drunk and I swapped with Center 0.",
                ((1, frozenset({Role.DRUNK})),),
                ((SwitchPriority.DRUNK, 1, 5),),
            ),
            Statement(
                "I am a Seer and I saw that Player 4 was a Wolf.",
                ((2, frozenset({Role.SEER})), (4, frozenset({Role.WOLF})),),
            ),
            Statement(
                "I am a Troublemaker and I swapped Player 4 and Player 1.",
                ((3, frozenset({Role.TROUBLEMAKER})),),
                ((SwitchPriority.TROUBLEMAKER, 4, 1),),
            ),
            Statement(
                "I am a Seer and I saw that Player 3 was a Troublemaker.",
                ((4, frozenset({Role.SEER})), (3, frozenset({Role.TROUBLEMAKER})),),
            ),
        ),
    )


@pytest.fixture
def example_large_game_result(large_game_roles: Tuple[Role, ...]) -> GameResult:
    return GameResult(
        (
            Role.WOLF,
            Role.VILLAGER,
            Role.WOLF,
            Role.SEER,
            Role.VILLAGER,
            Role.TANNER,
            Role.MASON,
            Role.ROBBER,
            Role.MINION,
            Role.MASON,
            Role.INSOMNIAC,
            Role.VILLAGER,
            Role.TROUBLEMAKER,
            Role.DRUNK,
            Role.HUNTER,
        ),
        (
            Role.TANNER,
            Role.VILLAGER,
            Role.WOLF,
            Role.SEER,
            Role.VILLAGER,
            Role.WOLF,
            Role.MASON,
            Role.ROBBER,
            Role.MINION,
            Role.MASON,
            Role.INSOMNIAC,
            Role.VILLAGER,
            Role.TROUBLEMAKER,
            Role.DRUNK,
            Role.HUNTER,
        ),
        (0, 7),
        Team.TANNER,
        (
            Statement(
                "I am a Seer and I saw that Center 0 was a Insomniac"
                " and that Center 2 was a Minion.",
                (
                    (0, frozenset({Role.SEER})),
                    (12, frozenset({Role.INSOMNIAC})),
                    (14, frozenset({Role.MINION})),
                ),
            ),
            Statement("I am a Villager.", ((1, frozenset({Role.VILLAGER})),)),
            Statement(
                "I am a Robber and I swapped with Player 7. I am now a Wolf.",
                ((2, frozenset({Role.ROBBER})), (7, frozenset({Role.WOLF}))),
                ((SwitchPriority.ROBBER, 2, 7),),
            ),
            Statement(
                "I am a Seer and I saw that Center 1 was a Insomniac"
                " and that Center 2 was a Hunter.",
                (
                    (3, frozenset({Role.SEER})),
                    (13, frozenset({Role.INSOMNIAC})),
                    (14, frozenset({Role.HUNTER})),
                ),
            ),
            Statement("I am a Villager.", ((4, frozenset({Role.VILLAGER})),)),
            Statement(
                "I am a Seer and I saw that Center 0 was a Insomniac "
                "and that Center 2 was a Minion.",
                (
                    (5, frozenset({Role.SEER})),
                    (12, frozenset({Role.INSOMNIAC})),
                    (14, frozenset({Role.MINION})),
                ),
            ),
            Statement(
                "I am a Mason. The other Mason is Player 9.",
                ((6, frozenset({Role.MASON})), (9, frozenset({Role.MASON}))),
            ),
            Statement(
                "I am a Seer and I saw that Center 0 was a Insomniac "
                "and that Center 2 was a Minion.",
                (
                    (7, frozenset({Role.SEER})),
                    (12, frozenset({Role.INSOMNIAC})),
                    (14, frozenset({Role.MINION})),
                ),
            ),
            Statement(
                "I am a Seer and I saw that Center 0 was a Insomniac "
                "and that Center 2 was a Minion.",
                (
                    (8, frozenset({Role.SEER})),
                    (12, frozenset({Role.INSOMNIAC})),
                    (14, frozenset({Role.MINION})),
                ),
            ),
            Statement(
                "I am a Mason. The other Mason is Player 6.",
                ((9, frozenset({Role.MASON})), (6, frozenset({Role.MASON}))),
            ),
            Statement(
                "I am a Drunk and I swapped with Center 1.",
                ((10, frozenset({Role.DRUNK})),),
                ((SwitchPriority.DRUNK, 10, 13),),
            ),
            Statement("I am a Villager.", ((11, frozenset({Role.VILLAGER})),)),
        ),
    )
