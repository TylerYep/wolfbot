""" statements.py """
# pylint: disable=missing-function-docstring
from typing import Tuple

import pytest

from src.const import Role, RoleBits, SwitchPriority
from src.statements import Statement


@pytest.fixture
def example_statement() -> Statement:
    return Statement(
        "test",
        ((2, RoleBits(Role.ROBBER)), (0, RoleBits(Role.SEER))),
        ((SwitchPriority.ROBBER, 2, 0),),
        Role.ROBBER,
    )


@pytest.fixture
def small_statement_list(small_game_roles: Tuple[Role, ...]) -> Tuple[Statement, ...]:
    return (
        Statement("I am a Villager.", ((0, RoleBits(Role.VILLAGER)),)),
        Statement(
            "I am a Robber and I swapped with Player 2. I am now a Seer.",
            ((1, RoleBits(Role.ROBBER)), (2, RoleBits(Role.SEER))),
            ((SwitchPriority.ROBBER, 1, 2),),
        ),
        Statement(
            "I am a Seer and I saw that Player 1 was a Robber.",
            ((2, RoleBits(Role.SEER)), (1, RoleBits(Role.ROBBER))),
        ),
    )


@pytest.fixture
def medium_statement_list(medium_game_roles: Tuple[Role, ...]) -> Tuple[Statement, ...]:
    return (
        Statement(
            "I am a Seer and I saw that Player 2 was a Drunk.",
            ((0, RoleBits(Role.SEER)), (2, RoleBits(Role.DRUNK))),
        ),
        Statement(
            "I am a Seer and I saw that Player 3 was a Minion.",
            ((1, RoleBits(Role.SEER)), (3, RoleBits(Role.MINION))),
        ),
        Statement(
            "I am a Drunk and I swapped with Center 0.",
            ((2, RoleBits(Role.DRUNK)),),
            ((SwitchPriority.DRUNK, 2, 5),),
        ),
        Statement(
            "I am a Robber and I swapped with Player 2. I am now a Drunk.",
            ((3, RoleBits(Role.ROBBER)), (2, RoleBits(Role.DRUNK))),
            ((SwitchPriority.ROBBER, 3, 2),),
        ),
        Statement(
            "I am a Seer and I saw that Player 1 was a Wolf.",
            ((4, RoleBits(Role.SEER)), (1, RoleBits(Role.WOLF))),
        ),
    )


@pytest.fixture
def large_statement_list(large_game_roles: Tuple[Role, ...]) -> Tuple[Statement, ...]:
    return (
        Statement(
            "I am a Robber and I swapped with Player 6. I am now a Drunk.",
            ((0, RoleBits(Role.ROBBER)), (6, RoleBits(Role.DRUNK))),
            ((SwitchPriority.ROBBER, 6, 0),),
        ),
        Statement(
            "I am a Robber and I swapped with Player 0. I am now a Seer.",
            ((1, RoleBits(Role.ROBBER)), (0, RoleBits(Role.SEER))),
            ((SwitchPriority.ROBBER, 0, 1),),
        ),
        Statement(
            "I am a Seer and I saw that Player 3 was a Villager.",
            ((2, RoleBits(Role.SEER)), (3, RoleBits(Role.VILLAGER))),
        ),
        Statement("I am a Villager.", ((3, RoleBits(Role.VILLAGER)),)),
        Statement(
            "I am a Mason. The other Mason is Player 5.",
            ((4, RoleBits(Role.MASON)), (5, RoleBits(Role.MASON))),
        ),
        Statement(
            "I am a Mason. The other Mason is Player 4.",
            ((5, RoleBits(Role.MASON)), (4, RoleBits(Role.MASON))),
        ),
        Statement(
            "I am a Drunk and I swapped with Center 1.",
            ((6, RoleBits(Role.DRUNK)),),
            ((SwitchPriority.ROBBER, 9, 6),),
        ),
        Statement(
            "I am a Robber and I swapped with Player 5. I am now a Seer.",
            ((7, RoleBits(Role.ROBBER)), (5, RoleBits(Role.SEER))),
            ((SwitchPriority.ROBBER, 5, 7),),
        ),
    )
