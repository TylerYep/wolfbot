""" algorithms.py """
from dataclasses import dataclass
from typing import FrozenSet, List, Optional, Sequence, Set, Tuple, Union

from src import const
from src.const import Priority
from src.statements import Statement


@dataclass
class SolverState:
    """
    Each solver returns a SolverState object with the result.
    @param path: tuple of (True, False, True ...) values.
    """

    def __init__(
        self,
        possible_roles: Optional[Union[Sequence[Set[str]], Sequence[FrozenSet[str]]]] = None,
        switches: Tuple[Tuple[Priority, int, int], ...] = (),
        path_init: Tuple[bool, ...] = (),
        count_true: int = 0,
    ):
        # We share the same reference here because frozen sets are immutable.
        self.possible_roles = tuple(
            [frozenset(const.ROLE_SET)] * const.NUM_ROLES
            if possible_roles is None
            else [frozenset(role_set) for role_set in possible_roles]
        )
        self.switches = switches
        self.path = path_init
        self.count_true = count_true

    def is_valid_state(self) -> bool:
        """ Checks for invalid state, denoted as SolverState([]). """
        return bool(self.possible_roles)

    def add_to_path(self, statement_is_true: bool) -> None:
        """ Adds a new statement truth value to the state's path. """
        self.path += (statement_is_true,)
        if statement_is_true:
            self.count_true += 1

    def __repr__(self) -> str:
        """ Returns a String representation of a SolverState. """
        possible = [set(roles) for roles in self.possible_roles]
        return f"SolverState(possible_roles={possible}, switches={self.switches}, path={self.path})"


def is_consistent(statement: Statement, state: SolverState) -> SolverState:
    """
    Returns the new state if the statement is consistent with state,
    otherwise returns an empty state.
    @param state: list that contains a set of possible roles for each player.
    """
    new_switches = state.switches + statement.switches
    new_possible_roles = list(state.possible_roles)
    for proposed_ind, proposed_roles in statement.knowledge:
        intersection = proposed_roles & new_possible_roles[proposed_ind]
        if not intersection:
            return SolverState([])
        new_possible_roles[proposed_ind] = intersection
        if not check_role_counts(new_possible_roles, proposed_roles):
            return SolverState([])
    return SolverState(new_possible_roles, new_switches, state.path, state.count_true)


def switching_solver(
    statements: Tuple[Statement, ...], known_true: Tuple[int, ...] = ()
) -> List[SolverState]:
    """
    Returns maximal list of statements that can be true from a list
    of Statements. Handles switching characters.
    Returns a list of [True, False, True ...] values and
    the possible role sets for each player.
    """
    num_statements = len(statements)

    def _switch_recurse(solutions: List[SolverState], state: SolverState, ind: int = 0) -> None:
        """ ind = index of statement being considered. """
        curr_max = solutions[0].count_true
        if ind == num_statements:
            if state.count_true > curr_max:
                solutions.clear()
            if state.count_true >= curr_max:
                solutions.append(state)
            return

        if state.count_true + num_statements - ind < curr_max:
            return

        truth_state = is_consistent(statements[ind], state)
        false_state = is_consistent(statements[ind].negate(), state)

        if truth_state.is_valid_state():
            truth_state.add_to_path(True)
            _switch_recurse(solutions, truth_state, ind + 1)

        if false_state.is_valid_state() and ind not in known_true:
            false_state.add_to_path(False)
            _switch_recurse(solutions, false_state, ind + 1)

    solutions = [SolverState()]
    _switch_recurse(solutions, solutions[0])
    return solutions


def check_role_counts(
    possible_roles_list: List[FrozenSet[str]], proposed_roles: FrozenSet[str]
) -> bool:
    """
    Returns a dictionary of counts for each role in [proposed roles sets].
    Only counts players in which we are sure of their role, such as:
    {'Villager': 3, 'Robber': 0, 'Seer': 0, 'Wolf': 1}
    """
    counts_dict = dict(const.ROLE_COUNTS)
    for possible_roles in possible_roles_list:
        if len(possible_roles) == 1:
            [single_role] = possible_roles
            if single_role in proposed_roles:
                if counts_dict[single_role] == 0:
                    return False
                counts_dict[single_role] -= 1
    return True


def cached_solver(statements: Tuple[Statement, ...]) -> int:
    """ Returns maximium number of statements that can be true from a list of Statements. """
    num_statements = len(statements)

    def _cache_recurse(state: SolverState, ind: int = 0) -> int:
        if ind == num_statements or not state.is_valid_state():
            return 0
        new_state = is_consistent(statements[ind], state)
        skip_statement = _cache_recurse(state, ind + 1)
        if not new_state.is_valid_state():
            return skip_statement
        return max(1 + _cache_recurse(new_state, ind + 1), skip_statement)

    return _cache_recurse(SolverState())
