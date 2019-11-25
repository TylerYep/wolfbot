''' algorithms.py '''
from typing import FrozenSet, List, Optional, Set, Tuple, Union

from src.statements import Statement
from src.const import Priority
from src import const

class SolverState:
    '''
    Each solver returns a SolverState object with the result.
    @param path: tuple of (True, False, True ...) values.
    '''

    def __init__(self,
                 possible_roles: Union[List, List[Set[str]], List[FrozenSet[str]]] = None,
                 switches: Tuple[Tuple[Priority, int, int], ...] = (),
                 path_init: Tuple[bool, ...] = ()):
        possible = [const.ROLE_SET] * const.NUM_ROLES if possible_roles is None else possible_roles
        self.possible_roles = tuple([frozenset(role_set) for role_set in possible])
        self.switches = switches
        self.path = path_init

    def is_valid_state(self) -> bool:
        ''' Checks for invalid state, denoted as SolverState([]). '''
        return bool(self.possible_roles)

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
    new_switches = state.switches + statement.switches
    new_possible_roles = list(state.possible_roles)
    for proposed_ind, proposed_roles in statement.knowledge:
        intersection = proposed_roles & new_possible_roles[proposed_ind]
        if not intersection:
            return SolverState([])
        new_possible_roles[proposed_ind] = intersection
        if not check_role_counts(new_possible_roles, proposed_roles):
            return SolverState([])
    return SolverState(new_possible_roles, new_switches, state.path)


def cached_solver(statements: Tuple[Statement, ...]) -> int:
    ''' Returns maximal number of statements that can be true from a list of Statements. '''
    def _cache_recurse(ind, state) -> int:
        if ind == len(statements) or not state.is_valid_state():
            return 0
        new_state = is_consistent(statements[ind], state)
        if not new_state.is_valid_state():
            return _cache_recurse(ind + 1, state)
        return max(1 + _cache_recurse(ind + 1, new_state), _cache_recurse(ind + 1, state))

    return _cache_recurse(0, SolverState())


def switching_solver(statements: Tuple[Statement, ...],
                     known_true: Optional[int] = None) -> List[SolverState]:
    '''
    Returns maximal list of statements that can be true from a list
    of Statements. Handles switching characters.
    Returns a list of [True, False, True ...] values and
    the possible role sets for each player.
    '''
    start_state = SolverState()
    solution = [start_state]

    def _switch_recurse(ind: int, state: SolverState) -> None:
        ''' ind = index of statement being considered. '''
        nonlocal solution
        curr_path_count = state.path.count(True)
        prev_max = solution[0].path.count(True)
        if ind == len(statements):
            if curr_path_count > prev_max:
                solution = [state]
                prev_max = curr_path_count
            elif curr_path_count == prev_max:
                solution.append(state)
            return

        if curr_path_count + (len(statements) - ind) < prev_max:
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


def check_role_counts(possible_roles_list: List[FrozenSet[str]],
                      proposed_roles: FrozenSet[str]) -> bool:
    '''
    Returns a dictionary of counts for each role in [proposed roles sets].
    Only counts players in which we are sure of their role, such as:
    {'Villager': 3, 'Robber': 0, 'Seer': 0, 'Wolf': 1}
    '''
    counts_dict = dict(const.ROLE_COUNTS)
    for possible_roles in possible_roles_list:
        if len(possible_roles) == 1:
            [single_role] = possible_roles
            if single_role in proposed_roles:
                if counts_dict[single_role] == 0:
                    return False
                counts_dict[single_role] -= 1
    return True
