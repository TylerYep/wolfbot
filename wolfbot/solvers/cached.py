from __future__ import annotations

from typing import TYPE_CHECKING

from wolfbot.solvers.state import SolverState

if TYPE_CHECKING:
    from wolfbot.statements import Statement


def cached_solver(statements: tuple[Statement, ...]) -> int:
    """Returns max number of statements that can be true from a list of Statements."""
    num_statements = len(statements)

    def _cache_recurse(state: SolverState, ind: int = 0) -> int:
        if ind == num_statements or state is None:
            return 0
        new_state = state.is_consistent(statements[ind])
        skip_statement = _cache_recurse(state, ind + 1)
        if new_state is None:
            return skip_statement
        return max(1 + _cache_recurse(new_state, ind + 1), skip_statement)

    return _cache_recurse(SolverState())
