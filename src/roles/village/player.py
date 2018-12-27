''' player.py '''
import random
from const import logger
import const
import util

class Player:
    ''' Player class. '''

    def __init__(self, player_index, new_role=''):
        self.player_index = player_index
        self.role = self.__class__.__name__ # e.g. 'Wolf'
        self.new_role = new_role
        self.statements = []
        self.is_user = const.IS_USER[player_index]

    def get_statement(self, stated_roles, previous):
        ''' Gets Player Statement. '''
        if self.is_user:
            logger.info('Please choose from the following statements: ')
            for i, statement in enumerate(self.statements):
                logger.info(str(i) + '. ' + statement.sentence)
            choice = util.get_numeric_input(len(self.statements))
            return self.statements[choice]

        return random.choice(tuple(self.statements))

    def json_repr(self):
        ''' Gets JSON representation of a Player object. '''
        return {'type': self.role, 'player_index': self.player_index,
                'statements': self.statements, 'new_role': self.new_role}

    def __repr__(self):
        ''' Used to distiguish Player objects for logging. '''
        return '<' + self.role + '>'
