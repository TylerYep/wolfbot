''' algorithms_test.py '''
from src import algorithms, const
from src.statements import Statement

class TestSolverState:
    ''' Tests for the SolverState class. '''
    @staticmethod
    def test_constructor():
        ''' Should initialize a SolverState. '''
        result = algorithms.SolverState([{'Villager'}], [], [True])

        assert isinstance(result, algorithms.SolverState)

    @staticmethod
    def test_is_valid_state():
        ''' Should return False for empty SolverStates. '''
        valid_state = algorithms.SolverState([{'Villager'}], [], [True])
        invalid_state = algorithms.SolverState([])

        assert valid_state.is_valid_state()
        assert not invalid_state.is_valid_state()

    @staticmethod
    def test_eq(example_small_solverstate):
        ''' Should be able to compare two identical SolverStates. '''
        possible_roles = [{'Seer'}, {'Robber', 'Villager', 'Seer'}, {'Robber'}]
        switches = ((1, 2, 0),)
        path = ()

        result = algorithms.SolverState(possible_roles, switches, path)

        assert result == example_small_solverstate

    @staticmethod
    def test_repr():
        ''' Should convert a SolverState into a representative string. '''
        result = algorithms.SolverState([{'Villager'}], [], [True])

        assert str(result) == "SolverState([{'Villager'}], [], [True])"


class TestIsConsistent:
    ''' Tests for the is_consistent function. '''
    @staticmethod
    def test_is_consistent_on_empty_state(example_small_solverstate, example_statement):
        ''' Should check a new statement against an empty SolverState for consistency. '''
        start_state = algorithms.SolverState()

        result = algorithms.is_consistent(example_statement, start_state)

        assert result == example_small_solverstate

    @staticmethod
    def test_is_consistent_on_existing_state(example_medium_solverstate):
        '''
        Should check a new statement against accumulated statements for consistency.
        Should not change result.path - that is done in the switching_solver function.
        '''
        possible_roles = [const.ROLE_SET]*const.NUM_ROLES
        possible_roles[0] = {'Seer'}
        example_solverstate = algorithms.SolverState(possible_roles, (), (True,))
        new_statement = Statement('next', [(2, {'Drunk'})], [(const.DRUNK_PRIORITY, 2, 5)])

        result = algorithms.is_consistent(new_statement, example_solverstate)

        assert result == example_medium_solverstate


class TestSwitchingSolver:
    ''' Tests for the switching_solver and count_roles function. '''

    @staticmethod
    def test_solver_small(small_statement_list, example_small_solverstate_solved):
        ''' Should return a SolverState with the most likely solution. '''
        result = algorithms.switching_solver(small_statement_list)

        assert result[0] == example_small_solverstate_solved

    @staticmethod
    def test_solver_medium(medium_statement_list, example_medium_solverstate_solved):
        ''' Should return a SolverState with the most likely solution. '''
        result = algorithms.switching_solver(medium_statement_list)

        assert result[0] == example_medium_solverstate_solved

    @staticmethod
    def test_solver_medium_multiple_solns(medium_statement_list, example_medium_solved_list):
        ''' Should return a SolverState with the most likely solution. '''
        result = algorithms.switching_solver(medium_statement_list)

        assert result == example_medium_solved_list

    @staticmethod
    def test_solver_large(large_statement_list, example_large_solverstate):
        ''' Should return a SolverState with the most likely solution. '''
        result = algorithms.switching_solver(large_statement_list)

        assert result[0] == example_large_solverstate

    @staticmethod
    def test_count_roles():
        ''' Should return a dict with counts of all certain roles. '''
        const.ROLE_SET = {'Wolf', 'Seer', 'Villager', 'Robber'}
        possible_roles_list = [{'Villager'}, {'Seer'}, {'Villager'}] + [const.ROLE_SET]*2

        result = algorithms.count_roles(possible_roles_list)

        assert result == {'Seer': 1, 'Villager': 2, 'Wolf': 0, 'Robber': 0}
