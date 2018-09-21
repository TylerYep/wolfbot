from statements import Statement
from util import find_all_player_indices
from const import logger
import const
import random
from .player import Player

class Mason(Player):
    def __init__(self, player_index, game_roles, ORIGINAL_ROLES):
        super().__init__(player_index)
        mason_indices = self.mason_init(game_roles, ORIGINAL_ROLES)
        self.role = 'Mason'
        self.new_role = ''
        self.statements = self.get_mason_statements(player_index, mason_indices)

    def mason_init(self, game_roles, ORIGINAL_ROLES):
        ''' Initializes Mason - sees all other Masons. '''
        mason_indices = find_all_player_indices(ORIGINAL_ROLES, 'Mason')
        logger.debug('[Hidden] Masons are at indices: ' + str(mason_indices))
        return mason_indices

    @staticmethod
    def get_mason_statements(player_index, mason_indices):
        if len(mason_indices) == 1:
            sentence = 'I am a Mason. The other Mason is not present.'
            knowledge = [(player_index, {'Mason'})]
            for ind in range(const.NUM_PLAYERS):
                if ind != player_index:
                    knowledge.append((ind, set(const.ROLE_SET) - {'Mason'}))
        else:
            other_mason = mason_indices[0] if mason_indices[0] != player_index else mason_indices[1]
            sentence = 'I am a Mason. The other Mason is Player ' + str(other_mason) + '.'
            knowledge = [(player_index, {'Mason'}), (other_mason, {'Mason'})]
        return [Statement(sentence, knowledge)]
