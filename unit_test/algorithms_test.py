""" algorithms_test.py """
from src import algorithms, const
from src.const import Priority
from src.statements import Statement


class TestSolverState:
    """ Tests for the SolverState class. """

    @staticmethod
    def test_constructor():
        """ Should initialize a SolverState. """
        result = algorithms.SolverState([{"Villager"}], [], [True])

        assert isinstance(result, algorithms.SolverState)

    @staticmethod
    def test_is_valid_state():
        """ Should return False for empty SolverStates. """
        valid_state = algorithms.SolverState([{"Villager"}], [], [True])
        invalid_state = algorithms.SolverState([])

        assert valid_state.is_valid_state() is True
        assert invalid_state.is_valid_state() is False

    @staticmethod
    def test_eq(example_small_solverstate):
        """ Should be able to compare two identical SolverStates. """
        possible_roles = [{"Seer"}, {"Robber", "Villager", "Seer"}, {"Robber"}]
        switches = ((Priority.ROBBER, 2, 0),)
        path = ()

        result = algorithms.SolverState(possible_roles, switches, path)

        assert result == example_small_solverstate

    @staticmethod
    def test_repr():
        """ Should convert a SolverState into a representative string. """
        result = algorithms.SolverState([{"Villager"}], [], [True])

        assert str(result) == "SolverState(possible_roles=[{'Villager'}], switches=[], path=[True])"


class TestIsConsistent:
    """ Tests for the is_consistent function. """

    @staticmethod
    def test_is_consistent_on_empty_state(example_small_solverstate, example_statement):
        """ Should check a new statement against an empty SolverState for consistency. """
        start_state = algorithms.SolverState()

        result = algorithms.is_consistent(example_statement, start_state)

        assert result == example_small_solverstate

    @staticmethod
    def test_is_consistent_on_existing_state(example_medium_solverstate):
        """
        Should check a new statement against accumulated statements for consistency.
        Should not change result.path - that is done in the switching_solver function.
        """
        possible_roles = [const.ROLE_SET] * const.NUM_ROLES
        possible_roles[0] = {"Seer"}
        example_solverstate = algorithms.SolverState(possible_roles, (), (True,))
        new_statement = Statement("next", [(2, {"Drunk"})], [(Priority.DRUNK, 2, 5)])

        result = algorithms.is_consistent(new_statement, example_solverstate)

        assert result == example_medium_solverstate

    @staticmethod
    def test_is_consistent_deepcopy_mechanics(example_medium_solverstate):
        """
        Modifying one SolverState should not affect other SolverStates created by is_consistent.
        """
        possible_roles = [const.ROLE_SET] * const.NUM_ROLES
        possible_roles[0] = {"Seer"}
        example = algorithms.SolverState(possible_roles, (), (True,))
        new_statement = Statement("next", [(2, {"Drunk"})], [(Priority.DRUNK, 2, 5)])

        result = algorithms.is_consistent(new_statement, example)
        example.possible_roles += ("junk-data",)
        example.switches += ("junk-data",)
        example.possible_roles = list(example.possible_roles)[0] & set(["junk"])

        assert result == example_medium_solverstate


class TestCachedSolver:
    """ Tests for the cached_solver and count_roles function. """

    @staticmethod
    def test_solver_small(small_statement_list):
        """ Should return a SolverState with the most likely solution. """
        result = algorithms.cached_solver(small_statement_list)

        assert result == 3

    @staticmethod
    def test_solver_medium(medium_statement_list):
        """ Should return a SolverState with the most likely solution. """
        result = algorithms.cached_solver(medium_statement_list)

        assert result == 3

    @staticmethod
    def test_solver_large(large_statement_list):
        """ Should return a SolverState with the most likely solution. """
        result = algorithms.cached_solver(large_statement_list)

        assert result == 6


class TestSwitchingSolver:
    """ Tests for the switching_solver and count_roles function. """

    @staticmethod
    def test_solver_small(small_statement_list, example_small_solverstate_solved):
        """ Should return a SolverState with the most likely solution. """
        result = algorithms.switching_solver(small_statement_list)

        assert result[0] == example_small_solverstate_solved

    @staticmethod
    def test_solver_medium(medium_statement_list, example_medium_solverstate_solved):
        """ Should return a SolverState with the most likely solution. """
        result = algorithms.switching_solver(medium_statement_list)

        assert result[0] == example_medium_solverstate_solved

    @staticmethod
    def test_solver_medium_known_true(medium_statement_list, medium_game_roles):
        """ Should return a SolverState with the most likely solution. """
        const.ROLES = medium_game_roles
        possible_roles = [
            {"Drunk", "Minion", "Troublemaker", "Wolf", "Robber"},
            {"Seer"},
            {"Drunk"},
            {"Minion"},
            {"Drunk", "Minion", "Troublemaker", "Wolf", "Robber"},
            {"Robber", "Minion", "Troublemaker", "Seer", "Wolf", "Drunk"},
        ]

        result = algorithms.switching_solver(medium_statement_list, (1,))

        assert result[0] == algorithms.SolverState(
            possible_roles, ((Priority.DRUNK, 2, 5),), (False, True, True, False, False)
        )

    @staticmethod
    def test_solver_medium_multiple_solns(medium_statement_list, example_medium_solved_list):
        """ Should return a SolverState with the most likely solution. """
        result = algorithms.switching_solver(medium_statement_list)

        assert result == example_medium_solved_list

    @staticmethod
    def test_solver_large(large_statement_list, example_large_solverstate):
        """ Should return a SolverState with the most likely solution. """
        result = algorithms.switching_solver(large_statement_list)

        assert result[0] == example_large_solverstate

    @staticmethod
    def test_check_role_counts_true():
        """ Should return True if there is a a dict with counts of all certain roles. """
        const.ROLE_SET = {"Wolf", "Seer", "Villager", "Robber"}
        const.ROLE_COUNTS = {"Seer": 1, "Villager": 2, "Wolf": 0, "Robber": 0}
        possible_roles_list = [{"Villager"}, {"Seer"}, {"Villager"}] + [const.ROLE_SET] * 2

        result = algorithms.check_role_counts(possible_roles_list)

        assert result is True

    @staticmethod
    def test_check_role_counts_false():
        """ Should return a dict with counts of all certain roles. """
        const.ROLE_SET = {"Wolf", "Seer", "Villager", "Robber"}
        const.ROLE_COUNTS = {"Seer": 1, "Villager": 1, "Wolf": 0, "Robber": 0}
        possible_roles_list = [{"Villager"}, {"Seer"}, {"Villager"}] + [const.ROLE_SET] * 2

        result = algorithms.check_role_counts(possible_roles_list)

        assert result is False
