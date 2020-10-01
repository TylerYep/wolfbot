""" statements.py """
from __future__ import annotations

from dataclasses import dataclass, field
from functools import cached_property
from typing import Any, Dict, FrozenSet, List, Tuple

from dataslots import dataslots

from src import const
from src.const import Role, StatementLevel, SwitchPriority

Knowledge = Tuple[int, FrozenSet[Role]]
Switch = Tuple[SwitchPriority, int, int]


@dataslots
@dataclass
class KnowledgeBase:
    """
    Class for storing all available knowledge shared by all players.
    Used during one_night, to avoid repeated computation and
    to help players make decisions.
    """

    all_statements: List[Statement] = field(default_factory=list)
    stated_roles: List[Role] = field(default_factory=list)
    final_claims: List[Statement] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.stated_roles = [Role.NONE] * const.NUM_PLAYERS
        # Can share the same reference because they will be replaced
        zero_priority = StatementLevel.NOT_YET_SPOKEN
        self.final_claims = [Statement("", priority=zero_priority)] * const.NUM_PLAYERS

    @classmethod
    def from_statement_list(
        cls, statement_list: Tuple[Statement, ...]
    ) -> KnowledgeBase:
        """ Create a new statement from a Statement list. """
        knowledge_base = cls()
        for statement in statement_list:
            speaker_index = statement.knowledge[0][0]
            knowledge_base.add(statement, speaker_index)
        return knowledge_base

    def add(self, statement: Statement, curr_ind: int) -> None:
        """ Adds a new statement to the knowledge base. """
        self.all_statements.append(statement)
        self.stated_roles[curr_ind] = statement.speaker
        self.final_claims[curr_ind] = statement


@dataslots(add_dict=True)
@dataclass
class Statement:
    """
    Model for all statements in the game. Statements are intended to be immutable.
    All member variables are converted into an immutable type to be used in hash().
    __slots__ must contain __dict__ to use @cached_property.
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
    speaker: Role = Role.NONE
    priority: StatementLevel = StatementLevel.PRIMARY

    def __post_init__(self) -> None:
        if self.speaker is Role.NONE and self.knowledge:
            [self.speaker] = self.knowledge[0][1]

    def __hash__(self) -> int:
        """
        The sentence field currently uniquely identifies the fields of a statement,
        however this could change with the introduction of statements
        (e.g. user-generated) in which different sentences carry the same knowledge.
        """
        return hash(self.sentence)

    @cached_property
    def negation(self) -> Statement:
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

    def references(self, player_index: int) -> bool:
        """ Returns True if a given player_index is referenced in a statement. """
        for i, _ in self.knowledge[1:]:
            if i == player_index:
                return True
        for _, i, j in self.switches:
            if player_index in (i, j):
                return True
        return False

    def get_references(self, player_index: int, stated_roles: List[Role]) -> Role:
        """ Returns True if a given player_index is referenced in a statement. """
        for i, role_set in self.knowledge[1:]:
            if i == player_index and len(role_set) == 1:
                [role] = role_set
                return role
        for _, i, j in self.switches:
            if player_index in (i, j) and player_index < len(stated_roles):
                return stated_roles[player_index]
        return Role.NONE

    def json_repr(self) -> Dict[str, Any]:
        """ Returns json representation of the Statement. """
        return {
            "type": "Statement",
            "sentence": self.sentence,
            "knowledge": self.knowledge,
            "switches": self.switches,
            "speaker": self.speaker,
        }
