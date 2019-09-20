''' algorithms_test.py '''
from copy import deepcopy

from src import algorithms, const
from src.statements import Statement

class TestSolverState:
    def test_constructor(self):
        ''' Should initialize a SolverState. '''
        result = algorithms.SolverState([{'Villager'}], [], [True])

        assert isinstance(result, algorithms.SolverState)

    def test_is_valid_state(self):
        ''' Should return False for empty SolverStates. '''
        valid_state = algorithms.SolverState([{'Villager'}], [], [True])
        invalid_state = algorithms.SolverState([])

        assert valid_state.is_valid_state()
        assert not invalid_state.is_valid_state()

    def test_repr(self):
        ''' Should convert a SolverState into a representative string. '''
        result = algorithms.SolverState([{'Villager'}], [], [True])

        assert str(result) == "\n[{'Villager'}]\n[True]\n[]\n"


class TestIsConsistent:
    def test_is_consistent_on_empty_state(self, small_game_roles, example_statement):
        ''' Should check a new statement against an empty SolverState for consistency. '''
        const.ROLES = small_game_roles
        start_state = algorithms.SolverState()

        result = algorithms.is_consistent(example_statement, start_state)

        assert result.switches == ((1, 2, 0),)
        assert result.possible_roles == (frozenset({'Seer'}),
                                         frozenset({'Robber', 'Villager', 'Seer'}),
                                         frozenset({'Robber'}))

    def test_is_consistent_on_existing_state(self, medium_game_roles):
        '''
        Should check a new statement against accumulated statements for consistency.
        Should not change result.path - that is done in the switching_solver function.
        '''
        const.ROLES = medium_game_roles
        possible_roles = [frozenset(deepcopy(const.ROLE_SET)) for i in range(const.NUM_ROLES)]
        possible_roles[0] = frozenset(['Seer'])
        example_solverstate = algorithms.SolverState(possible_roles, (), (True,))
        new_statement = Statement('next', [(2, {'Drunk'})], [(const.DRUNK_PRIORITY, 2, 5)])
        expected_roles = (frozenset({'Seer'}),
                          frozenset({'Troublemaker', 'Wolf', 'Drunk', 'Robber', 'Seer', 'Minion'}),
                          frozenset({'Drunk'}),
                          frozenset({'Troublemaker', 'Wolf', 'Drunk', 'Robber', 'Seer', 'Minion'}),
                          frozenset({'Troublemaker', 'Wolf', 'Drunk', 'Robber', 'Seer', 'Minion'}),
                          frozenset({'Troublemaker', 'Wolf', 'Drunk', 'Robber', 'Seer', 'Minion'}))

        result = algorithms.is_consistent(new_statement, example_solverstate)

        assert result.switches == ((3, 2, 5),)
        assert result.path == (True,)
        assert result.possible_roles == expected_roles


class TestSolver:
    def test_switching_solver(self, example_statement_list):
        ''' Should return a SolverState with the most likely solution. '''
        expected_roles = [
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
        expected_possible_roles = tuple([frozenset(role_set) for role_set in expected_roles])
        expected_path = (True, False, True, True, True, True, True, False)

        result = algorithms.switching_solver(example_statement_list)

        assert result[0].possible_roles == expected_possible_roles
        assert result[0].path == expected_path

    def test_count_roles(self):
        ''' Should return a dict with counts of all certain roles. '''
        const.ROLE_SET = set(['Wolf', 'Seer', 'Villager', 'Robber'])
        possible_roles_list = [
            {'Villager'},
            {'Seer'},
            {'Villager'}
        ] + [const.ROLE_SET]*2

        result = algorithms.count_roles(possible_roles_list)

        assert result == {'Seer': 1, 'Villager': 2, 'Wolf': 0, 'Robber': 0}
