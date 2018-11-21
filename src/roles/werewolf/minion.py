''' minion.py '''
from util import find_all_player_indices
from const import logger
from ..village import Player

class Minion(Player):
    ''' Minion Player class. '''

    def __init__(self, player_index, game_roles, ORIGINAL_ROLES=None):
        # Roles default to None when another player becomes a Minion and realizes it
        super().__init__(player_index)
        self.role = 'Minion'
        self.statements = []
        self.wolf_indices = self.minion_init(ORIGINAL_ROLES)
        self.new_role = ''

    def minion_init(self, ORIGINAL_ROLES):
        ''' Initializes Minion - gets Wolf indices. '''
        wolf_indices = []
        if ORIGINAL_ROLES is not None:
            wolf_indices = set(find_all_player_indices(ORIGINAL_ROLES, 'Wolf'))
        logger.debug('[Hidden] Wolves are at indices: %s', str(wolf_indices))
        return wolf_indices

    def get_statement(self, stated_roles, previous_statements):
        ''' Get Wolf Statement. '''
        if const.USE_REG_WOLF:
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