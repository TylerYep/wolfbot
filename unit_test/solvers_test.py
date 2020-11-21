""" solvers_test.py """
from typing import Tuple

from conftest import set_roles
from src import const, solvers
from src.const import Role, SwitchPriority
from src.solvers import SolverState
from src.statements import Statement


class TestSolverState:
    """ Tests for the SolverState class. """

    @staticmethod
    def test_constructor() -> None:
        """ Should initialize a SolverState. """
        result = SolverState((frozenset({Role.VILLAGER}),), path=(True,))

        assert isinstance(result, SolverState)

    @staticmethod
    def test_eq(example_small_solverstate: SolverState) -> None:
        """ Should be able to compare two identical SolverStates. """
        possible_roles = (
            frozenset({Role.SEER}),
            frozenset({Role.ROBBER, Role.VILLAGER, Role.SEER}),
            frozenset({Role.ROBBER}),
        )
        switches = ((SwitchPriority.ROBBER, 2, 0),)
        path = (True,)

        result = SolverState(possible_roles, switches, path)

        assert result == example_small_solverstate

    @staticmethod
    def test_get_role_counts() -> None:
        """
        Should return True if there is a a dict with counts of all certain roles.
        """
        set_roles(Role.WOLF, Role.SEER, Role.VILLAGER, Role.ROBBER, Role.VILLAGER)
        possible_roles_list = (
            frozenset({Role.VILLAGER}),
            frozenset({Role.SEER}),
            frozenset({Role.VILLAGER}),
        ) + (const.ROLE_SET,) * 2

        result = SolverState(possible_roles_list).get_role_counts()

        assert result == {Role.SEER: 0, Role.VILLAGER: 0, Role.WOLF: 1, Role.ROBBER: 1}


class TestIsConsistent:
    """ Tests for the is_consistent function. """

    @staticmethod
    def test_is_consistent_on_empty_state(
        example_small_solverstate: SolverState, example_statement: Statement
    ) -> None:
        """
        Should check a new statement against an empty SolverState for consistency.
        """
        start_state = SolverState()

        result = start_state.is_consistent(example_statement)

        assert result == example_small_solverstate

    @staticmethod
    def test_invalid_state(example_statement: Statement) -> None:
        """ Should return None for inconsistent states. """
        start_state = SolverState((frozenset({Role.VILLAGER}),) * 3, path=(True,))

        invalid_state = start_state.is_consistent(example_statement)

        assert invalid_state is None

    @staticmethod
    def test_is_consistent_on_existing_state(
        example_medium_solverstate: SolverState,
    ) -> None:
        """
        Should check a new statement against accumulated statements for consistency.
        Should not change result.path - that is done in the switching_solver function.
        """
        possible_roles = (frozenset({Role.SEER}),) + (const.ROLE_SET,) * (
            const.NUM_ROLES - 1
        )
        example_solverstate = SolverState(possible_roles, path=(True,))
        new_statement = Statement(
            "next", ((2, frozenset({Role.DRUNK})),), ((SwitchPriority.DRUNK, 2, 5),)
        )

        result = example_solverstate.is_consistent(new_statement)

        assert result == example_medium_solverstate

    @staticmethod
    def test_is_consistent_deepcopy_mechanics(
        example_medium_solverstate: SolverState,
    ) -> None:
        """
        Modifying one SolverState should not affect
        other SolverStates created by is_consistent.
        """
        possible_roles = (frozenset({Role.SEER}),) + (const.ROLE_SET,) * (
            const.NUM_ROLES - 1
        )
        example = SolverState(possible_roles, path=(True,))
        new_statement = Statement(
            "next", ((2, frozenset({Role.DRUNK})),), ((SwitchPriority.DRUNK, 2, 5),)
        )

        result = example.is_consistent(new_statement)
        example.possible_roles += (frozenset({Role.NONE}),)
        example.switches += ((SwitchPriority.DRUNK, 5, 5),)
        example.possible_roles = (example.possible_roles[0] & {Role.NONE},)

        assert result == example_medium_solverstate


class TestCachedSolver:
    """ Tests for the cached_solver and count_roles function. """

    @staticmethod
    def test_solver_small(small_statement_list: Tuple[Statement, ...]) -> None:
        """ Should return a SolverState with the most likely solution. """
        result = solvers.cached_solver(small_statement_list)

        assert result == 3

    @staticmethod
    def test_solver_medium(medium_statement_list: Tuple[Statement, ...]) -> None:
        """ Should return a SolverState with the most likely solution. """
        result = solvers.cached_solver(medium_statement_list)

        assert result == 3

    @staticmethod
    def test_solver_large(large_statement_list: Tuple[Statement, ...]) -> None:
        """ Should return a SolverState with the most likely solution. """
        result = solvers.cached_solver(large_statement_list)

        assert result == 6


class TestSwitchingSolver:
    """ Tests for the switching_solver. """

    @staticmethod
    def test_solver_small(
        small_statement_list: Tuple[Statement],
        example_small_solverstate_solved: SolverState,
    ) -> None:
        """ Should return a SolverState with the most likely solution. """
        result = solvers.switching_solver(small_statement_list)

        assert result[0] == example_small_solverstate_solved

    @staticmethod
    def test_solver_medium(
        medium_statement_list: Tuple[Statement],
        example_medium_solverstate_solved: SolverState,
    ) -> None:
        """ Should return a SolverState with the most likely solution. """
        result = solvers.switching_solver(medium_statement_list)

        assert result[0] == example_medium_solverstate_solved

    @staticmethod
    def test_solver_medium_known_true(
        medium_statement_list: Tuple[Statement, ...],
        medium_game_roles: Tuple[Role, ...],
    ) -> None:
        """ Should return a SolverState with the most likely solution. """
        possible_roles = (
            frozenset(
                {Role.DRUNK, Role.MINION, Role.TROUBLEMAKER, Role.WOLF, Role.ROBBER}
            ),
            frozenset({Role.SEER}),
            frozenset({Role.DRUNK}),
            frozenset({Role.MINION}),
            frozenset(
                {Role.DRUNK, Role.MINION, Role.TROUBLEMAKER, Role.WOLF, Role.ROBBER}
            ),
            frozenset(
                {
                    Role.ROBBER,
                    Role.MINION,
                    Role.TROUBLEMAKER,
                    Role.SEER,
                    Role.WOLF,
                    Role.DRUNK,
                }
            ),
        )

        result = solvers.switching_solver(medium_statement_list, (1,))

        assert result[0] == SolverState(
            possible_roles,
            ((SwitchPriority.DRUNK, 2, 5),),
            (False, True, True, False, False),
        )

    @staticmethod
    def test_solver_medium_multiple_solns(
        medium_statement_list: Tuple[Statement, ...],
        example_medium_solved_list: Tuple[SolverState, ...],
    ) -> None:
        """ Should return a SolverState with the most likely solution. """
        result = solvers.switching_solver(medium_statement_list)

        assert tuple(result) == example_medium_solved_list

    @staticmethod
    def test_solver_large(
        large_statement_list: Tuple[Statement, ...],
        example_large_solverstate: SolverState,
    ) -> None:
        """ Should return a SolverState with the most likely solution. """
        result = solvers.switching_solver(large_statement_list)

        assert result[0] == example_large_solverstate


class TestRelaxedSolver:
    """ Tests for the relaxed_solver. """

    @staticmethod
    def test_solver_small(
        small_statement_list: Tuple[Statement],
        example_small_solverstate_solved: SolverState,
    ) -> None:
        """ Should return a SolverState with the most likely solution. """
        result = solvers.relaxed_solver(small_statement_list)

        # There are no desirable alternative solutions.
        assert example_small_solverstate_solved in result

    @staticmethod
    def test_solver_medium(
        medium_statement_list: Tuple[Statement],
        example_medium_solverstate_solved: SolverState,
    ) -> None:
        """ Should return a SolverState with the most likely solution. """
        result = solvers.relaxed_solver(medium_statement_list)

        # Ensure alternative solution was a proposed result (3 lie statements)
        assert (True, False, True, False, False) in (state.path for state in result)
        assert example_medium_solverstate_solved in result

    @staticmethod
    def test_solver_medium_known_true(
        medium_statement_list: Tuple[Statement, ...],
        medium_game_roles: Tuple[Role, ...],
    ) -> None:
        """ Should return a SolverState with the most likely solution. """
        possible_roles = (
            frozenset(
                {Role.DRUNK, Role.MINION, Role.TROUBLEMAKER, Role.WOLF, Role.ROBBER}
            ),
            frozenset({Role.SEER}),
            frozenset({Role.DRUNK}),
            frozenset({Role.MINION}),
            frozenset(
                {Role.DRUNK, Role.MINION, Role.TROUBLEMAKER, Role.WOLF, Role.ROBBER}
            ),
            frozenset(
                {
                    Role.ROBBER,
                    Role.MINION,
                    Role.TROUBLEMAKER,
                    Role.SEER,
                    Role.WOLF,
                    Role.DRUNK,
                }
            ),
        )

        result = solvers.relaxed_solver(medium_statement_list, (1,))

        assert (
            SolverState(
                possible_roles,
                ((SwitchPriority.DRUNK, 2, 5),),
                (False, True, True, False, False),
            )
            in result
        )

    @staticmethod
    def test_solver_medium_multiple_solns(
        medium_statement_list: Tuple[Statement, ...],
        example_medium_solved_list: Tuple[SolverState, ...],
    ) -> None:
        """ Should return a SolverState with the most likely solution. """
        result = solvers.relaxed_solver(medium_statement_list)

        assert len(result) == 10

    @staticmethod
    def test_solver_large(
        large_statement_list: Tuple[Statement, ...],
        example_large_solverstate: SolverState,
    ) -> None:
        """ Should return a SolverState with the most likely solution. """
        result = solvers.relaxed_solver(large_statement_list)

        # Ensure alternative solutions were in proposed results (4-5 lie statements)
        # 5 lie statements is not possible because a partial lie is still True to the
        # solver. These cases are handled in the prediction engine escape hatch.
        # (e.g. "I am a Seer" is False, but the action is consistent)
        assert (False, False, True, True, True, True, False, False) in (
            state.path for state in result
        )
        assert example_large_solverstate in result
