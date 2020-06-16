""" expectimax_wolf.py """
import random
from typing import Any, Dict, List, Optional, Tuple

from src import const, roles
from src.algorithms import SolverState
from src.const import logger
from src.statements import Statement


def get_expected_statements() -> Dict[int, List[Statement]]:
    """
    Gets all possible statements that can be made by a village player from any index.
    Used to find the 'expect' part of the Expectimax algorithm.
    Returns set of statement objects.
    """
    possible: Dict[int, List[Statement]] = {}
    for player_index in range(const.NUM_PLAYERS):
        statements = []
        village_roles = sorted(tuple(const.VILLAGE_ROLES))
        random.shuffle(village_roles)
        for role in village_roles:
            role_obj = roles.get_role_obj(role)
            statements += role_obj.get_all_statements(player_index)
        possible[player_index] = statements
    return possible


def get_statement_expectimax(player_obj: Any, prev_statements: List[Statement]) -> Statement:
    """ Gets Expectimax Wolf statement. """
    expected_player_statements = get_expected_statements()

    def expectimax(
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
            best_indices = [index for index, value in enumerate(vals) if value == max(vals)]
            best_move = player_obj.statements[random.choice(best_indices)]
            # if not vals: return -5, super.get_statement()     # is vals ever empty?
            return max(vals), best_move

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
                val, _ = expectimax(new_statements, new_state, ind + 1, depth - 1)
                values.append(val)
        return values

    # Initialize start_state to use all previous statements
    start_state = SolverState()
    for i in range(player_obj.player_index):
        if player_obj.role in ("Wolf", "Minion") and i not in player_obj.wolf_indices:
            check_state = start_state.is_consistent(prev_statements[i])
            if check_state is not None:
                start_state = check_state

    if const.MULTI_STATEMENT:
        player_obj.statements = [
            x for x in player_obj.statements if x.priority > player_obj.prev_priority
        ]
    best_val, best_move = expectimax(tuple(prev_statements), start_state, player_obj.player_index)
    logger.debug(f"Evaluation Function Score: {best_val}")
    assert best_move is not None
    player_obj.prev_priority = best_move.priority
    return best_move
