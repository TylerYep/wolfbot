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
        return self.player_index == other.player_index \
           and self.role == other.role \
           and self.new_role == other.new_role \
           and self.statements == other.statements \
           and self.is_user == other.is_user

    def json_repr(self) -> Dict:
        ''' Gets JSON representation of a Player object. '''
        return {'type': self.role, 'player_index': self.player_index,
                'statements': self.statements, 'new_role': self.new_role}

    def __repr__(self) -> str:
        ''' Used to distiguish Player objects for logging. '''
        return '<' + self.role + '>'
