from predictions import make_predictions, print_guesses
from statements import Statement
from copy import deepcopy
import const
import random

class SolverState():
    def __init__(self, possible_roles, switches, path=[]):
        self.possible_roles = possible_roles
        self.switches = switches
        self.path = path
    def __repr__(self):
        return "\n" + str(self.possible_roles) + "\n" + str(self.path) + '\n' + str(self.switches) + '\n'


def is_consistent(statement, state):
    '''
    Returns the new state if the statement is consistent with state,
    otherwise returns False.
    State: list that contains a set of possible roles for each player.
    '''
    new_switches = deepcopy(state.switches)
    for s in statement.switches:
        new_switches.append(s)
    new_possible_roles = deepcopy(state.possible_roles)
    for proposed_ind, proposed_roles in statement.knowledge:
        intersection = proposed_roles & new_possible_roles[proposed_ind]
        if len(intersection) == 0:
            return False
        new_possible_roles[proposed_ind] = intersection
        count = count_roles(new_possible_roles)
        for proposed_role in proposed_roles:
            if count[proposed_role] > const.ROLE_COUNTS[proposed_role]:
                return False
    return SolverState(new_possible_roles, new_switches, list(state.path))

def switching_solver(statements, known_true=None):
    '''
    Returns maximal list of statements that can be true from a list
    of Statements. Handles switching characters.
    Returns a list of [True, False, True ...] values and
    the possible role sets for each player.
    '''
    possible_roles = [deepcopy(const.ROLE_SET) for i in range(const.NUM_ROLES)]
    start_state = SolverState(possible_roles, [])
    solution = [SolverState([],[])]
    # if known_true != None:
    #     temp = statements[0]
    #     statements[0] = statements[known_true]
    #     statements[known_true] = temp

    def _switch_recurse(ind, state):
        '''
        ind = index of statement being considered
        state.path = list of [True, False, True ...] values.
        '''
        nonlocal solution
        if ind == len(statements):
            if state.path.count(True) > solution.path.count(True):
                solution = [state]
            return
        truth_state = is_consistent(statements[ind], state)
        false_state = is_consistent(statements[ind].negate(), state)

        if truth_state:
            truth_state.path = list(state.path) + [True]
            _switch_recurse(ind + 1, truth_state)

        if false_state and ind != known_true:
            false_state.path = list(state.path) + [False]
            _switch_recurse(ind + 1, false_state)

    _switch_recurse(0, start_state)

    # if known_true != None:
    #     temp = solution.path[0]
    #     solution.path[0] = solution.path[known_true]
    #     solution.path[known_true] = temp
    return solution

def baseline_solver(statements, known_true=None):
    '''
    Returns maximal list of statements that can be true from a list
    of Statements.
    Does not handle switching characters.
    Returns a list of [True, False, True ...] values.
    '''
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
            newState[proposed_ind] = proposed_roles & state[proposed_ind]
            count = count_roles(newState)
            for proposed_role in proposed_roles:
                if count[proposed_role] > const.ROLE_COUNTS[proposed_role]:
                    return False
        return newState

    final_state, solution = [], []
    def _bl_solver_recurse(ind, state, path=[]):
        nonlocal solution, final_state
        if ind == len(statements):
            if path.count(True) > solution.count(True):
                solution = path
                final_state = state
            return
        truth_state = is_consistent_bl(statements[ind], state)
        false_state = is_consistent_bl(statements[ind].negate(), state)
        if truth_state:
            new_path = list(path) + [True]
            _bl_solver_recurse(ind+1, truth_state, new_path)
        if false_state:
            new_path2 = list(path) + [False]
            _bl_solver_recurse(ind+1, false_state, new_path2)

    start_state = [deepcopy(const.ROLE_SET) for i in range(const.NUM_ROLES)]
    _bl_solver_recurse(0, start_state)
    return SolverState(final_state, [], solution)

def random_solver(statements, known_true=None):
    '''
    Only works if there are no center cards.
    Returns random list of [True, False, True ...] values for each statement.
    '''
    f_inds = random.sample(range(0, const.NUM_ROLES), const.ROLE_COUNTS['Wolf'])
    path = [False if i in f_inds else True for i in range(const.NUM_PLAYERS)]
    all_possible = [deepcopy(const.ROLE_SET) for i in range(const.NUM_ROLES)]
    return SolverState(all_possible, [], path)

def count_roles(state):
    '''
    Returns a dictionary of counts for each role in [proposed roles sets].
    Only counts players in which we are sure of their role
    such as {'Villager': 3, 'Robber': 0, 'Seer': 0, 'Wolf': 1}
    '''
    count = {role: 0 for role in const.ROLE_SET}
    for s in state:
        if len(s) == 1:
            count[next(iter(s))] += 1
    return count

if __name__ == '__main__':
    statements = [
        Statement('I am a Robber and I swapped with Player 6. I am now a Drunk.', [(0, {'Robber'}), (6, {'Drunk'})], [(0, 6, 0)]),
        Statement('I am a Robber and I swapped with Player 0. I am now a Seer.', [(1, {'Robber'}), (0, {'Seer'})], [(0, 0, 1)]),
        Statement('I am a Seer and I saw that Player 3 was a Villager.', [(2, {'Seer'}), (3, {'Villager'})], []),
        Statement('I am a Villager.', [(3, {'Villager'})], []),
        Statement('I am a Mason. The other Mason is Player 5.', [(4, {'Mason'}), (5, {'Mason'})], []),
        Statement('I am a Mason. The other Mason is Player 4.', [(5, {'Mason'}), (4, {'Mason'})], []),
        Statement('I am a Drunk and I swapped with Center 1.', [(6, {'Drunk'})], [(1, 9, 6)]),
        Statement('I am a Robber and I swapped with Player 5. I am now a Seer.', [(7, {'Robber'}), (5, {'Seer'})], [(0, 5, 7)])
    ]
    solution = switching_solver(statements)
    print(solution)

    all_role_guesses = make_predictions(solution)
    print_guesses()
