''' player.py '''
import random

class Player():
    ''' Player class. '''

    def __init__(self, player_index, new_role=''):
        self.player_index = player_index
        self.role = 'Player'
        self.new_role = new_role
        self.statements = []

    def get_statement(self, stated_roles=None, previous=None):
        ''' Gets Player Statement. '''
        return random.choice(tuple(self.statements))

    def json_repr(self):
        ''' Gets JSON representation of a Player object. '''
        return {'type': self.role, 'player_index': self.player_index,
                'statements': self.statements, 'new_role': self.new_role}

    def __repr__(self):
        ''' Used to distiguish Player objects for logging. '''
        return '<' + self.role + '>'
