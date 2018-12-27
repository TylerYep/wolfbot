''' mason.py '''
from statements import Statement
from util import find_all_player_indices
from const import logger
import const

from .player import Player

class Mason(Player):
    ''' Mason Player class. '''

    def __init__(self, player_index, game_roles, original_roles):
        super().__init__(player_index)
        self.mason_indices = self.mason_init(original_roles)
        self.role = 'Mason'
        self.statements = self.get_mason_statements(player_index, self.mason_indices)

    def mason_init(self, original_roles):
        ''' Initializes Mason - sees all other Masons. '''
        mason_indices = find_all_player_indices(original_roles, 'Mason')
        logger.debug('[Hidden] Masons are at indices: %s', str(mason_indices))
        if self.is_user: logger.info('Masons are players: %s (You are player %s)',
                                     str(mason_indices), self.player_index)
        return mason_indices

    @staticmethod
    def get_mason_statements(player_index, mason_indices):
        ''' Gets Mason Statement. '''
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

    @staticmethod
    def get_all_statements(player_index):
        ''' Required for all player types. Returns all possible role statements. '''
        statements = Mason.get_mason_statements(player_index, [player_index])
        for i in range(const.NUM_PLAYERS):
            if player_index != i:
                mason_indices = [player_index, i]
                statements += Mason.get_mason_statements(player_index, mason_indices)
        return statements
