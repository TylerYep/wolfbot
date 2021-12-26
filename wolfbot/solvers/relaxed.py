from __future__ import annotations

import heapq

from wolfbot.solvers.state import SolverState
from wolfbot.statements import Statement


def relaxed_solver(
    statements: tuple[Statement, ...], known_true: tuple[int, ...] = ()
) -> list[SolverState]:
    """
    Does not assume the first largest subset of correct statements is the solution.

    Returns maximal list of statements that can be true from a list
    of Statements. Handles switching characters.
    Returns a list of [True, False, True ...] values and
    the possible role sets for each player.
    """
    num_statements = len(statements)
    max_avg = 10  # len(const.VILLAGE_ROLES)

    def _relaxed_recurse(
        solutions: list[SolverState], state: SolverState, ind: int = 0
    ) -> None:
        """ind = index of statement being considered."""
        if ind == num_statements:
            # if len(solutions) == 0 or (
            #     state.count_true
            #     >= sum(x.count_true for x in solutions) / len(solutions)
            # ):
            num_sols = len(solutions)
            if num_sols < max_avg:
                heapq.heappush(solutions, state)
            elif num_sols == max_avg:
                heapq.heappushpop(solutions, state)
            return

        truth_state = state.is_consistent(statements[ind])
        false_state = state.is_consistent(statements[ind].negation, False)

        if truth_state is not None:
            _relaxed_recurse(solutions, truth_state, ind + 1)

        if false_state is not None and ind not in known_true:
            _relaxed_recurse(solutions, false_state, ind + 1)

    solutions: list[SolverState] = []
    _relaxed_recurse(solutions, SolverState())
    return solutions
