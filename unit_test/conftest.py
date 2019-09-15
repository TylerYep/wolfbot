''' conftest.py '''
from typing import List, Tuple
from collections import Counter
import pytest

from src import const
from src.statements import Statement

@pytest.fixture(autouse=True)
def reset_const():
    const.logger.setLevel(const.TRACE)
    const.ROLES = ('Insomniac', 'Villager', 'Villager', 'Villager', 'Drunk', 'Wolf', 'Wolf', 'Seer',
                   'Tanner', 'Mason', 'Mason', 'Troublemaker', 'Robber', 'Minion', 'Hunter')
    const.ROLE_SET = set(const.ROLES)
    const.ROLE_COUNTS = dict(Counter(const.ROLES))
    const.NUM_ROLES = len(const.ROLES)
    const.NUM_PLAYERS = 12
    const.NUM_CENTER = 3


@pytest.fixture
def small_game_roles() -> Tuple[str, ...]:
    return ('Villager', 'Seer', 'Robber')


@pytest.fixture
def large_game_roles() -> Tuple[str, ...]:
    return ('Wolf', 'Villager', 'Robber', 'Seer', 'Villager', 'Tanner', 'Mason', 'Wolf',
            'Minion', 'Mason', 'Drunk', 'Villager', 'Troublemaker', 'Insomniac', 'Hunter')


@pytest.fixture
def example_statement() -> Statement:
    return Statement('test', [(2, {'Robber'}), (0, {'Seer'})], [(0, 2, const.ROBBER_PRIORITY)])


@pytest.fixture
def example_statement_list() -> List[Statement]:
    return [
        Statement('I am a Robber and I swapped with Player 6. I am now a Drunk.',
                  [(0, {'Robber'}), (6, {'Drunk'})], [(0, 6, 0)]),
        Statement('I am a Robber and I swapped with Player 0. I am now a Seer.',
                  [(1, {'Robber'}), (0, {'Seer'})], [(0, 0, 1)]),
        Statement('I am a Seer and I saw that Player 3 was a Villager.',
                  [(2, {'Seer'}), (3, {'Villager'})], []),
        Statement('I am a Villager.', [(3, {'Villager'})], []),
        Statement('I am a Mason. The other Mason is Player 5.',
                  [(4, {'Mason'}), (5, {'Mason'})], []),
        Statement('I am a Mason. The other Mason is Player 4.',
                  [(5, {'Mason'}), (4, {'Mason'})], []),
        Statement('I am a Drunk and I swapped with Center 1.',
                  [(6, {'Drunk'})], [(1, 9, 6)]),
        Statement('I am a Robber and I swapped with Player 5. I am now a Seer.',
                  [(7, {'Robber'}), (5, {'Seer'})], [(0, 5, 7)])
    ]


def debug_spacing_issues(captured: str, expected: str):
    ''' Helper method for debugging print differences. '''
    print(len(captured), len(expected))
    for i, captured_char in enumerate(captured):
        if captured_char != expected[i]:
            print("INCORRECT: ", i, captured_char + " vs " + expected[i])
        else:
            print(" " * 10, i, captured_char + " vs " + expected[i])
