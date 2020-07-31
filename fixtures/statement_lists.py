""" statements.py """
# pylint: disable=missing-function-docstring
from typing import Tuple

import pytest

from src.const import Role, SwitchPriority
from src.statements import Statement


@pytest.fixture(scope="session")
def example_statement() -> Statement:
    return Statement(
        "test",
        ((2, frozenset({Role.ROBBER})), (0, frozenset({Role.SEER}))),
        ((SwitchPriority.ROBBER, 2, 0),),
        Role.ROBBER,
    )


@pytest.fixture(scope="session")
def small_statement_list() -> Tuple[Statement, ...]:
    return (
        Statement("I am a Villager.", ((0, frozenset({Role.VILLAGER})),)),
        Statement(
            "I am a Robber and I swapped with Player 2. I am now a Seer.",
            ((1, frozenset({Role.ROBBER})), (2, frozenset({Role.SEER}))),
            ((SwitchPriority.ROBBER, 1, 2),),
        ),
        Statement(
            "I am a Seer and I saw that Player 1 was a Robber.",
            ((2, frozenset({Role.SEER})), (1, frozenset({Role.ROBBER}))),
        ),
    )


@pytest.fixture(scope="session")
def medium_statement_list() -> Tuple[Statement, ...]:
    return (
        Statement(
            "I am a Seer and I saw that Player 2 was a Drunk.",
            ((0, frozenset({Role.SEER})), (2, frozenset({Role.DRUNK}))),
        ),
        Statement(
            "I am a Seer and I saw that Player 3 was a Minion.",
            ((1, frozenset({Role.SEER})), (3, frozenset({Role.MINION}))),
        ),
        Statement(
            "I am a Drunk and I swapped with Center 0.",
            ((2, frozenset({Role.DRUNK})),),
            ((SwitchPriority.DRUNK, 2, 5),),
        ),
        Statement(
            "I am a Robber and I swapped with Player 2. I am now a Drunk.",
            ((3, frozenset({Role.ROBBER})), (2, frozenset({Role.DRUNK}))),
            ((SwitchPriority.ROBBER, 3, 2),),
        ),
        Statement(
            "I am a Seer and I saw that Player 1 was a Wolf.",
            ((4, frozenset({Role.SEER})), (1, frozenset({Role.WOLF}))),
        ),
    )


@pytest.fixture(scope="session")
def large_statement_list() -> Tuple[Statement, ...]:
    return (
        Statement(
            "I am a Robber and I swapped with Player 6. I am now a Drunk.",
            ((0, frozenset({Role.ROBBER})), (6, frozenset({Role.DRUNK}))),
            ((SwitchPriority.ROBBER, 6, 0),),
        ),
        Statement(
            "I am a Robber and I swapped with Player 0. I am now a Seer.",
            ((1, frozenset({Role.ROBBER})), (0, frozenset({Role.SEER}))),
            ((SwitchPriority.ROBBER, 0, 1),),
        ),
        Statement(
            "I am a Seer and I saw that Player 3 was a Villager.",
            ((2, frozenset({Role.SEER})), (3, frozenset({Role.VILLAGER}))),
        ),
        Statement("I am a Villager.", ((3, frozenset({Role.VILLAGER})),)),
        Statement(
            "I am a Mason. The other Mason is Player 5.",
            ((4, frozenset({Role.MASON})), (5, frozenset({Role.MASON}))),
        ),
        Statement(
            "I am a Mason. The other Mason is Player 4.",
            ((5, frozenset({Role.MASON})), (4, frozenset({Role.MASON}))),
        ),
        Statement(
            "I am a Drunk and I swapped with Center 1.",
            ((6, frozenset({Role.DRUNK})),),
            ((SwitchPriority.ROBBER, 9, 6),),
        ),
        Statement(
            "I am a Robber and I swapped with Player 5. I am now a Seer.",
            ((7, frozenset({Role.ROBBER})), (5, frozenset({Role.SEER}))),
            ((SwitchPriority.ROBBER, 5, 7),),
        ),
    )
