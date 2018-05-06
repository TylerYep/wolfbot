from statements import Statement
from copy import deepcopy
import const
import random

def is_consistent(statement, state):
    '''
    Returns the new state if the statement is consistent with state,
    otherwise returns False.
    State: list that contains a set of possible roles for each player.
    '''
    newState = SolverState(state.index, deepcopy(state.possible_roles), dict(state.switch_dict), list(state.path))
    for proposed_ind, proposed_roles in statement.knowledge:
        if not (proposed_roles & state.possible_roles[proposed_ind]):
            return False
        newState = SolverState(state.index, deepcopy(state.possible_roles), dict(state.switch_dict), list(state.path))
        newState.possible_roles[proposed_ind] = proposed_roles & state.possible_roles[proposed_ind]
        count = count_roles(newState)
        for proposed_role in proposed_roles:
            if count[proposed_role] > const.ROLE_COUNTS[proposed_role]:
                return False
                # ADD MORE CHECKS
    return newState

class SolverState():
    def __init__(self, index, possible_roles, switch_dict, path=[]):
        self.index = index
        self.possible_roles = possible_roles
        self.switch_dict = switch_dict
        self.path = path
    def __repr__(self):
        return "\n<" + str(self.possible_roles) + ">\n"


def switching_solver(statements, n_players=const.NUM_ROLES):
    '''
    Returns maximal list of statements that can be true from a list
    of Statements. Handles switching characters.
    Returns a list of [True, False, True ...] values and
    the possible role sets for each player.
    '''
    possible_rols = [deepcopy(const.ROLE_SET) for i in range(n_players)]
    switch_dict = {a:a for a in range(const.NUM_ROLES)}
    start_state = SolverState(0, possible_rols, switch_dict)
    final_state = []
    solution = []

    def _switch_recurse(state):
        '''
        ind: index of statement being considered
        state = list of possible role sets for each player
        path = list of [True, False, True ...] values.
        '''
        nonlocal solution, final_state
        if state.index == len(statements):
            if state.path.count(True) > solution.count(True):
                solution = list(state.path)
                new_possible = deepcopy(state.possible_roles)
                final_state = SolverState(state.index, new_possible, dict(state.switch_dict), list(state.path))
            return
        truth_state = is_consistent(statements[state.index], state)
        false_state = is_consistent(statements[state.index].negate(), state)
        if truth_state:
            new_path = list(state.path)
            new_path.append(True)
            new_possible1 = deepcopy(truth_state.possible_roles)
            new_state1 = SolverState(state.index+1, new_possible1, dict(state.switch_dict), new_path)
            _switch_recurse(new_state1)
        if false_state:
            new_path2 = list(state.path)
            new_path2.append(False)
            new_possible2 = deepcopy(false_state.possible_roles)
            new_state2 = SolverState(state.index+1, new_possible2, dict(state.switch_dict), new_path2)
            _switch_recurse(new_state2)
    _switch_recurse(start_state)
    return solution, final_state.possible_roles

def is_consistent_bl(statement, state):
    '''
    Returns the new state if the statement is consistent with state.
    otherwise returns False.
    State: list that contains a set of possible roles for each player.
    '''
    newState = deepcopy(state)
    for proposed_ind, proposed_roles in statement.knowledge:
        if not (proposed_roles & state[proposed_ind]):
            return False
        newState = deepcopy(newState)
        newState[proposed_ind] = proposed_roles & state[proposed_ind]
        count = count_roles(newState)
        for proposed_role in proposed_roles:
            if count[proposed_role] > const.ROLE_COUNTS[proposed_role]:
                return False
                # ADD MORE CHECKS
    return newState

def baseline_solver(statements, n_players=const.NUM_ROLES):
    '''
    Returns maximal list of statements that can be true from a list
    of Statements.
    Does not handle switching characters.
    Returns a list of [True, False, True ...] values.
    '''
    solution = []
    def _bl_solver_recurse(ind, state, path=[]):
        nonlocal solution
        if ind == len(statements):
            if path.count(True) > solution.count(True):
                solution = path
            return
        truth_state = is_consistent_bl(statements[ind], state)
        false_state = is_consistent_bl(statements[ind].negate(), state)
        new_path, new_path2 = [], []
        if truth_state:
            new_path = list(path)
            new_path.append(True)
            _bl_solver_recurse(ind+1, truth_state, new_path)
        if false_state:
            new_path2 = list(path)
            new_path2.append(False)
            _bl_solver_recurse(ind+1, false_state, new_path2)

    start_state = [deepcopy(const.ROLE_SET) for i in range(n_players)]
    _bl_solver_recurse(0, start_state)
    return solution

def random_solver(statements, n_players=const.NUM_PLAYERS):
    '''
    Only works if there are no center cards.
    Returns random list of [True, False, True ...] values for each statement.
    '''
    f_inds = random.sample(range(0, const.NUM_ROLES), const.ROLE_COUNTS['Wolf'])
    return [False if i in f_inds else True for i in range(n_players)]

def count_roles(state):
    '''
    Returns a dictionary of counts for each role in a state.
    Only counts players in which we are sure of their role
    such as {'Villager': 3, 'Robber': 0, 'Seer': 0, 'Wolf': 1}
    '''
    count = {role: 0 for role in const.ROLE_SET}
    for s in state.possible_roles:
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
