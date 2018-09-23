from ..village import Player, Villager, Mason, Seer, Robber, Troublemaker, Drunk, Insomniac
from .wolf_variants import get_easy_wolf_statements, get_wolf_statements_random, get_statement_expectimax, get_statement_rl
from util import find_all_player_indices, get_random_center
from const import logger
import const

class Wolf(Player):
    def __init__(self, player_index, game_roles=None, ORIGINAL_ROLES=None):
         # Roles default to None when another player becomes a Wolf and realizes it
        super().__init__(player_index)
        self.role = 'Wolf'
        self.statements = []
        self.wolf_indices, self.wolf_center_index, self.wolf_center_role = self.wolf_init(game_roles, ORIGINAL_ROLES)
        self.new_role = ''

    def wolf_init(self, game_roles, ORIGINAL_ROLES):
        ''' Initializes Wolf - gets Wolf indices and a random center card, if applicable. '''
        wolf_indices = []
        wolf_center_index, wolf_center_role = None, None
        if ORIGINAL_ROLES is not None:
            wolf_indices = set(find_all_player_indices(ORIGINAL_ROLES, 'Wolf'))
            if len(wolf_indices) == 1 and const.NUM_CENTER > 0:
                wolf_center_index = get_random_center()
                wolf_center_role = game_roles[wolf_center_index]
            logger.debug('[Hidden] Wolves are at indices: ' + str(wolf_indices))
        return wolf_indices, wolf_center_index, wolf_center_role

    def get_wolf_statements(self, stated_roles, previous_statements):
        # role = self.center_role
        # if role != None and role != 'Wolf' and role != 'Mason':
        #     return self.get_easy_wolf_statements(stated_roles)
        statements = []
        if 'Villager' in const.ROLE_SET:
            statements += Villager.get_villager_statements(self.player_index)
        if 'Insomniac' in const.ROLE_SET: # and 'Insomniac' not in stated_roles:
            statements += Insomniac.get_insomniac_statements(self.player_index, 'Insomniac')
        if 'Mason' in const.ROLE_SET:
            # Only say you are a Mason if you are the last player and there are no Masons.
            if self.player_index == const.NUM_PLAYERS - 1:
                mason_indices = [self.player_index]
                for i in range(len(stated_roles)):
                    if stated_roles[i] == 'Mason':
                        mason_indices.append(i)
                if len(mason_indices) == 1:
                    statements += Mason.get_mason_statements(self.player_index, mason_indices)
        if 'Drunk' in const.ROLE_SET: # and 'Drunk' not in stated_roles:
            for k in range(const.NUM_CENTER):
                statements += Drunk.get_drunk_statements(self.player_index, k + const.NUM_PLAYERS)
        if 'Troublemaker' in const.ROLE_SET:  # and 'Troublemaker' not in stated_roles:
            for i in range(len(stated_roles)):
                for j in range(i+1, len(stated_roles)):
                    if j not in self.wolf_indices:
                        statements += Troublemaker.get_troublemaker_statements(self.player_index, i, j)
        if 'Robber' in const.ROLE_SET:  # and 'Robber' not in stated_roles:
            for i in range(len(stated_roles)):
                statements += Robber.get_robber_statements(self.player_index, i, stated_roles[i])
        if 'Seer' in const.ROLE_SET:
            for i in range(len(stated_roles)):
                if i not in self.wolf_indices and stated_roles[i] != 'Seer':      # 'Hey, I'm a Seer and I saw another Seer...'
                    statements += Seer.get_seer_statements(self.player_index, i, stated_roles[i])
        return statements

    def get_statement(self, stated_roles, previous_statements):
        if const.USE_WOLF_RL:
            self.statements = self.get_wolf_statements(stated_roles, previous_statements)
            return get_statement_rl(self.wolf_indices, previous_statements)
        elif const.USE_EXPECTIMAX_WOLF:
            self.statements = self.get_wolf_statements(stated_roles, previous_statements)
            return get_statement_expectimax(self.player_index, self.wolf_indices, self.statements, stated_roles, previous_statements)
        else:
            self.statements = get_wolf_statements_random(self.player_index, self.wolf_indices)
            return super().get_statement()
