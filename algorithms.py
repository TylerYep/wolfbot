import const
import copy
from statements import Statement
import pickle
# import pdb; pdb.set_trace()

def count_roles(state):
    '''
    Returns a dictionary of counts for each role in a state.
    Only counts players in which we are sure of their role
    such as {'Villager': 3, 'Robber': 0, 'Seer': 0, 'Wolf': 1}
    '''
    count = {role: 0 for role in const.ROLE_SET}
    for s in state:
        if len(s) == 1:
            for role in s: # There's only one??
                count[role] += 1
    return count

#x = [{'Villager', 'Wolf'},{'Villager'},{'Villager'},{'Wolf'}]
# print(count_roles(x))

def is_consistent(statement, state):
    '''
    Returns the new state if the statement is consistent with state.
    otherwise returns False.
    State: list that contains a set of possible roles for each player.
    '''
    newState = copy.deepcopy(state)
    for proposed_ind, proposed_roles in statement.knowledge:
        if not (proposed_roles & state[proposed_ind]):
            return False
        newState = copy.deepcopy(newState)
        newState[proposed_ind] = proposed_roles
        count = count_roles(newState)
        for proposed_role in proposed_roles:
            if count[proposed_role] > const.ROLE_COUNTS[proposed_role]:
                return False
                # WE CAN ADD MORE CHECKS
    return newState

def baseline_solver(statements, n_players):
    def _bl_solver_recurse(ind, state):
        if ind == len(statements):
            return 0
        else:
            # t_count, f_count = float('-inf'), float('-inf')
            t_count, f_count = 0, 0
            truth_state = is_consistent(statements[ind], state)
            false_state = is_consistent(statements[ind].negate(), state)
            # print(truth_state, false_state)
            if truth_state:
                t_count = 1 + _bl_solver_recurse(ind+1, truth_state)
            if false_state:
                f_count = _bl_solver_recurse(ind+1, false_state)
            return max(f_count, t_count)

    state = [copy.deepcopy(const.ROLE_SET) for i in range(n_players)]

    return _bl_solver_recurse(0, state)

# V V W S W V
if __name__ == '__main__':
    statements = [
        Statement('Player 0: I am a Villager', [(0, {'Villager'})]),
        Statement('Player 1: I am a Villager', [(1, {'Villager'})]),
        Statement('Player 2: I am a Seer and I saw that Player 3 was a Wolf', [(2, {'Seer'}), (3, {'Wolf'})]),
        Statement('Player 3: I am a Seer and I saw that Player 5 was a Villager', [(3, {'Seer'}), (5, {'Villager'})]),
        Statement('Player 4: I am a Seer and I saw that Player 3 was a Villager', [(4, {'Seer'}), (3, {'Villager'})]),
        Statement('Player 5: I am a Villager', [(5, {'Villager'})]),
        ]
    print(baseline_solver(statements, 6))
    # state = [{'Villager'}, {'Villager'}, {'Villager'}, {'Villager', 'Seer', 'Wolf'}, {'Villager', 'Seer', 'Wolf'}, {'Villager', 'Seer', 'Wolf'}]
    # is_consistent(Statement('Player 3: I am a Seer and I saw that Player 2 was a Villager', [(3, {'Seer'}), (2, {'Villager'})]), state)
