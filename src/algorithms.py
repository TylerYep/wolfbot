""" algorithms.py """
from __future__ import annotations

from typing import FrozenSet, List, Optional, Sequence, Set, Tuple, Union

from src import const
from src.const import Priority
from src.statements import Statement


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
    ):
        # We share the same reference here because frozen sets are immutable.
        self.possible_roles = tuple(
            [const.ROLE_SET] * const.NUM_ROLES
            if possible_roles is None
            else [frozenset(role_set) for role_set in possible_roles]
        )
        self.switches = switches
        self.path = path_init

    def is_valid_state(self) -> bool:
        """ Checks for invalid state, denoted as SolverState(). """
        return bool(self.possible_roles)

    def __eq__(self, other: object) -> bool:
        assert isinstance(other, SolverState)
        return self.__dict__ == other.__dict__

    def __repr__(self) -> str:
        """ Returns a String representation of a SolverState. """
        possible = [set(roles) for roles in self.possible_roles]
        return f"SolverState(possible_roles={possible}, switches={self.switches}, path={self.path})"

    def is_consistent(self, statement: Statement) -> SolverState:
        """
        Returns the new state if the statement is consistent with state,
        otherwise returns an empty state.
        """
        new_possible_roles = list(self.possible_roles)
        for proposed_ind, proposed_roles in statement.knowledge:
            new_possible_roles[proposed_ind] &= proposed_roles
            if not new_possible_roles[proposed_ind]:
                return SolverState([])
        if not check_role_counts(new_possible_roles):
            return SolverState([])
        new_switches = self.switches + statement.switches
        return SolverState(new_possible_roles, new_switches, self.path)


def check_role_counts(possible_roles_list: List[FrozenSet[str]]) -> bool:
    """
    Ensures that all current sets in possible_roles_list that contain only one element
    are still within the bounds of the ROLE_COUNTS dict. E.g.
    {'Villager': 3, 'Robber': 0, 'Seer': 0, 'Wolf': 1}
    """
    counts_dict = dict(const.ROLE_COUNTS)
    for possible_roles in possible_roles_list:
        if len(possible_roles) == 1:
            [single_role] = possible_roles
            if counts_dict[single_role] == 0:
                return False
            counts_dict[single_role] -= 1
    return True


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
        prev_max = solutions[0].path.count(True)
        curr_path_count = state.path.count(True)
        if ind == num_statements:
            if curr_path_count > prev_max:
                solutions.clear()
            if curr_path_count >= prev_max:
                solutions.append(state)
            return

        if curr_path_count + num_statements - ind < prev_max:
            return

        truth_state = state.is_consistent(statements[ind])
        false_state = state.is_consistent(statements[ind].negate())

        if truth_state.is_valid_state():
            truth_state.path += (True,)
            _switch_recurse(solutions, truth_state, ind + 1)

        if false_state.is_valid_state() and ind not in known_true:
            false_state.path += (False,)
            _switch_recurse(solutions, false_state, ind + 1)

    solutions = [SolverState()]
    _switch_recurse(solutions, solutions[0])
    return solutions


def cached_solver(statements: Tuple[Statement, ...]) -> int:
    """ Returns maximium number of statements that can be true from a list of Statements. """
    num_statements = len(statements)

    def _cache_recurse(state: SolverState, ind: int = 0) -> int:
        if ind == num_statements or not state.is_valid_state():
            return 0
        new_state = state.is_consistent(statements[ind])
        skip_statement = _cache_recurse(state, ind + 1)
        if not new_state.is_valid_state():
            return skip_statement
        return max(1 + _cache_recurse(new_state, ind + 1), skip_statement)

    return _cache_recurse(SolverState())
