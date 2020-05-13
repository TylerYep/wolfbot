""" statements.py """
from typing import List

import pytest

from src.const import SwitchPriority
from src.statements import Statement


@pytest.fixture
def example_statement() -> Statement:
    return Statement(
        "test",
        ((2, frozenset({"Robber"})), (0, frozenset({"Seer"}))),
        ((SwitchPriority.ROBBER, 2, 0),),
    )


@pytest.fixture
def small_statement_list() -> List[Statement]:
    return [
        Statement("I am a Villager.", ((0, frozenset({"Villager"})),), (), "Villager"),
        Statement(
            "I am a Robber and I swapped with Player 2. I am now a Seer.",
            ((1, frozenset({"Robber"})), (2, frozenset({"Seer"})),),
            ((SwitchPriority.ROBBER, 1, 2),),
            "Robber",
        ),
        Statement(
            "I am a Seer and I saw that Player 1 was a Robber.",
            ((2, frozenset({"Seer"})), (1, frozenset({"Robber"})),),
            (),
            "Seer",
        ),
    ]


@pytest.fixture
def medium_statement_list() -> List[Statement]:
    return [
        Statement(
            "I am a Seer and I saw that Player 2 was a Drunk.",
            ((0, frozenset({"Seer"})), (2, frozenset({"Drunk"})),),
            (),
            "Seer",
        ),
        Statement(
            "I am a Seer and I saw that Player 3 was a Minion.",
            ((1, frozenset({"Seer"})), (3, frozenset({"Minion"})),),
            (),
            "Seer",
        ),
        Statement(
            "I am a Drunk and I swapped with Center 0.",
            ((2, frozenset({"Drunk"})),),
            ((SwitchPriority.DRUNK, 2, 5),),
            "Drunk",
        ),
        Statement(
            "I am a Robber and I swapped with Player 2. I am now a Drunk.",
            ((3, frozenset({"Robber"})), (2, frozenset({"Drunk"})),),
            ((SwitchPriority.ROBBER, 3, 2),),
            "Robber",
        ),
        Statement(
            "I am a Seer and I saw that Player 1 was a Wolf.",
            ((4, frozenset({"Seer"})), (1, frozenset({"Wolf"})),),
            (),
            "Seer",
        ),
    ]


@pytest.fixture
def large_statement_list() -> List[Statement]:
    return [
        Statement(
            "I am a Robber and I swapped with Player 6. I am now a Drunk.",
            ((0, frozenset({"Robber"})), (6, frozenset({"Drunk"})),),
            ((SwitchPriority.ROBBER, 6, 0),),
        ),
        Statement(
            "I am a Robber and I swapped with Player 0. I am now a Seer.",
            ((1, frozenset({"Robber"})), (0, frozenset({"Seer"})),),
            ((SwitchPriority.ROBBER, 0, 1),),
        ),
        Statement(
            "I am a Seer and I saw that Player 3 was a Villager.",
            ((2, frozenset({"Seer"})), (3, frozenset({"Villager"})),),
            (),
        ),
        Statement("I am a Villager.", ((3, frozenset({"Villager"})),), ()),
        Statement(
            "I am a Mason. The other Mason is Player 5.",
            ((4, frozenset({"Mason"})), (5, frozenset({"Mason"})),),
            (),
        ),
        Statement(
            "I am a Mason. The other Mason is Player 4.",
            ((5, frozenset({"Mason"})), (4, frozenset({"Mason"})),),
            (),
        ),
        Statement(
            "I am a Drunk and I swapped with Center 1.",
            ((6, frozenset({"Drunk"})),),
            ((SwitchPriority.ROBBER, 9, 6),),
        ),
        Statement(
            "I am a Robber and I swapped with Player 5. I am now a Seer.",
            ((7, frozenset({"Robber"})), (5, frozenset({"Seer"})),),
            ((SwitchPriority.ROBBER, 5, 7),),
        ),
    ]
