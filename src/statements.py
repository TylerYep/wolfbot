''' statements.py '''
from __future__ import annotations
from typing import Dict, List, Set, Tuple

from src import const

class Statement:
    ''' Model for all statements in the game. Statements are intended to be immutable. '''
    def __init__(self,
                 sentence: str,
                 knowledge: List[Tuple[int, Set[str]]] = None,
                 switches: List[Tuple[int, int, int]] = None,
                 speaker: str = None):
        '''
        sentence is a string representation of the statement
        knowledge is a list of (player_index, set(role)) tuples
        switches is a list of (player_priority, player_index, new_index) tuples
        speaker is the role string that supposedly gave the statement.
        '''
        self.sentence = sentence
        self.knowledge = tuple([(i, frozenset(role_set)) for i, role_set in knowledge])
        self.switches = tuple(map(tuple, switches)) if switches is not None else ()
        self.speaker = speaker if speaker is not None or not knowledge \
                       else next(iter(knowledge[0][1]))

    def negate(self) -> Statement:
        ''' Returns a negated version of the first clause in a statement. '''
        neg = []
        if self.knowledge:
            index, player_clause = self.knowledge[0]
            neg = [(index, const.ROLE_SET - player_clause)]
        return Statement('NOT - ' + self.sentence, neg, [], self.speaker)

    def negate_all(self) -> Statement:
        ''' Returns a negated version of every clause in the statement. '''
        neg = [(i, const.ROLE_SET - role_set) for i, role_set in self.knowledge]
        return Statement('NOT - ' + self.sentence, neg, [], self.speaker)

    def __eq__(self, other) -> bool:
        assert isinstance(other, Statement)
        return self.__dict__ == other.__dict__

    def __hash__(self) -> int:
        return hash((self.sentence, self.knowledge, self.switches, self.speaker))

    def json_repr(self) -> Dict:
        ''' Returns json representation of the Statement. '''
        return {'type': 'Statement',
                'sentence': self.sentence,
                'knowledge': self.knowledge,
                'switches': self.switches,
                'speaker': self.speaker}

    def __repr__(self) -> str:
        knowledge = [(i, set(role_set)) for i, role_set in self.knowledge]
        switches = list(self.switches)
        return f"Statement(\"{self.sentence}\", {knowledge}, {switches}, '{self.speaker}')"
