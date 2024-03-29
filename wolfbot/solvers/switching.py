from __future__ import annotations

from typing import TYPE_CHECKING

from wolfbot.solvers.state import SolverState

if TYPE_CHECKING:
    from wolfbot.statements import Statement


def switching_solver(
    statements: tuple[Statement, ...], known_true: tuple[int, ...] = ()
) -> list[SolverState]:
    """
    Returns maximal list of statements that can be true from a list
    of Statements. Handles switching characters.
    Returns a list of [True, False, True ...] values and
    the possible role sets for each player.
    """
    num_statements = len(statements)

    def _switch_recurse(
        solutions: list[SolverState], state: SolverState, ind: int = 0
    ) -> None:
        """ind = index of statement being considered."""
        curr_max = solutions[0].count_true if solutions else 0
        if ind == num_statements:
            if state.count_true > curr_max:
                solutions.clear()
            if state.count_true >= curr_max:
                solutions.append(state)
            return

        if state.count_true + num_statements - ind < curr_max:
            return

        truth_state = state.is_consistent(statements[ind])
        false_state = state.is_consistent(statements[ind].negation, False)

        if truth_state is not None:
            _switch_recurse(solutions, truth_state, ind + 1)

        if false_state is not None and ind not in known_true:
            _switch_recurse(solutions, false_state, ind + 1)

    solutions: list[SolverState] = []
    _switch_recurse(solutions, SolverState())
    return solutions
