''' player.py '''
from typing import Dict, List
import random

from src import const, util
from src.const import logger
from src.statements import Statement

class Player:
    ''' Player class. '''

    def __init__(self, player_index: int, new_role: str = ''):
        self.player_index = player_index
        self.role = self.__class__.__name__ # e.g. 'Wolf'
        self.new_role = new_role
        self.statements = []
        self.is_user = const.IS_USER[player_index]

    def get_statement(self, stated_roles: List[str], previous: List[Statement]) -> Statement:
        ''' Gets Player Statement. '''
        if self.is_user:
            logger.info('Please choose from the following statements: ')
            sample_statements = random.sample(self.statements, 10) if len(self.statements) > 10 \
                                else self.statements
            for i, statement in enumerate(sample_statements):
                logger.info(f'{i}. {statement.sentence}')
            choice = util.get_numeric_input(len(sample_statements))
            return sample_statements[choice]

        return random.choice(tuple(self.statements))

    def __eq__(self, other) -> bool:
        ''' Checks for equality between Players. '''
        assert isinstance(other, Player)
        self_json, other_json = self.json_repr(), other.json_repr()
        is_equal = all([self_json[key] == other_json[key] for key in self_json])
        return self.__dict__ == other.__dict__ and is_equal

    def json_repr(self) -> Dict:
        ''' Gets JSON representation of a Player object. '''
        return {'type': self.role, 'player_index': self.player_index}

    def __repr__(self) -> str:
        ''' Gets string representation of a Player object. '''
        attrs = ''
        for key, item in self.json_repr().items():
            if key != 'type':
                attrs += f'{item}, '
        return f'{self.role}({attrs[:-2]})'
