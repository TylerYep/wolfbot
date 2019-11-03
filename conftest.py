''' conftest.py '''
from typing import List, Tuple
from collections import Counter
import random
import pytest

from src import const
from src.statements import Statement
from src.algorithms import SolverState
from src.stats import GameResult, SavedGame
from src.roles import Villager, Mason, Seer, Robber, Troublemaker, Drunk, Insomniac, \
                      Hunter, Wolf, Minion, Tanner

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
    const.VILLAGE_ROLES = {'Villager', 'Mason', 'Seer', 'Robber', 'Troublemaker',
                           'Drunk', 'Insomniac', 'Hunter'}
    const.EVIL_ROLES = {'Tanner', 'Wolf', 'Minion'}
    const.USE_VOTING = True
    const.USE_REG_WOLF = False
    const.USE_EXPECTIMAX_WOLF = False
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
def standard_game_roles() -> Tuple[str, ...]:
    const.ROLES = ('Villager', 'Villager', 'Villager', 'Seer', 'Wolf', 'Wolf', 'Troublemaker',
                   'Mason', 'Mason', 'Drunk')
    const.ROLE_SET = set(const.ROLES)
    const.ROLE_COUNTS = dict(Counter(const.ROLES))
    const.NUM_ROLES = len(const.ROLES)
    const.NUM_PLAYERS = 7
    const.NUM_CENTER = 3
    const.VILLAGE_ROLES &= const.ROLE_SET
    const.EVIL_ROLES &= const.ROLE_SET
    return const.ROLES


@pytest.fixture
def example_statement() -> Statement:
    return Statement('test', [(2, {'Robber'}), (0, {'Seer'})], [(const.ROBBER_PRIORITY, 2, 0)])


@pytest.fixture
def small_statement_list() -> List[Statement]:
    return [
        Statement("I am a Villager.", [(0, {'Villager'})], [], 'Villager'),
        Statement("I am a Robber and I swapped with Player 2. I am now a Seer.",
                  [(1, {'Robber'}), (2, {'Seer'})], [(1, 1, 2)], 'Robber'),
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
                  [(2, {'Drunk'})], [(3, 2, 5)], 'Drunk'),
        Statement("I am a Robber and I swapped with Player 2. I am now a Drunk.",
                  [(3, {'Robber'}), (2, {'Drunk'})], [(1, 3, 2)], 'Robber'),
        Statement("I am a Seer and I saw that Player 1 was a Wolf.",
                  [(4, {'Seer'}), (1, {'Wolf'})], [], 'Seer')
    ]

@pytest.fixture
def large_statement_list() -> List[Statement]:
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
    possible_roles = [{'Seer'}, {'Robber', 'Villager', 'Seer'}, {'Robber'}]
    return SolverState(possible_roles, ((1, 2, 0),))


@pytest.fixture
def example_small_solverstate_solved(small_game_roles) -> SolverState:
    possible_roles = [{'Villager'}, {'Robber'}, {'Seer'}]
    return SolverState(possible_roles, ((1, 1, 2),), (True, True, True))


@pytest.fixture
def example_medium_solverstate(medium_game_roles) -> SolverState:
    possible_roles = [{'Seer'},
                      {'Troublemaker', 'Wolf', 'Drunk', 'Robber', 'Seer', 'Minion'},
                      {'Drunk'},
                      {'Troublemaker', 'Wolf', 'Drunk', 'Robber', 'Seer', 'Minion'},
                      {'Troublemaker', 'Wolf', 'Drunk', 'Robber', 'Seer', 'Minion'},
                      {'Troublemaker', 'Wolf', 'Drunk', 'Robber', 'Seer', 'Minion'}]
    return SolverState(possible_roles, ((3, 2, 5),), (True,))


@pytest.fixture
def example_medium_solverstate_solved(medium_game_roles) -> SolverState:
        possible_roles = [{'Seer'},
                          {'Robber', 'Drunk', 'Wolf', 'Troublemaker', 'Minion'},
                          {'Drunk'},
                          {'Robber'},
                          {'Robber', 'Drunk', 'Wolf', 'Troublemaker', 'Minion'},
                          {'Drunk', 'Robber', 'Seer', 'Wolf', 'Troublemaker', 'Minion'}]
        switches = ((3, 2, 5), (1, 3, 2))
        path = (True, False, True, True, False)
        return SolverState(possible_roles, switches, path)


@pytest.fixture
def example_medium_solved_list(medium_game_roles) -> SolverState:
    return [SolverState([{'Seer'},
                         {'Robber', 'Troublemaker', 'Wolf', 'Drunk', 'Minion'},
                         {'Drunk'},
                         {'Robber'},
                         {'Robber', 'Troublemaker', 'Wolf', 'Drunk', 'Minion'},
                         {'Robber', 'Troublemaker', 'Wolf', 'Drunk', 'Seer', 'Minion'}],
                         ((3, 2, 5), (1, 3, 2)),
                         (True, False, True, True, False)),
            SolverState([{'Robber', 'Troublemaker', 'Wolf', 'Drunk', 'Minion'},
                         {'Wolf'},
                         {'Drunk'},
                         {'Robber'},
                         {'Seer'},
                         {'Robber', 'Troublemaker', 'Wolf', 'Drunk', 'Seer', 'Minion'}],
                         ((3, 2, 5), (1, 3, 2)),
                         (False, False, True, True, True))]

@pytest.fixture
def example_medium_solverstate_list(medium_game_roles) -> SolverState:
    return [SolverState([{'Seer'},
                         {'Robber'},
                         {'Drunk'},
                         {'Minion', 'Wolf', 'Seer', 'Drunk', 'Troublemaker'},
                         {'Minion', 'Wolf', 'Drunk', 'Troublemaker', 'Robber'},
                         {'Minion', 'Wolf', 'Seer', 'Drunk', 'Troublemaker', 'Robber'}],
                        ((1, 1, 0), (3, 2, 5)),
                        (True, True, True, False, False)),
            SolverState([{'Seer'},
                         {'Minion', 'Wolf', 'Seer', 'Drunk', 'Troublemaker'},
                         {'Drunk'},
                         {'Robber'},
                         {'Minion', 'Wolf', 'Drunk', 'Troublemaker', 'Robber'},
                         {'Minion', 'Wolf', 'Seer', 'Drunk', 'Troublemaker', 'Robber'}],
                        ((3, 2, 5), (1, 3, 2)),
                        (True, False, True, True, False)),
            SolverState([{'Minion', 'Wolf', 'Drunk', 'Troublemaker', 'Robber'},
                         {'Minion', 'Wolf', 'Seer', 'Drunk', 'Troublemaker'},
                         {'Drunk'},
                         {'Robber'},
                         {'Seer'},
                         {'Minion', 'Wolf', 'Seer', 'Drunk', 'Troublemaker', 'Robber'}],
                        ((3, 2, 5), (1, 3, 2)),
                        (False, False, True, True, True))]


@pytest.fixture
def example_large_solverstate(large_game_roles) -> SolverState:
    possible_roles = [
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
    ] + [const.ROLE_SET] * 7
    switches = ((0, 6, 0), (1, 9, 6))
    path = (True, False, True, True, True, True, True, False)
    return SolverState(possible_roles, switches, path)


@pytest.fixture
def example_small_game_result(small_game_roles) -> GameResult:
    return GameResult(['Villager', 'Seer', 'Robber'],
                      ['Villager', 'Seer', 'Robber'],
                      [],
                      'Villager')


@pytest.fixture
def example_medium_game_result(medium_game_roles) -> GameResult:
    return GameResult(['Seer', 'Wolf', 'Troublemaker', 'Drunk', 'Minion', 'Robber'],
                      ['Seer', 'Wolf', 'Troublemaker', 'Drunk', 'Minion', 'Robber'],
                      [1],
                      'Villager')


@pytest.fixture
def example_large_game_result(large_game_roles) -> GameResult:
    return GameResult(['Villager', 'Insomniac', 'Mason', 'Tanner', 'Villager', 'Drunk', 'Seer',
                       'Wolf', 'Minion', 'Villager', 'Wolf', 'Hunter', 'Troublemaker',
                       'Mason', 'Robber'],
                      ['Villager', 'Mason', 'Mason', 'Minion', 'Villager', 'Drunk', 'Tanner',
                       'Troublemaker', 'Villager', 'Wolf', 'Wolf', 'Hunter', 'Insomniac',
                       'Seer', 'Robber'],
                      [7, 10],
                      'Villager')



@pytest.fixture
def example_small_saved_game(small_game_roles) -> SavedGame:
    return SavedGame(('Villager', 'Robber', 'Seer'),
                     ['Villager', 'Seer', 'Robber'],
                     [Statement("I am a Villager.", [(0, {'Villager'})], [], 'Villager'),
                      Statement("I am a Robber and I swapped with Player 2. I am now a Seer.",
                                [(1, {'Robber'}), (2, {'Seer'})], [(1, 1, 2)], 'Robber'),
                      Statement("I am a Seer and I saw that Player 1 was a Robber.",
                                [(2, {'Seer'}), (1, {'Robber'})], [], 'Seer')],
                     [Villager(0), Robber(1, 2, 'Seer'), Seer(2, (1, 'Robber'), (None, None))])


@pytest.fixture
def example_medium_saved_game(medium_game_roles) -> SavedGame:
    return SavedGame(('Seer', 'Wolf', 'Drunk', 'Robber', 'Minion', 'Troublemaker'),
                     ['Seer', 'Wolf', 'Troublemaker', 'Drunk', 'Minion', 'Robber'],
                     [Statement("I am a Seer and I saw that Player 2 was a Drunk.",
                                [(0, {'Seer'}), (2, {'Drunk'})], [], 'Seer'),
                      Statement("I am a Robber and I swapped with Player 0. I am now a Seer.",
                                [(1, {'Robber'}), (0, {'Seer'})], [(1, 1, 0)], 'Robber'),
                      Statement("I am a Drunk and I swapped with Center 0.",
                                [(2, {'Drunk'})], [(3, 2, 5)], 'Drunk'),
                      Statement("I am a Robber and I swapped with Player 2. I am now a Drunk.",
                                [(3, {'Robber'}), (2, {'Drunk'})], [(1, 3, 2)], 'Robber'),
                      Statement("I am a Seer and I saw that Player 3 was a Robber.",
                                [(4, {'Seer'}), (3, {'Robber'})], [], 'Seer')],
                     [Seer(0, (2, 'Drunk'), (None, None)), Wolf(1, [1], 5, 'Troublemaker'),
                      Drunk(2, 5), Robber(3, 2, 'Drunk'), Minion(4, [1])])


@pytest.fixture
def example_large_saved_game(large_game_roles) -> SavedGame:
    mason_roles = [const.ROLE_SET - {'Mason'} for i in range(len(const.NUM_PLAYERS)) if i != 2]
    return SavedGame(('Villager', 'Drunk', 'Mason', 'Tanner', 'Villager', 'Robber', 'Seer',
                      'Wolf', 'Minion', 'Villager', 'Wolf', 'Hunter',
                      'Troublemaker', 'Mason', 'Insomniac'),
                     ['Villager', 'Insomniac', 'Mason', 'Tanner', 'Villager', 'Drunk', 'Seer',
                      'Wolf', 'Minion', 'Villager', 'Wolf', 'Hunter', 'Troublemaker',
                      'Mason', 'Robber'],
                     [Statement("I am a Villager.", [(0, {'Villager'})], [], 'Villager'),
                      Statement("I am a Drunk and I swapped with Center 2.",
                                [(1, {'Drunk'})], [(3, 1, 14)], 'Drunk'),
                      Statement("I am a Mason. The other Mason is not present.",
                                [(2, {'Mason'})] + mason_roles, [], 'Mason'),
                      Statement("I am a Robber and I swapped with Player 10. I am now a Insomniac.",
                                [(3, {'Robber'}), (10, {'Insomniac'})], [(1, 3, 10)], 'Robber'),
                      Statement("I am a Villager.", [(4, {'Villager'})], [], 'Villager'),
                      Statement("I am a Robber and I swapped with Player 1. I am now a Drunk.",
                                [(5, {'Robber'}), (1, {'Drunk'})], [(1, 5, 1)], 'Robber'),
                      Statement(("I am a Seer and I saw that Center 1 was a Mason and that "
                                "Center 0 was a Troublemaker."), [(6, {'Seer'}),
                                (13, {'Mason'}), (12, {'Troublemaker'})], [], 'Seer'),
                      Statement("I am a Seer and I saw that Player 3 was a Robber.",
                                [(7, {'Seer'}), (3, {'Robber'})], [], 'Seer'),
                      Statement("I am a Troublemaker and I swapped Player 0 and Player 1.",
                                [(8, {'Troublemaker'})], [(2, 0, 1)], 'Troublemaker'),
                      Statement("I am a Villager.", [(9, {'Villager'})], [], 'Villager'),
                      Statement("I am a Troublemaker and I swapped Player 3 and Player 4.",
                                [(10, {'Troublemaker'})], [(2, 3, 4)], 'Troublemaker'),
                      Statement("I am a Hunter.", [(11, {'Hunter'})], [], 'Hunter')],
                     [Villager(0), Drunk(1, 14), Mason(2, [2]), Tanner(3), Villager(4),
                      Robber(5, 1, 'Drunk'), Seer(6, (13, 'Mason'), (12, 'Troublemaker')),
                      Wolf(7, [7, 10], None, None), Minion(8, [7, 10]), Villager(9),
                      Wolf(10, [7, 10], None, None), Hunter(11)])


def debug_spacing_issues(captured: str, expected: str):
    ''' Helper method for debugging print differences. '''
    print(len(captured), len(expected))
    for i, captured_char in enumerate(captured):
        if captured_char != expected[i]:
            print("INCORRECT: ", i, captured_char + " vs " + expected[i])
        else:
            print(" " * 10, i, captured_char + " vs " + expected[i])
