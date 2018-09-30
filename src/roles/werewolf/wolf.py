''' wolf.py '''
from util import find_all_player_indices, get_random_center
from const import logger
import const

from ..village import Player
from .wolf_variants import get_wolf_statements_random, get_statement_expectimax, \
                           get_statement_rl, get_wolf_statements, get_center_wolf_statements

class Wolf(Player):
    ''' Wolf Player class. '''

    def __init__(self, player_index, game_roles=None, ORIGINAL_ROLES=None):
        ''' Constructor: ORIGINAL_ROLES defaults to None when a player becomes a Wolf and realizes it. '''
        super().__init__(player_index)
        self.role = 'Wolf'
        self.new_role = ''
        self.wolf_indices, self.center_index, self.center_role = self.wolf_init(game_roles, ORIGINAL_ROLES)
        self.statements = []

    def wolf_init(self, game_roles, ORIGINAL_ROLES):
        ''' Initializes Wolf - gets Wolf indices and a random center card, if applicable. '''
        wolf_indices = []
        wolf_center_index, wolf_center_role = None, None
        # Only get center roles and wolf indices if not a Robber/Insomniac Wolf
        if ORIGINAL_ROLES is not None:
            wolf_indices = set(find_all_player_indices(ORIGINAL_ROLES, 'Wolf'))
            if len(wolf_indices) == 1 and const.NUM_CENTER > 0:
                wolf_center_index = get_random_center()
                wolf_center_role = game_roles[wolf_center_index]
            logger.debug('[Hidden] Wolves are at indices: %s', str(wolf_indices))
        return wolf_indices, wolf_center_index, wolf_center_role

    def get_statement(self, stated_roles, previous_statements):
        ''' Get Wolf Statement. '''
        if const.USE_REG_WOLF:
            if self.center_role not in (None, 'Wolf', 'Mason'):
                self.statements = get_center_wolf_statements(self.player_index, self.center_role,
                                                             self.center_index, self.wolf_indices, stated_roles)
            if not self.statements:
                self.statements = get_wolf_statements(self.player_index, self.wolf_indices,
                                                      stated_roles, previous_statements)
        else:
            self.statements = get_wolf_statements_random(self.player_index, self.wolf_indices)

        if const.USE_RL_WOLF:
            return get_statement_rl(self.player_index, self.wolf_indices, stated_roles,
                                    previous_statements, super().get_statement())
        if const.USE_EXPECTIMAX_WOLF:
            return get_statement_expectimax(self.player_index, self.wolf_indices,
                                            self.statements, previous_statements)
        return super().get_statement()
