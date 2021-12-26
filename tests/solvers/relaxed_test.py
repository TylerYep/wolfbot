from wolfbot import solvers
from wolfbot.enums import Role, SwitchPriority
from wolfbot.solvers import SolverState
from wolfbot.statements import Statement


class TestRelaxedSolver:
    """Tests for the relaxed_solver."""

    @staticmethod
    def test_solver_small(
        small_statement_list: tuple[Statement],
        example_small_solverstate_solved: SolverState,
    ) -> None:
        """Should return a SolverState with the most likely solution."""
        result = solvers.relaxed_solver(small_statement_list)

        # There are no desirable alternative solutions.
        assert example_small_solverstate_solved in result

    @staticmethod
    def test_solver_medium(
        medium_statement_list: tuple[Statement],
        example_medium_solverstate_solved: SolverState,
    ) -> None:
        """Should return a SolverState with the most likely solution."""
        result = solvers.relaxed_solver(medium_statement_list)

        # Ensure alternative solution was a proposed result (3 lie statements)
        assert (True, False, True, False, False) in (state.path for state in result)
        assert example_medium_solverstate_solved in result

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
        medium_statement_list: tuple[Statement, ...],
        example_medium_solved_list: tuple[SolverState, ...],
    ) -> None:
        """Should return a SolverState with the most likely solution."""
        result = solvers.relaxed_solver(medium_statement_list)

        assert len(result) == 10

    @staticmethod
    def test_solver_large(
        large_statement_list: tuple[Statement, ...],
        example_large_solverstate: SolverState,
    ) -> None:
        """Should return a SolverState with the most likely solution."""
        result = solvers.relaxed_solver(large_statement_list)

        # Ensure alternative solutions were in proposed results (4-5 lie statements)
        # 5 lie statements is not possible because a partial lie is still True to the
        # solver. These cases are handled in the prediction engine escape hatch.
        # (e.g. "I am a Seer" is False, but the action is consistent)
        assert (False, False, True, True, True, True, False, False) in (
            state.path for state in result
        )
        assert example_large_solverstate in result
