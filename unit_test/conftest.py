''' conftest.py '''
from typing import List, Tuple
from collections import Counter
import random
import pytest

from src import const
from src.statements import Statement
from src.algorithms import SolverState

@pytest.fixture(autouse=True)
def reset_const():
    const.logger.setLevel(const.TRACE)
    const.ROLES = ('Insomniac', 'Villager', 'Robber', 'Villager', 'Drunk', 'Wolf', 'Wolf', 'Seer',
                   'Tanner', 'Mason', 'Minion', 'Troublemaker', 'Villager', 'Mason', 'Hunter')
    const.ROLE_SET = set(const.ROLES)
    const.ROLE_COUNTS = dict(Counter(const.ROLES))
    const.NUM_ROLES = len(const.ROLES)
    const.NUM_PLAYERS = 12
    const.NUM_CENTER = 3
    const.CENTER_SEER_PROB = 0.9
    const.VILLAGE_ROLES &= const.ROLE_SET
    const.EVIL_ROLES &= const.ROLE_SET
    random.seed(0)


@pytest.fixture
def small_game_roles() -> Tuple[str, ...]:
    const.ROLES = ('Villager', 'Seer', 'Robber')
    const.ROLE_SET = set(const.ROLES)
    const.ROLE_COUNTS = dict(Counter(const.ROLES))
    const.NUM_ROLES = len(const.ROLES)
    const.NUM_PLAYERS = 3
    const.NUM_CENTER = 0
    const.VILLAGE_ROLES &= const.ROLE_SET
    const.EVIL_ROLES &= const.ROLE_SET
    return const.ROLES


@pytest.fixture
def medium_game_roles() -> Tuple[str, ...]:
    const.ROLES = ('Robber', 'Drunk', 'Wolf', 'Troublemaker', 'Seer', 'Minion')
    const.ROLE_SET = set(const.ROLES)
    const.ROLE_COUNTS = dict(Counter(const.ROLES))
    const.NUM_ROLES = len(const.ROLES)
    const.NUM_PLAYERS = 5
    const.NUM_CENTER = 1
    const.VILLAGE_ROLES &= const.ROLE_SET
    const.EVIL_ROLES &= const.ROLE_SET
    return const.ROLES


@pytest.fixture
def large_game_roles() -> Tuple[str, ...]:
    const.ROLES = ('Wolf', 'Villager', 'Robber', 'Seer', 'Villager', 'Tanner', 'Mason', 'Wolf',
                   'Minion', 'Mason', 'Drunk', 'Villager', 'Troublemaker', 'Insomniac', 'Hunter')
    const.ROLE_SET = frozenset(const.ROLES)
    const.ROLE_COUNTS = dict(Counter(const.ROLES))
    const.NUM_ROLES = len(const.ROLES)
    const.NUM_PLAYERS = 12
    const.NUM_CENTER = 3
    const.VILLAGE_ROLES &= const.ROLE_SET
    const.EVIL_ROLES &= const.ROLE_SET
    return const.ROLES


@pytest.fixture
def example_statement() -> Statement:
    return Statement('test', [(2, {'Robber'}), (0, {'Seer'})], [(const.ROBBER_PRIORITY, 2, 0)])


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


@pytest.fixture
def example_small_solverstate(small_game_roles) -> SolverState:
    possible_roles = (frozenset({'Seer'}),
                      frozenset({'Robber', 'Villager', 'Seer'}),
                      frozenset({'Robber'}))
    return SolverState(possible_roles, ((1, 2, 0),))


@pytest.fixture
def example_medium_solverstate(medium_game_roles) -> SolverState:
    possible_roles = (frozenset({'Seer'}),
                      frozenset({'Troublemaker', 'Wolf', 'Drunk', 'Robber', 'Seer', 'Minion'}),
                      frozenset({'Drunk'}),
                      frozenset({'Troublemaker', 'Wolf', 'Drunk', 'Robber', 'Seer', 'Minion'}),
                      frozenset({'Troublemaker', 'Wolf', 'Drunk', 'Robber', 'Seer', 'Minion'}),
                      frozenset({'Troublemaker', 'Wolf', 'Drunk', 'Robber', 'Seer', 'Minion'}))
    return SolverState(possible_roles, ((3, 2, 5),), (True,))


@pytest.fixture
def example_large_solverstate(large_game_roles) -> SolverState:
    roles = [
        {'Robber'},
        {'Seer', 'Hunter', 'Drunk', 'Tanner', 'Wolf', 'Insomniac',
         'Mason', 'Minion', 'Villager', 'Troublemaker'},
        {'Seer'},
        {'Villager'},
        {'Mason'},
        {'Mason'},
        {'Drunk'},
        {'Seer', 'Hunter', 'Drunk', 'Tanner', 'Wolf', 'Insomniac', 'Mason',
         'Minion', 'Villager', 'Troublemaker'}
    ] + [const.ROLE_SET]*7
    possible_roles = tuple([frozenset(role_set) for role_set in roles])
    switches = ((0, 6, 0), (1, 9, 6))
    path = (True, False, True, True, True, True, True, False)
    return SolverState(possible_roles, switches, path)


def debug_spacing_issues(captured: str, expected: str):
    ''' Helper method for debugging print differences. '''
    print(len(captured), len(expected))
    for i, captured_char in enumerate(captured):
        if captured_char != expected[i]:
            print("INCORRECT: ", i, captured_char + " vs " + expected[i])
        else:
            print(" " * 10, i, captured_char + " vs " + expected[i])
