from __future__ import annotations

import random
from typing import Any

from wolfbot import const
from wolfbot.solvers import SolverState
from wolfbot.statements import Statement


def expectimax(
    player_obj: Any,
    expected_statements: dict[int, tuple[Statement, ...]],
    statement_list: tuple[Statement, ...],
    state: SolverState,
    ind: int,
) -> tuple[float, Statement | None]:
    """
    Runs expectimax on the list of statements and current state up to a max depth.
    """
    if (
        ind == const.NUM_PLAYERS
        or ind - player_obj.player_index == const.EXPECTIMAX_DEPTH
    ):
        return player_obj.eval_fn(statement_list), None

    next_statements = player_obj.statements

    # Randomly choose a subset of the expected player statements and get expected value
    # of remaining statements. Adjust sample size based on const.BRANCH_FACTOR.
    if ind != player_obj.player_index:
        sample_size = const.BRANCH_FACTOR * player_obj.player_index
        indices = random.sample(range(len(expected_statements[ind])), sample_size)
        next_statements = [expected_statements[ind][i] for i in sorted(indices)]

    # Evaluate current state (value of consistent statements) and return values.
    vals = []
    for statement in next_statements:
        # If you are a Wolf, let yourself be inconsistent (each state needs a value).
        new_state = state if player_obj.is_evil() else state.is_consistent(statement)
        if new_state is not None:
            val, _ = expectimax(
                player_obj,
                expected_statements,
                statement_list + (statement,),
                new_state,
                ind + 1,
            )
            vals.append(val)

    if not vals:
        return 10, None

    # Choose your own move to maximize val
    if ind == player_obj.player_index:
        max_value = max(vals)
        best_indices = [index for index, value in enumerate(vals) if value == max_value]
        return max_value, player_obj.statements[random.choice(best_indices)]

    return sum(vals) / len(vals), None
