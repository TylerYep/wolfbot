""" solvers.py """
from __future__ import annotations

import heapq
import shutil
from dataclasses import dataclass, field
from functools import total_ordering

from dataslots import dataslots

from src import const
from src.const import Role, formatter
from src.statements import Statement, Switch


@dataslots
@total_ordering
@dataclass
class SolverState:
    """
    Each solver returns a SolverState object with the result.
    @param path: tuple of (True, False, True ...) values.
    """

    possible_roles: tuple[frozenset[Role], ...] = ()
    switches: tuple[Switch, ...] = ()
    path: tuple[bool, ...] = ()
    role_counts: dict[Role, int] = field(default_factory=dict)
    count_true: int = -1

    def __post_init__(self) -> None:
        # We share the same reference here because frozensets are immutable.
        if not self.possible_roles:
            self.possible_roles = (const.ROLE_SET,) * const.NUM_ROLES
        if self.count_true == -1:
            self.count_true = self.path.count(True)
        if not self.role_counts:
            self.role_counts = self.get_role_counts()

    def __hash__(self) -> int:
        """
        Not recommended to hash SolverStates because each possible_roles is very large,
        but SolverStates are hashable nonetheless.
        """
        return hash((self.possible_roles, self.switches, self.path))

    def __repr__(self) -> str:
        width, _ = shutil.get_terminal_size()
        return str(formatter.pformat(self, width=width, ribbon_width=width))

    def __lt__(self, other: object) -> bool:
        if isinstance(other, SolverState):
            return self.count_true < other.count_true
        raise TypeError

    def is_consistent(
        self, statement: Statement, assumption: bool = True
    ) -> SolverState | None:
        """
        Returns the new state if the statement is consistent with state,
        otherwise returns an empty state.
        @param assumption: whether we are assuming the statement is True or False

        Warning: only creates a new_role_counts dict if the role_counts dict changes.
        Otherwise the new state will share the same role_counts
        dict as the previous state.
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

        return SolverState(
            tuple(new_possible_roles),
            self.switches + statement.switches,
            self.path + (assumption,),
            self.role_counts if new_role_counts is None else new_role_counts,
            self.count_true + int(assumption),
        )

    def get_role_counts(self) -> dict[Role, int]:
        """
        Ensures that all current sets in possible_roles_list that contain only
        one element are still within the bounds of the ROLE_COUNTS dict. E.g.
        {'Villager': 3, 'Robber': 0, 'Seer': 0, 'Wolf': 1}

        Does not benefit from @cached_property, because the function
        is only called once per instance.
        """
        if not self.possible_roles:
            return {}
        counts_dict = dict(const.ROLE_COUNTS)
        for possible_roles in self.possible_roles:
            if len(possible_roles) == 1:
                [single_role] = possible_roles
                if counts_dict[single_role] <= 0:
                    raise RuntimeError("Count should never go below 0.")
                counts_dict[single_role] -= 1
        return counts_dict


def relaxed_solver(
    statements: tuple[Statement, ...], known_true: tuple[int, ...] = ()
) -> list[SolverState]:
    """
    Returns maximal list of statements that can be true from a list
    of Statements. Handles switching characters.
    Returns a list of [True, False, True ...] values and
    the possible role sets for each player.
    """
    num_statements = len(statements)
    max_avg = 10  # len(const.VILLAGE_ROLES)

    def _relaxed_recurse(
        solutions: list[SolverState], state: SolverState, ind: int = 0
    ) -> None:
        """ ind = index of statement being considered. """
        if ind == num_statements:
            # if len(solutions) == 0 or (
            #     state.count_true
            #     >= sum(x.count_true for x in solutions) / len(solutions)
            # ):
            num_sols = len(solutions)
            if num_sols < max_avg:
                heapq.heappush(solutions, state)
            elif num_sols == max_avg:
                heapq.heappushpop(solutions, state)
            return

        truth_state = state.is_consistent(statements[ind])
        false_state = state.is_consistent(statements[ind].negation, False)

        if truth_state is not None:
            _relaxed_recurse(solutions, truth_state, ind + 1)

        if false_state is not None and ind not in known_true:
            _relaxed_recurse(solutions, false_state, ind + 1)

    solutions: list[SolverState] = []
    _relaxed_recurse(solutions, SolverState())
    return solutions


def switching_solver(
    statements: tuple[Statement, ...], known_true: tuple[int, ...] = ()
) -> list[SolverState]:
    """
    Returns maximal list of statements that can be true from a list
    of Statements. Handles switching characters.
    Returns a list of [True, False, True ...] values and
    the possible role sets for each player.
    """
    num_statements = len(statements)

    def _switch_recurse(
        solutions: list[SolverState], state: SolverState, ind: int = 0
    ) -> None:
        """ ind = index of statement being considered. """
        curr_max = solutions[0].count_true if solutions else 0
        if ind == num_statements:
            if state.count_true > curr_max:
                solutions.clear()
            if state.count_true >= curr_max:
                solutions.append(state)
            return

        if state.count_true + num_statements - ind < curr_max:
            return

        truth_state = state.is_consistent(statements[ind])
        false_state = state.is_consistent(statements[ind].negation, False)

        if truth_state is not None:
            _switch_recurse(solutions, truth_state, ind + 1)

        if false_state is not None and ind not in known_true:
            _switch_recurse(solutions, false_state, ind + 1)

    solutions: list[SolverState] = []
    _switch_recurse(solutions, SolverState())
    return solutions


def cached_solver(statements: tuple[Statement, ...]) -> int:
    """ Returns max number of statements that can be true from a list of Statements. """
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
