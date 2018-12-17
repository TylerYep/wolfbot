''' minion.py '''
from util import find_all_player_indices
from const import logger
import const

from ..village import Player
from .wolf import Wolf

class Minion(Player):
    ''' Minion Player class. '''

    def __init__(self, player_index, game_roles, ORIGINAL_ROLES=None):
        # Roles default to None when another player becomes a Minion and realizes it
        super().__init__(player_index)
        self.role = 'Minion'
        self.statements = []
        self.wolf_indices = self.minion_init(ORIGINAL_ROLES)
        self.center_role = None # Temporary, to use Wolf class
        self.new_role = ''

    def minion_init(self, ORIGINAL_ROLES):
        ''' Initializes Minion - gets Wolf indices. '''
        wolf_indices = []
        if ORIGINAL_ROLES is not None:
            wolf_indices = set(find_all_player_indices(ORIGINAL_ROLES, 'Wolf'))
        logger.debug('[Hidden] Wolves are at indices: %s', str(wolf_indices))
        return wolf_indices

    def get_statement(self, stated_roles, previous_statements):
        ''' Get Minion Statement. '''
        return Wolf.get_statement(self, stated_roles, previous_statements)