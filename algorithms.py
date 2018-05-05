from statements import Statement
import const
import copy
import random

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
        newState[proposed_ind] = proposed_roles & state[proposed_ind]
        count = count_roles(newState)
        for proposed_role in proposed_roles:
            if count[proposed_role] > const.ROLE_COUNTS[proposed_role]:
                return False
                # ADD MORE CHECKS
    return newState

def switching_solver(statements, n_players=const.NUM_ROLES):
    '''
    Returns maximal list of statements that can be true from a list
    of Statements.
    Handles switching characters.
    Outputs a list of [True, False, True ...] values.
    '''
    solution = []
    return solution

def baseline_solver(statements, n_players=const.NUM_ROLES):
    '''
    Returns maximal list of statements that can be true from a list
    of Statements.
    Does not handle switching characters.
    Outputs a list of [True, False, True ...] values.
    '''
    solution = []
    def _bl_solver_recurse(ind, state, path=[]):
        nonlocal solution
        if ind == len(statements):
            if path.count(True) > solution.count(True): solution = path
            return
        t_count, f_count = 0, 0
        truth_state = is_consistent(statements[ind], state)
        false_state = is_consistent(statements[ind].negate(), state)
        new_path, new_path2 = [], []
        if truth_state:
            new_path = list(path)
            new_path.append(True)
            t_count = _bl_solver_recurse(ind+1, truth_state, new_path)
        if false_state:
            new_path2 = list(path)
            new_path2.append(False)
            f_count = _bl_solver_recurse(ind+1, false_state, new_path2)

    start_state = [copy.deepcopy(const.ROLE_SET) for i in range(n_players)]
    _bl_solver_recurse(0, start_state)
    return solution

def random_solver(statements, n_players=const.NUM_PLAYERS):
    '''
    Only works if there are no center cards.
    Returns random list of [True, False, True ...] values for each statement.
    '''
    # assert const.NUM_CENTER == 0
    f_inds = random.sample(range(0, const.NUM_ROLES), const.ROLE_COUNTS['Wolf'])
    return [False if i in f_inds else True for i in range(n_players)]

def count_roles(state):
    '''
    Returns a dictionary of counts for each role in a state.
    Only counts players in which we are sure of their role
    such as {'Villager': 3, 'Robber': 0, 'Seer': 0, 'Wolf': 1}
    '''
    count = {role: 0 for role in const.ROLE_SET}
    for s in state:
        # Get only element of s
        if len(s) == 1:
            count[next(iter(s))] += 1
    return count

if __name__ == '__main__':
    statements = [
        Statement('Player 0: I am a Villager', [(0, {'Villager'})]),
        Statement('Player 1: I am a Villager', [(1, {'Villager'})]),
        Statement('Player 2: I am a Seer and I saw that Player 3 was a Wolf', [(2, {'Seer'}), (3, {'Wolf'})]),
        Statement('Player 3: I am a Seer and I saw that Player 5 was a Villager', [(3, {'Seer'}), (5, {'Villager'})]),
        Statement('Player 4: I am a Seer and I saw that Player 3 was a Villager', [(4, {'Seer'}), (3, {'Villager'})]),
        Statement('Player 5: I am a Villager', [(5, {'Villager'})]),
    ]
    print(random_solver(statements, 6))
