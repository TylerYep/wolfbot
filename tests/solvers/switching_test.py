from wolfbot import solvers
from wolfbot.enums import Role, SwitchPriority
from wolfbot.solvers import SolverState
from wolfbot.statements import Statement


class TestSwitchingSolver:
    """Tests for the switching_solver."""

    @staticmethod
    def test_solver_small(
        small_statement_list: tuple[Statement],
        example_small_solverstate_solved: SolverState,
    ) -> None:
        """Should return a SolverState with the most likely solution."""
        result = solvers.switching_solver(small_statement_list)

        assert result[0] == example_small_solverstate_solved

    @staticmethod
    def test_solver_medium(
        medium_statement_list: tuple[Statement],
        example_medium_solverstate_solved: SolverState,
    ) -> None:
        """Should return a SolverState with the most likely solution."""
        result = solvers.switching_solver(medium_statement_list)

        assert result[0] == example_medium_solverstate_solved

    @staticmethod
    def test_solver_medium_known_true(
        medium_statement_list: tuple[Statement, ...],
        medium_game_roles: tuple[Role, ...],
    ) -> None:
        """Should return a SolverState with the most likely solution."""
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
        medium_statement_list: tuple[Statement, ...],
        example_medium_solved_list: tuple[SolverState, ...],
    ) -> None:
        """Should return a SolverState with the most likely solution."""
        result = solvers.switching_solver(medium_statement_list)

        assert tuple(result) == example_medium_solved_list

    @staticmethod
    def test_solver_large(
        large_statement_list: tuple[Statement, ...],
        example_large_solverstate: SolverState,
    ) -> None:
        """Should return a SolverState with the most likely solution."""
        result = solvers.switching_solver(large_statement_list)

        assert result[0] == example_large_solverstate
