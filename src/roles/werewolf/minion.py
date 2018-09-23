from ..village import Player, Villager, Mason, Seer, Robber, Troublemaker, Drunk, Insomniac
import const

class Minion(Player):
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
        logger.debug('[Hidden] Wolves are at indices: ' + str(wolf_indices))
        return wolf_indices
