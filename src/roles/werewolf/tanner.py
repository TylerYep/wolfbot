''' tanner.py '''
from ..village import Player

class Tanner(Player):
    ''' Tanner Player class. '''

    def __init__(self, player_index, game_roles, ORIGINAL_ROLES=None):
        # Roles default to None when another player becomes a Tanner and realizes it
        super().__init__(player_index)
        self.role = 'Tanner'
        self.statements = []
        self.new_role = ''

    def get_statement(self, stated_roles, previous_statements):
        ''' Get Tanner Statement. '''
        return None
