''' solverstates.py '''
from typing import List
import pytest

from src import const
from src.const import Priority
from src.algorithms import SolverState


@pytest.fixture
def example_small_solverstate(small_game_roles) -> SolverState:
    possible_roles = [{'Seer'}, {'Robber', 'Villager', 'Seer'}, {'Robber'}]
    return SolverState(possible_roles, ((Priority.ROBBER, 2, 0),))


@pytest.fixture
def example_small_solverstate_solved(small_game_roles) -> SolverState:
    possible_roles = [{'Villager'}, {'Robber'}, {'Seer'}]
    return SolverState(possible_roles, ((Priority.ROBBER, 1, 2),), (True, True, True))


@pytest.fixture
def example_medium_solverstate(medium_game_roles) -> SolverState:
    possible_roles = [{'Seer'},
                      {'Troublemaker', 'Wolf', 'Drunk', 'Robber', 'Seer', 'Minion'},
                      {'Drunk'},
                      {'Troublemaker', 'Wolf', 'Drunk', 'Robber', 'Seer', 'Minion'},
                      {'Troublemaker', 'Wolf', 'Drunk', 'Robber', 'Seer', 'Minion'},
                      {'Troublemaker', 'Wolf', 'Drunk', 'Robber', 'Seer', 'Minion'}]
    return SolverState(possible_roles, ((Priority.DRUNK, 2, 5),), (True,))


@pytest.fixture
def example_medium_solverstate_solved(medium_game_roles) -> SolverState:
    possible_roles = [{'Seer'},
                      {'Robber', 'Drunk', 'Wolf', 'Troublemaker', 'Minion'},
                      {'Drunk'},
                      {'Robber'},
                      {'Robber', 'Drunk', 'Wolf', 'Troublemaker', 'Minion'},
                      {'Drunk', 'Robber', 'Seer', 'Wolf', 'Troublemaker', 'Minion'}]
    switches = ((Priority.DRUNK, 2, 5), (Priority.ROBBER, 3, 2))
    path = (True, False, True, True, False)
    return SolverState(possible_roles, switches, path)


@pytest.fixture
def example_medium_solved_list(medium_game_roles) -> List[SolverState]:
    return [SolverState([{'Seer'},
                         {'Robber', 'Troublemaker', 'Wolf', 'Drunk', 'Minion'},
                         {'Drunk'},
                         {'Robber'},
                         {'Robber', 'Troublemaker', 'Wolf', 'Drunk', 'Minion'},
                         {'Robber', 'Troublemaker', 'Wolf', 'Drunk', 'Seer', 'Minion'}],
                        ((Priority.DRUNK, 2, 5), (Priority.ROBBER, 3, 2)),
                        (True, False, True, True, False)),
            SolverState([{'Robber', 'Troublemaker', 'Wolf', 'Drunk', 'Minion'},
                         {'Wolf'},
                         {'Drunk'},
                         {'Robber'},
                         {'Seer'},
                         {'Robber', 'Troublemaker', 'Wolf', 'Drunk', 'Seer', 'Minion'}],
                        ((Priority.DRUNK, 2, 5), (Priority.ROBBER, 3, 2)),
                        (False, False, True, True, True))]


@pytest.fixture
def example_medium_solverstate_list(medium_game_roles) -> List[SolverState]:
    return [SolverState([{'Seer'},
                         {'Robber'},
                         {'Drunk'},
                         {'Minion', 'Wolf', 'Seer', 'Drunk', 'Troublemaker'},
                         {'Minion', 'Wolf', 'Drunk', 'Troublemaker', 'Robber'},
                         {'Minion', 'Wolf', 'Seer', 'Drunk', 'Troublemaker', 'Robber'}],
                        ((Priority.ROBBER, 1, 0), (Priority.DRUNK, 2, 5)),
                        (True, True, True, False, False)),
            SolverState([{'Seer'},
                         {'Minion', 'Wolf', 'Seer', 'Drunk', 'Troublemaker'},
                         {'Drunk'},
                         {'Robber'},
                         {'Minion', 'Wolf', 'Drunk', 'Troublemaker', 'Robber'},
                         {'Minion', 'Wolf', 'Seer', 'Drunk', 'Troublemaker', 'Robber'}],
                        ((Priority.DRUNK, 2, 5), (Priority.ROBBER, 3, 2)),
                        (True, False, True, True, False)),
            SolverState([{'Minion', 'Wolf', 'Drunk', 'Troublemaker', 'Robber'},
                         {'Minion', 'Wolf', 'Seer', 'Drunk', 'Troublemaker'},
                         {'Drunk'},
                         {'Robber'},
                         {'Seer'},
                         {'Minion', 'Wolf', 'Seer', 'Drunk', 'Troublemaker', 'Robber'}],
                        ((Priority.DRUNK, 2, 5), (Priority.ROBBER, 3, 2)),
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
    switches = ((Priority.ROBBER, 6, 0), (Priority.ROBBER, 9, 6))
    path = (True, False, True, True, True, True, True, False)
    return SolverState(possible_roles, switches, path)
