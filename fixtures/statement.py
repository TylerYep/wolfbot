''' statements.py '''
from typing import List
import pytest

from src.const import Priority
from src.statements import Statement


@pytest.fixture
def example_statement() -> Statement:
    return Statement('test', [(2, {'Robber'}), (0, {'Seer'})], [(Priority.ROBBER, 2, 0)])


@pytest.fixture
def small_statement_list() -> List[Statement]:
    return [
        Statement("I am a Villager.", [(0, {'Villager'})], [], 'Villager'),
        Statement("I am a Robber and I swapped with Player 2. I am now a Seer.",
                  [(1, {'Robber'}), (2, {'Seer'})], [(Priority.ROBBER, 1, 2)], 'Robber'),
        Statement("I am a Seer and I saw that Player 1 was a Robber.",
                  [(2, {'Seer'}), (1, {'Robber'})], [], 'Seer')
    ]


@pytest.fixture
def medium_statement_list() -> List[Statement]:
    return [
        Statement("I am a Seer and I saw that Player 2 was a Drunk.",
                  [(0, {'Seer'}), (2, {'Drunk'})], [], 'Seer'),
        Statement("I am a Seer and I saw that Player 3 was a Minion.",
                  [(1, {'Seer'}), (3, {'Minion'})], [], 'Seer'),
        Statement("I am a Drunk and I swapped with Center 0.",
                  [(2, {'Drunk'})], [(Priority.DRUNK, 2, 5)], 'Drunk'),
        Statement("I am a Robber and I swapped with Player 2. I am now a Drunk.",
                  [(3, {'Robber'}), (2, {'Drunk'})], [(Priority.ROBBER, 3, 2)], 'Robber'),
        Statement("I am a Seer and I saw that Player 1 was a Wolf.",
                  [(4, {'Seer'}), (1, {'Wolf'})], [], 'Seer')
    ]


@pytest.fixture
def large_statement_list() -> List[Statement]:
    return [
        Statement('I am a Robber and I swapped with Player 6. I am now a Drunk.',
                  [(0, {'Robber'}), (6, {'Drunk'})], [(Priority.ROBBER, 6, 0)]),
        Statement('I am a Robber and I swapped with Player 0. I am now a Seer.',
                  [(1, {'Robber'}), (0, {'Seer'})], [(Priority.ROBBER, 0, 1)]),
        Statement('I am a Seer and I saw that Player 3 was a Villager.',
                  [(2, {'Seer'}), (3, {'Villager'})], []),
        Statement('I am a Villager.', [(3, {'Villager'})], []),
        Statement('I am a Mason. The other Mason is Player 5.',
                  [(4, {'Mason'}), (5, {'Mason'})], []),
        Statement('I am a Mason. The other Mason is Player 4.',
                  [(5, {'Mason'}), (4, {'Mason'})], []),
        Statement('I am a Drunk and I swapped with Center 1.',
                  [(6, {'Drunk'})], [(Priority.ROBBER, 9, 6)]),
        Statement('I am a Robber and I swapped with Player 5. I am now a Seer.',
                  [(7, {'Robber'}), (5, {'Seer'})], [(Priority.ROBBER, 5, 7)])
    ]
