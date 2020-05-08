""" statements.py """
from __future__ import annotations

from typing import Any, Dict, FrozenSet, List, Optional, Set, Tuple, Union

from src import const
from src.const import Priority


class Statement:
    """ Model for all statements in the game. Statements are intended to be immutable. """

    def __init__(
        self,
        sentence: str,
        knowledge: List[Tuple[int, Set[str]]] = [],
        switches: List[Tuple[Priority, int, int]] = [],
        speaker: str = "",
        priority: int = const.PRIMARY,
    ):
        """
        sentence is a string representation of the statement
        knowledge is a list of (player_index, set(role)) tuples
        switches is a list of (player_priority, player_index, new_index) tuples
        speaker is the role string that supposedly gave the statement.
        priority is what level of priority the statement was said.
        All member variables are converted into an immutable type to be used in hash()
        """
        self.sentence = sentence
        self.knowledge = tuple([(i, frozenset(role_set)) for i, role_set in knowledge])
        self.switches = tuple(switches)
        self.speaker = speaker if speaker or not knowledge else next(iter(knowledge[0][1]))
        self.priority = priority

    def references(self, player_index: int) -> bool:
        """ Returns True if a given player_index is referenced in a statement. """
        for i, _ in self.knowledge[1:]:
            if i == player_index:
                return True
        for _, i, j in self.switches:
            if i == player_index or j == player_index:
                return True
        return False

    def get_references(self, player_index: int) -> Optional[Union[FrozenSet[str], int]]:
        """ Returns True if a given player_index is referenced in a statement. """
        for i, role_set in self.knowledge[1:]:
            if i == player_index:
                return role_set
        for _, i, j in self.switches:
            if i == player_index or j == player_index:
                return player_index
        return None

    def negate(self) -> Statement:
        """ Returns a negated version of the first clause in a statement. """
        neg = []
        if self.knowledge:
            index, player_clause = self.knowledge[0]
            neg.append((index, const.ROLE_SET - player_clause))
        return Statement("NOT - " + self.sentence, neg, [], self.speaker)

    def negate_all(self) -> Statement:
        """ Returns a negated version of every clause in the statement. """
        neg = [(i, const.ROLE_SET - role_set) for i, role_set in self.knowledge]
        return Statement("NOT - " + self.sentence, neg, [], self.speaker)

    def __eq__(self, other: object) -> bool:
        assert isinstance(other, Statement)
        return self.__dict__ == other.__dict__

    def __hash__(self) -> int:
        return hash((self.sentence, self.knowledge, self.switches, self.speaker))

    def json_repr(self) -> Dict[str, Any]:
        """ Returns json representation of the Statement. """
        return {
            "type": "Statement",
            "sentence": self.sentence,
            "knowledge": self.knowledge,
            "switches": self.switches,
            "speaker": self.speaker,
        }

    def __repr__(self) -> str:
        knowledge = [(i, set(role_set)) for i, role_set in self.knowledge]
        return (
            f'Statement(sentence="{self.sentence}", knowledge={knowledge}, '
            f"switches={list(self.switches)}, speaker='{self.speaker}')"
        )
