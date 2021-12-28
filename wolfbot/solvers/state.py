from __future__ import annotations

import shutil
from dataclasses import dataclass, field
from functools import total_ordering

from wolfbot import const
from wolfbot.enums import Role
from wolfbot.log import formatter
from wolfbot.statements import Statement, Switch


@total_ordering
@dataclass(slots=True)
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
        return NotImplemented

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
            new_role_counts or self.role_counts,
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
