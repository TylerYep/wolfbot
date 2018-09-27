''' expectimax_wolf.py '''
import random
from copy import deepcopy
from algorithms import switching_solver, SolverState, is_consistent
from predictions import make_prediction_fast
import const

from .reg_wolf import get_wolf_statements
from .possible import get_expected_statements

def get_statement_expectimax(player_index, wolf_indices, stated_roles, previous_statements):
    ''' Gets Expectimax Wolf statement. '''

    statements = get_wolf_statements(player_index, wolf_indices, stated_roles, previous_statements)
    expected_player_statements = get_expected_statements(wolf_indices)

    def eval_fn(solver_result, predictions):
        '''
        Evaluates a complete or incomplete game.
        # wolves in a positions - # of ones that are actually wolves, size of set
        '''
        val = 10
        if not predictions: return -10
        for wolfi in wolf_indices:
            if predictions[wolfi] == 'Wolf':
                val -= 5
            if 'Wolf' in solver_result.possible_roles[wolfi]:
                val -= 5
        return val

    def expectimax(statement_list, state, ind, depth=None):
        ''' Runs expectimax on the list of statements and current state using the given depth. '''
        if ind == const.NUM_PLAYERS or depth == 0:
            solver_result = random.choice(switching_solver(statement_list))
            predictions = make_prediction_fast(solver_result)
            return eval_fn(solver_result, predictions), None
        if ind == player_index:              # Choose your own move, maximize val
            vals = _get_next_vals(statement_list, statements, state, ind, depth, True)
            best_move = statements[vals.index(max(vals))]
            if not vals: return -5, super.getNextStatement()
            return max(vals), best_move

        # Get expected value of remaining statements
        assert const.EXPECTIMAX_DEPTH != 1
        indices = random.sample(range(len(expected_player_statements[ind])), const.BRANCH_FACTOR * player_index)
        trimmed_statements = [expected_player_statements[ind][i] for i in sorted(indices)]
        vals = _get_next_vals(statement_list, trimmed_statements, state, ind, depth)
        if not vals: return 10, None
        return sum(vals) / len(vals), None

    def _get_next_vals(statement_list, actions, state, ind, depth, is_wolf=False):
        ''' Evaluate current state (value of consistent statements) and return values. '''
        values = []
        for statement in actions:
            # If you're a Wolf, let yourself be inconsistent (each state needs a value)
            if is_wolf: new_state = state
            else: new_state = is_consistent(statement, state)
            if new_state:
                new_statements = deepcopy(statement_list) + [statement]
                values.append(expectimax(new_statements, new_state, ind + 1, depth - 1))
        return [v[0] for v in values]

    possible_roles = [deepcopy(const.ROLE_SET) for i in range(const.NUM_ROLES)]
    start_state = SolverState(possible_roles, [])
    for i in range(player_index):
        if i not in wolf_indices:
            st = is_consistent(previous_statements[i], start_state)
            if st: start_state = st
    _, best_move = expectimax(previous_statements, start_state, player_index, const.EXPECTIMAX_DEPTH)
    return best_move
