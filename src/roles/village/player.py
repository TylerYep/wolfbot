import random

class Player():
    def __init__(self, player_index):
        self.player_index = player_index

    def get_statement(self, stated_roles=None, previous=None):
        return random.choice(tuple(self.statements))

    def json_repr(self):
        return {'type': self.role, 'player_index': self.player_index, 'statements': self.statements}

    def __repr__(self):
        return '<' + self.role + '>'
