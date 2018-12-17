''' expectimax_wolf.py '''
import random
from copy import deepcopy
from algorithms import SolverState, is_consistent
from const import logger
import const

from .possible import get_expected_statements

def get_statement_expectimax(player_obj, prev_statements):
    ''' Gets Expectimax Wolf statement. '''
    expected_player_statements = get_expected_statements(player_obj.wolf_indices)

    def expectimax(statement_list, state, ind, depth=const.EXPECTIMAX_DEPTH):
        '''
        Runs expectimax on the list of statements and current state using the given depth.
        Depth: how many players to look into the future.
        '''
        if ind == const.NUM_PLAYERS or depth == 0:
            return player_obj.eval_fn(statement_list), None
        if ind == player_obj.player_index:         # Choose your own move, maximize val
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
        if not vals: return 10, None
        return sum(vals) / len(vals), None

    def _get_next_vals(statement_list, next_statements, state, ind, depth, is_evil=False):
        ''' Evaluate current state (value of consistent statements) and return values. '''
        values = []
        for statement in next_statements:
            # If you are a Wolf, let yourself be inconsistent (each state needs a value).
            new_state = state if is_evil else is_consistent(statement, state)
            if new_state:
                new_statements = deepcopy(statement_list) + [statement]
                val, _ = expectimax(new_statements, new_state, ind + 1, depth - 1)
                values.append(val)
        return values

    # Initialize start_state to use all previous statements
    possible_roles = [deepcopy(const.ROLE_SET) for i in range(const.NUM_ROLES)]
    start_state = SolverState(possible_roles, [])
    for i in range(player_obj.player_index):
        if player_obj.role in ['Wolf', 'Minion'] and i not in player_obj.wolf_indices:
            check_state = is_consistent(prev_statements[i], start_state)
            if check_state:
                start_state = check_state

    best_val, best_move = expectimax(prev_statements, start_state, player_obj.player_index)
    logger.debug('Evaluation Function Score: %f', best_val)
    return best_move
