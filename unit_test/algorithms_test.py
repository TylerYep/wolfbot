''' algorithms_test.py '''
from src import algorithms, const

class TestSolverState:
    def test_constructor(self):
        ''' Should initialize a SolverState. '''
        state = algorithms.SolverState([{'Villager'}], [], [True])

        assert isinstance(state, algorithms.SolverState)

    def test_is_valid_state(self):
        ''' Should return False for empty SolverStates. '''
        valid_state = algorithms.SolverState([{'Villager'}], [], [True])
        invalid_state = algorithms.SolverState()

        assert valid_state.is_valid_state()
        assert not invalid_state.is_valid_state()

    def test_repr(self):
        ''' Should convert a SolverState into a representative string. '''
        state = algorithms.SolverState([{'Villager'}], [], [True])

        assert str(state) == "\n[{'Villager'}]\n[True]\n[]\n"


class TestIsConsistent:
    def test_is_consistent(self):
        ''' Should check a new statement against the accumulated statements for consistency. '''
        pass


class TestSolver:
    def test_switching_solver(self, example_statement_list):
        ''' Should return a SolverState with the most likely solution. '''
        expected_possible_roles = [
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
        expected_path = [True, False, True, True, True, True, True, False]

        result_list = algorithms.switching_solver(example_statement_list)

        assert result_list[0].possible_roles == expected_possible_roles
        assert result_list[0].path == expected_path

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
