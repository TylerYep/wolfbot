""" statements.py """
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, FrozenSet, List, Optional, Sequence, Set, Tuple, Union

from src import const
from src.const import StatementLevel, SwitchPriority

Knowledge = Tuple[int, FrozenSet[str]]
Switch = Tuple[SwitchPriority, int, int]


@dataclass
class Statement:
    """
    Model for all statements in the game. Statements are intended to be immutable.
    sentence is a string representation of the statement
    knowledge is a list of (player_index, set(role)) tuples
    switches is a list of (player_priority, player_index, new_index) tuples
    speaker is the role string that supposedly gave the statement.
    priority is what level of priority the statement was said.
    All member variables are converted into an immutable type to be used in hash()
    """

    sentence: str
    knowledge: Tuple[Knowledge, ...] = ()
    switches: Tuple[Switch, ...] = ()
    speaker: str = ""
    priority: StatementLevel = StatementLevel.PRIMARY

    def __post_init__(self) -> None:
        if not self.speaker and self.knowledge:
            [self.speaker] = self.knowledge[0][1]

    def references(self, player_index: int) -> bool:
        """ Returns True if a given player_index is referenced in a statement. """
        for i, _ in self.knowledge[1:]:
            if i == player_index:
                return True
        for _, i, j in self.switches:
            if i == player_index or j == player_index:
                return True
        return False

    def get_references(self, player_index: int, stated_roles: List[str]) -> str:
        """ Returns True if a given player_index is referenced in a statement. """
        for i, role_set in self.knowledge[1:]:
            if i == player_index and len(role_set) == 1:
                [role] = role_set
                return role
        for _, i, j in self.switches:
            if (i == player_index or j == player_index) and player_index < len(stated_roles):
                return stated_roles[player_index]
        return ""

    def negate(self) -> Statement:
        """ Returns a negated version of the first clause in a statement. """
        neg = []
        if self.knowledge:
            index, player_clause = self.knowledge[0]
            neg.append((index, const.ROLE_SET - player_clause))
        return Statement("NOT - " + self.sentence, tuple(neg), (), self.speaker)

    def negate_all(self) -> Statement:
        """ Returns a negated version of every clause in the statement. """
        neg = [(i, const.ROLE_SET - role_set) for i, role_set in self.knowledge]
        return Statement("NOT - " + self.sentence, tuple(neg), (), self.speaker)

    def __hash__(self) -> int:
        return hash((self.sentence, self.knowledge, self.switches, self.speaker, self.priority))

    def json_repr(self) -> Dict[str, Any]:
        """ Returns json representation of the Statement. """
        return {
            "type": "Statement",
            "sentence": self.sentence,
            "knowledge": self.knowledge,
            "switches": self.switches,
            "speaker": self.speaker,
        }
