""" algorithms.py """
from __future__ import annotations

from typing import Dict, FrozenSet, List, Optional, Tuple

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
        possible_roles: Optional[Tuple[FrozenSet[str], ...]] = None,
        switches: Tuple[Tuple[Priority, int, int], ...] = (),
        path_init: Tuple[bool, ...] = (),
        role_counts: Optional[Dict[str, int]] = None,
        count_true: Optional[int] = None,
    ):
        # We share the same reference here because frozen sets are immutable.
        self.possible_roles = (
            [const.ROLE_SET] * const.NUM_ROLES if possible_roles is None else possible_roles
        )
        self.switches = switches
        self.path = path_init
        self.count_true = count_true if count_true else self.path.count(True)
        self.role_counts = role_counts if role_counts else self.get_role_counts()

    def add_to_path(self, statement_is_true: bool) -> None:
        """ Adds a new statement truth value to the state's path. """
        self.path += (statement_is_true,)
        if statement_is_true:
            self.count_true += 1

    def __eq__(self, other: object) -> bool:
        assert isinstance(other, SolverState)
        return self.__dict__ == other.__dict__

    def __repr__(self) -> str:
        """ Returns a string representation of a SolverState. """
        return (
            f"SolverState(possible_roles={self.possible_roles}, switches={self.switches}, "
            f"path={self.path}, count_true={self.count_true}, role_counts={self.role_counts})"
        )

    def is_consistent(self, statement: Statement, assumption: bool = True) -> Optional[SolverState]:
        """
        Returns the new state if the statement is consistent with state,
        otherwise returns an empty state.
        @param assumption: whether we are assuming the statement is True or False

        Warning: only creates a new_role_counts dict if the role_counts dict changes.
        Otherwise the new state will share the same role_counts dict as the previous state.
        """
        new_possible_roles = list(self.possible_roles)
        new_role_counts = None
        for proposed_ind, proposed_roles in statement.knowledge:
            old_length = len(new_possible_roles[proposed_ind])
            new_possible_roles[proposed_ind] &= proposed_roles
            possible_roles = new_possible_roles[proposed_ind]
            if not possible_roles:
                return None

            new_length = len(possible_roles)
            if new_length == 1 and new_length != old_length:
                [single_role] = possible_roles
                if new_role_counts is None:
                    new_role_counts = dict(self.role_counts)
                if new_role_counts[single_role] == 0:
                    return None
                new_role_counts[single_role] -= 1

        new_switches = self.switches + statement.switches
        return SolverState(
            tuple(new_possible_roles),
            new_switches,
            self.path + (assumption,),
            new_role_counts if new_role_counts else self.role_counts,
            self.count_true + 1 if assumption else self.count_true,
        )

    def get_role_counts(self) -> Dict[str, int]:
        """
        Ensures that all current sets in possible_roles_list that contain only one element
        are still within the bounds of the ROLE_COUNTS dict. E.g.
        {'Villager': 3, 'Robber': 0, 'Seer': 0, 'Wolf': 1}
        """
        if not self.possible_roles:
            return {}
        counts_dict = dict(const.ROLE_COUNTS)
        for possible_roles in self.possible_roles:
            if len(possible_roles) == 1:
                [single_role] = possible_roles
                assert counts_dict[single_role] > 0
                counts_dict[single_role] -= 1
        return counts_dict


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

        truth_state = state.is_consistent(statements[ind])
        false_state = state.is_consistent(statements[ind].negate(), False)

        if truth_state is not None:
            _switch_recurse(solutions, truth_state, ind + 1)

        if false_state is not None and ind not in known_true:
            _switch_recurse(solutions, false_state, ind + 1)

    solutions = [SolverState()]
    _switch_recurse(solutions, solutions[0])
    return solutions


def cached_solver(statements: Tuple[Statement, ...]) -> int:
    """ Returns maximium number of statements that can be true from a list of Statements. """
    num_statements = len(statements)

    def _cache_recurse(state: SolverState, ind: int = 0) -> int:
        if ind == num_statements or state is None:
            return 0
        new_state = state.is_consistent(statements[ind])
        skip_statement = _cache_recurse(state, ind + 1)
        if new_state is None:
            return skip_statement
        return max(1 + _cache_recurse(new_state, ind + 1), skip_statement)

    return _cache_recurse(SolverState())
