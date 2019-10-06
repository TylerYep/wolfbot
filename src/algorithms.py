''' algorithms.py '''
from typing import Dict, List, Optional, Set, Tuple
from copy import deepcopy

from src.statements import Statement
from src import const

class SolverState:
    '''
    Each solver returns a SolverState object with the result.
    @param path: tuple of (True, False, True ...) values.
    '''
    def __init__(self,
                 possible_roles: List[Set[str]] = None,
                 switches: Tuple[Tuple[int, int, int], ...] = (),
                 path_init: Tuple[bool] = ()):
        possible = [const.ROLE_SET]*const.NUM_ROLES if possible_roles is None else possible_roles
        self.possible_roles = tuple([frozenset(role_set) for role_set in possible])
        self.switches = switches
        self.path = path_init

    def is_valid_state(self) -> bool:
        ''' Checks for invalid state, denoted as SolverState([]). '''
        return len(self.possible_roles) != 0

    def __eq__(self, other) -> bool:
        ''' Checks for equality between SolverStates. '''
        return self.__dict__ == other.__dict__

    def __repr__(self) -> str:
        ''' Returns a String representation of a SolverState. '''
        possible = [set(roles) for roles in self.possible_roles]
        return f'SolverState({possible}, {self.switches}, {self.path})'


def is_consistent(statement: Statement, state: SolverState) -> SolverState:
    '''
    Returns the new state if the statement is consistent with state,
    otherwise returns an empty state.
    @param state: list that contains a set of possible roles for each player.
    '''
    new_switches = deepcopy(state.switches) + statement.switches
    new_possible_roles = list(deepcopy(state.possible_roles))
    for proposed_ind, proposed_roles in statement.knowledge:
        intersection = proposed_roles & new_possible_roles[proposed_ind]
        if not intersection:
            return SolverState([])
        new_possible_roles[proposed_ind] = intersection
        count = count_roles(new_possible_roles)
        for proposed_role in proposed_roles:
            if count[proposed_role] > const.ROLE_COUNTS[proposed_role]:
                return SolverState([])
    return SolverState(new_possible_roles, new_switches, state.path)


def switching_solver(statements: List[Statement],
                     known_true: Optional[int] = None) -> List[SolverState]:
    '''
    Returns maximal list of statements that can be true from a list
    of Statements. Handles switching characters.
    Returns a list of [True, False, True ...] values and
    the possible role sets for each player.
    '''
    start_state = SolverState()
    solution = [start_state]

    def _switch_recurse(ind, state) -> None:
        ''' ind = index of statement being considered '''
        nonlocal solution
        if ind == len(statements):
            prev_max, new_path_count = solution[0].path.count(True), state.path.count(True)
            if new_path_count > prev_max:
                solution = [state]
            elif new_path_count == prev_max:
                solution.append(state)
            return
        truth_state = is_consistent(statements[ind], state)
        false_state = is_consistent(statements[ind].negate(), state)

        if truth_state.is_valid_state():
            truth_state.path = state.path + (True,)
            _switch_recurse(ind + 1, truth_state)

        if false_state.is_valid_state() and ind != known_true:
            false_state.path = state.path + (False,)
            _switch_recurse(ind + 1, false_state)

    _switch_recurse(0, start_state)
    return solution


def count_roles(possible_roles_list: List[Set[str]]) -> Dict[str, int]:
    '''
    Returns a dictionary of counts for each role in [proposed roles sets].
    Only counts players in which we are sure of their role, such as:
    {'Villager': 3, 'Robber': 0, 'Seer': 0, 'Wolf': 1}
    '''
    counts_dict = {role: 0 for role in const.ROLE_SET}
    for possible_roles in possible_roles_list:
        if len(possible_roles) == 1:
            counts_dict[next(iter(possible_roles))] += 1
    return counts_dict
