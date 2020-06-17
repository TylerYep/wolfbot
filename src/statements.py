""" statements.py """
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, FrozenSet, List, Tuple

from src import const
from src.const import StatementLevel, SwitchPriority

Knowledge = Tuple[int, FrozenSet[str]]
Switch = Tuple[SwitchPriority, int, int]


@dataclass
class KnowledgeBase:
    """
    Class for storing all available knowledge shared by all players.
    Used during one_night, to avoid repeated computation and to help players make decisions.
    """

    all_statements: List[Statement] = field(default_factory=list)
    stated_roles: List[str] = field(default_factory=list)
    final_claims: List[Statement] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.stated_roles = [""] * const.NUM_PLAYERS
        # Can share the same reference because they will be replaced
        zero_priority = StatementLevel.NOT_YET_SPOKEN
        self.final_claims = [Statement("", priority=zero_priority)] * const.NUM_PLAYERS

    def add(self, statement: Statement, curr_ind: int) -> None:
        """ Adds a new statement to the knowledge base. """
        self.all_statements.append(statement)
        self.stated_roles[curr_ind] = statement.speaker
        self.final_claims[curr_ind] = statement


@dataclass
class Statement:
    """
    Model for all statements in the game. Statements are intended to be immutable.
    All member variables are converted into an immutable type to be used in hash().
    Args:
        sentence: a string representation of the statement
        knowledge: a list of (player_index, set(role)) tuples
        switches: a list of (player_priority, player_index, new_index) tuples
        speaker: the role string that supposedly gave the statement.
        priority: what level of priority the statement was said.
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
            if player_index in (i, j):
                return True
        return False

    def get_references(self, player_index: int, stated_roles: List[str]) -> str:
        """ Returns True if a given player_index is referenced in a statement. """
        for i, role_set in self.knowledge[1:]:
            if i == player_index and len(role_set) == 1:
                [role] = role_set
                return role
        for _, i, j in self.switches:
            if player_index in (i, j) and player_index < len(stated_roles):
                return stated_roles[player_index]
        return ""

    def negate(self) -> Statement:
        """ Returns a negated version of the first clause in a statement. """
        not_sentence = "NOT - " + self.sentence
        if self.knowledge:
            index, player_clause = self.knowledge[0]
            negated_knowledge = ((index, const.ROLE_SET - player_clause),)
            return Statement(not_sentence, negated_knowledge, speaker=self.speaker)
        return Statement(not_sentence, speaker=self.speaker)

    def negate_all(self) -> Statement:
        """ Returns a negated version of every clause in the statement. """
        not_sentence = "NOT - " + self.sentence
        neg = [(i, const.ROLE_SET - role_set) for i, role_set in self.knowledge]
        return Statement(not_sentence, tuple(neg), speaker=self.speaker)

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
