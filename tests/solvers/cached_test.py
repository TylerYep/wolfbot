from wolfbot import solvers
from wolfbot.statements import Statement


class TestCachedSolver:
    """Tests for the cached_solver and count_roles function."""

    @staticmethod
    def test_solver_small(small_statement_list: tuple[Statement, ...]) -> None:
        """Should return a SolverState with the most likely solution."""
        result = solvers.cached_solver(small_statement_list)

        assert result == 3

    @staticmethod
    def test_solver_medium(medium_statement_list: tuple[Statement, ...]) -> None:
        """Should return a SolverState with the most likely solution."""
        result = solvers.cached_solver(medium_statement_list)

        assert result == 3

    @staticmethod
    def test_solver_large(large_statement_list: tuple[Statement, ...]) -> None:
        """Should return a SolverState with the most likely solution."""
        result = solvers.cached_solver(large_statement_list)

        assert result == 6
