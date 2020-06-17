""" expectimax.py """
import random
from typing import Any, Dict, List, Optional, Tuple

from src import const
from src.const import logger
from src.solvers import SolverState
from src.solvers import switching_solver as solver
from src.statements import Statement


def expectimax(
    player_obj: Any,
    prev_statements: Tuple[Statement, ...],
    expected_player_statements: Dict[int, List[Statement]],
) -> Statement:
    """ Expectimax algorithm. """

    def _expectimax(
        statement_list: Tuple[Statement, ...],
        state: SolverState,
        ind: int,
        depth: int = const.EXPECTIMAX_DEPTH,
    ) -> Tuple[float, Optional[Statement]]:
        """
        Runs expectimax on the list of statements and current state using the given depth.
        Depth: how many players to look into the future.
        """
        if ind == const.NUM_PLAYERS or depth == 0:
            return player_obj.eval_fn(statement_list), None

        if ind == player_obj.player_index:  # Choose your own move, maximize val
            vals = _get_next_vals(statement_list, player_obj.statements, state, ind, depth, True)
            max_value = max(vals)
            best_indices = [index for index, value in enumerate(vals) if value == max_value]
            best_move = player_obj.statements[random.choice(best_indices)]
            # if not vals: return -5, super.get_statement()     # TODO is vals ever empty?
            return max_value, best_move

        assert const.EXPECTIMAX_DEPTH != 1
        # Randomly choose a subset of the expected player statements and get expected value
        # of remaining statements. Adjust sample size based on const.BRANCH_FACTOR.
        sample_size = const.BRANCH_FACTOR * player_obj.player_index
        indices = random.sample(range(len(expected_player_statements[ind])), sample_size)
        trimmed_statements = [expected_player_statements[ind][i] for i in sorted(indices)]
        vals = _get_next_vals(statement_list, trimmed_statements, state, ind, depth)
        if not vals:
            return 10, None
        return sum(vals) / len(vals), None

    def _get_next_vals(
        statement_list: Tuple[Statement, ...],
        next_statements: List[Statement],
        state: SolverState,
        ind: int,
        depth: int,
        is_evil: bool = False,
    ) -> List[float]:
        """ Evaluate current state (value of consistent statements) and return values. """
        values = []
        for statement in next_statements:
            # If you are a Wolf, let yourself be inconsistent (each state needs a value).
            new_state = state if is_evil else state.is_consistent(statement)
            if new_state is not None:
                new_statements = statement_list + (statement,)
                val, _ = _expectimax(new_statements, new_state, ind + 1, depth - 1)
                values.append(val)
        return values

    # Initialize start_state to use all previous statements
    start_state = random.choice(solver(prev_statements))
    best_val, best_move = _expectimax(tuple(prev_statements), start_state, player_obj.player_index)
    logger.debug(f"[Hidden] Evaluation Function Score: {best_val}")
    assert best_move is not None
    return best_move
