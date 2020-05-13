""" algorithms_test.py """
from src import algorithms, const
from src.const import SwitchPriority
from src.statements import Statement


class TestSolverState:
    """ Tests for the SolverState class. """

    @staticmethod
    def test_constructor():
        """ Should initialize a SolverState. """
        result = algorithms.SolverState((frozenset({"Villager"}),), path=(True,))

        assert isinstance(result, algorithms.SolverState)

    @staticmethod
    def test_eq(example_small_solverstate):
        """ Should be able to compare two identical SolverStates. """
        possible_roles = (
            frozenset({"Seer"}),
            frozenset({"Robber", "Villager", "Seer"}),
            frozenset({"Robber"}),
        )
        switches = ((SwitchPriority.ROBBER, 2, 0),)
        path = (True,)

        result = algorithms.SolverState(possible_roles, switches, path)

        assert result == example_small_solverstate

    @staticmethod
    def test_repr():
        """ Should convert a SolverState into a representative string. """
        result = algorithms.SolverState((frozenset({"Villager"}),), path=(True,))

        assert str(result) == (
            "SolverState(possible_roles=(frozenset({'Villager'}),), switches=(), path=(True,), role"
            "_counts={'Insomniac': 1, 'Villager': 2, 'Robber': 1, 'Drunk': 1, 'Wolf': 2, 'Seer': 1,"
            " 'Tanner': 1, 'Mason': 2, 'Minion': 1, 'Troublemaker': 1, 'Hunter': 1}, count_true=1)"
        )


class TestIsConsistent:
    """ Tests for the is_consistent function. """

    @staticmethod
    def test_is_consistent_on_empty_state(example_small_solverstate, example_statement):
        """ Should check a new statement against an empty SolverState for consistency. """
        start_state = algorithms.SolverState()

        result = start_state.is_consistent(example_statement)

        assert result == example_small_solverstate

    @staticmethod
    def test_invalid_state(example_statement):
        """ Should return None for inconsistent states. """
        start_state = algorithms.SolverState((frozenset({"Villager"}),) * 3, path=(True,))

        invalid_state = start_state.is_consistent(example_statement)

        assert invalid_state is None

    @staticmethod
    def test_is_consistent_on_existing_state(example_medium_solverstate):
        """
        Should check a new statement against accumulated statements for consistency.
        Should not change result.path - that is done in the switching_solver function.
        """
        possible_roles = (frozenset({"Seer"}),) + (const.ROLE_SET,) * (const.NUM_ROLES - 1)
        example_solverstate = algorithms.SolverState(possible_roles, path=(True,))
        new_statement = Statement(
            "next", ((2, frozenset({"Drunk"})),), ((SwitchPriority.DRUNK, 2, 5),)
        )

        result = example_solverstate.is_consistent(new_statement)

        assert result == example_medium_solverstate

    @staticmethod
    def test_is_consistent_deepcopy_mechanics(example_medium_solverstate):
        """
        Modifying one SolverState should not affect other SolverStates created by is_consistent.
        """
        possible_roles = (frozenset({"Seer"}),) + (const.ROLE_SET,) * (const.NUM_ROLES - 1)
        example = algorithms.SolverState(possible_roles, path=(True,))
        new_statement = Statement(
            "next", ((2, frozenset({"Drunk"})),), ((SwitchPriority.DRUNK, 2, 5),)
        )

        result = example.is_consistent(new_statement)
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
        possible_roles = (
            frozenset({"Drunk", "Minion", "Troublemaker", "Wolf", "Robber"}),
            frozenset({"Seer"}),
            frozenset({"Drunk"}),
            frozenset({"Minion"}),
            frozenset({"Drunk", "Minion", "Troublemaker", "Wolf", "Robber"}),
            frozenset({"Robber", "Minion", "Troublemaker", "Seer", "Wolf", "Drunk"}),
        )

        result = algorithms.switching_solver(medium_statement_list, (1,))

        assert result[0] == algorithms.SolverState(
            possible_roles, ((SwitchPriority.DRUNK, 2, 5),), (False, True, True, False, False)
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
    def test_get_role_counts():
        """ Should return True if there is a a dict with counts of all certain roles. """
        const.ROLE_SET = frozenset({"Wolf", "Seer", "Villager", "Robber"})
        const.ROLE_COUNTS = {"Seer": 1, "Villager": 2, "Wolf": 1, "Robber": 1}
        possible_roles_list = (
            frozenset({"Villager"}),
            frozenset({"Seer"}),
            frozenset({"Villager"}),
        ) + (const.ROLE_SET,) * 2

        result = algorithms.SolverState(possible_roles_list).get_role_counts()

        assert result == {"Seer": 0, "Villager": 0, "Wolf": 1, "Robber": 1}
