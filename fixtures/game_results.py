""" gameresults.py """
# pylint: disable=missing-function-docstring
from typing import Tuple

import pytest

from src import const
from src.const import Role, SwitchPriority, Team
from src.statements import Statement
from src.stats import GameResult


@pytest.fixture
def example_small_game_result(small_game_roles: Tuple[Role, ...]) -> GameResult:
    return GameResult(
        (Role.VILLAGER, Role.SEER, Role.ROBBER),
        (Role.VILLAGER, Role.SEER, Role.ROBBER),
        (),
        Team.VILLAGE,
        (
            Statement("I am a Villager.", ((0, frozenset({Role.VILLAGER})),)),
            Statement(
                "I am a Robber and I swapped with Player 2. I am now a Seer.",
                ((1, frozenset({Role.ROBBER})), (2, frozenset({Role.SEER}))),
                ((SwitchPriority.ROBBER, 1, 2),),
            ),
            Statement(
                "I am a Seer and I saw that Player 0 was a Villager.",
                ((2, frozenset({Role.SEER})), (0, frozenset({Role.VILLAGER}))),
            ),
        ),
    )


@pytest.fixture
def example_medium_game_result(medium_game_roles: Tuple[Role, ...]) -> GameResult:
    return GameResult(
        (Role.SEER, Role.WOLF, Role.TROUBLEMAKER, Role.DRUNK, Role.MINION, Role.ROBBER),
        (Role.SEER, Role.MINION, Role.TROUBLEMAKER, Role.DRUNK, Role.WOLF, Role.ROBBER),
        (1,),
        Team.WEREWOLF,
        (
            Statement(
                "I am a Seer and I saw that Player 2 was a Drunk.",
                ((0, frozenset({Role.SEER})), (2, frozenset({Role.DRUNK})),),
            ),
            Statement(
                "I am a Robber and I swapped with Player 2. I am now a Minion.",
                ((1, frozenset({Role.ROBBER})), (2, frozenset({Role.MINION})),),
                ((SwitchPriority.ROBBER, 1, 2),),
            ),
            Statement(
                "I am a Drunk and I swapped with Center 0.",
                ((2, frozenset({Role.DRUNK})),),
                ((SwitchPriority.DRUNK, 2, 5),),
            ),
            Statement(
                "I am a Robber and I swapped with Player 2. I am now a Drunk.",
                ((3, frozenset({Role.ROBBER})), (2, frozenset({Role.DRUNK})),),
                ((SwitchPriority.ROBBER, 3, 2),),
            ),
            Statement(
                "I am a Robber and I swapped with Player 0. I am now a Wolf.",
                ((4, frozenset({Role.ROBBER})), (0, frozenset({Role.WOLF})),),
                ((SwitchPriority.ROBBER, 4, 0),),
            ),
        ),
    )


@pytest.fixture
def example_large_game_result(large_game_roles: Tuple[Role, ...]) -> GameResult:
    mason_roles = tuple(
        [(i, const.ROLE_SET - frozenset({Role.MASON})) for i in range(const.NUM_PLAYERS) if i != 2]
    )
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
        Team.VILLAGE,
        (
            Statement("I am a Villager.", ((0, frozenset({Role.VILLAGER})),)),
            Statement(
                "I am a Drunk and I swapped with Center 2.",
                ((1, frozenset({Role.DRUNK})),),
                ((SwitchPriority.DRUNK, 1, 14),),
            ),
            Statement(
                "I am a Mason. The other Mason is not present.",
                ((2, frozenset({Role.MASON})),) + mason_roles,
            ),
            Statement(
                "I am a Seer and I saw that Center 1 was a Hunter and that Center 2 was a Wolf.",
                (
                    (3, frozenset({Role.SEER})),
                    (13, frozenset({Role.HUNTER})),
                    (14, frozenset({Role.WOLF})),
                ),
            ),
            Statement("I am a Villager.", ((4, frozenset({Role.VILLAGER})),)),
            Statement(
                "I am a Robber and I swapped with Player 1. I am now a Drunk.",
                ((5, frozenset({Role.ROBBER})), (1, frozenset({Role.DRUNK}))),
                ((SwitchPriority.ROBBER, 5, 1),),
            ),
            Statement(
                "I am a Seer and I saw that Center 1 was a Mason "
                "and that Center 0 was a Troublemaker.",
                (
                    (6, frozenset({Role.SEER})),
                    (13, frozenset({Role.MASON})),
                    (12, frozenset({Role.TROUBLEMAKER})),
                ),
            ),
            Statement(
                "I am a Seer and I saw that Center 0 was a Villager "
                "and that Center 2 was a Troublemaker.",
                (
                    (7, frozenset({Role.SEER})),
                    (12, frozenset({Role.VILLAGER})),
                    (14, frozenset({Role.TROUBLEMAKER})),
                ),
            ),
            Statement(
                "I am a Seer and I saw that Center 1 was a Troublemaker "
                "and that Center 2 was a Mason.",
                (
                    (8, frozenset({Role.SEER})),
                    (13, frozenset({Role.TROUBLEMAKER})),
                    (14, frozenset({Role.MASON})),
                ),
            ),
            Statement("I am a Villager.", ((9, frozenset({Role.VILLAGER})),)),
            Statement(
                "I am a Troublemaker and I swapped Player 0 and Player 3.",
                ((10, frozenset({Role.TROUBLEMAKER})),),
                ((SwitchPriority.TROUBLEMAKER, 0, 3),),
            ),
            Statement("I am a Hunter.", ((11, frozenset({Role.HUNTER})),)),
        ),
    )
