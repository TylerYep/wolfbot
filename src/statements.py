''' statements.py '''
from __future__ import annotations
from typing import Any, Dict, List, Set, Tuple
from src import const

class Statement:
    ''' Model for all statements in the game. '''
    def __init__(self,
                 sentence: str,
                 knowledge: List[Tuple[int, Set[str]]],
                 switches: List[Tuple[int, int, int]] = None,
                 speaker: str = None):
        '''
        sentence is a string representation of the statement
        knowledge is a list of (player_index, set(role)) tuples
        switches is a list of (player_priority, player_index, new_index) tuples
        speaker is the role string that supposedly gave the statement.
        '''
        self.sentence = sentence
        self.knowledge = knowledge
        self.switches = switches if switches is not None else []
        self.speaker = speaker
        if speaker is None and self.knowledge is not None:
            self.speaker = next(iter(knowledge[0][1]))

    def negate(self) -> Statement:
        ''' Returns a negated version of the first clause in a statement. '''
        neg = []
        if self.knowledge:
            player_clause = self.knowledge[0]
            new_set = set(const.ROLES) - player_clause[1]
            neg = [(player_clause[0], new_set)]
        return Statement('NOT - ' + self.sentence, neg, [], self.speaker)

    def negate_all(self) -> Statement:
        ''' Returns a negated version of every clause in the statement. '''
        neg = []
        for tupl in self.knowledge:
            new_set = set(const.ROLES) - tupl[1]
            neg.append((tupl[0], new_set))
        return Statement('NOT - ' + self.sentence, neg, [], self.speaker)

    def json_repr(self) -> Dict[str, Any]:
        ''' Returns json representation of the Statement. '''
        return {'type': 'Statement',
                'sentence': self.sentence,
                'knowledge': self.knowledge,
                'switches': self.switches,
                'speaker': self.speaker}

    def __repr__(self) -> str:
        return f'Statement("{self.sentence}", {self.knowledge}, {self.switches}, {self.speaker})'
