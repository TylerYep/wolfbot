''' drunk.py '''
from statements import Statement
from const import logger
import const
import util

from .player import Player

class Drunk(Player):
    ''' Drunk Player class. '''

    def __init__(self, player_index, game_roles, original_roles):
        super().__init__(player_index)
        drunk_choice_index = self.drunk_init(game_roles)
        self.role = 'Drunk'
        self.statements = self.get_drunk_statements(player_index, drunk_choice_index)

    def drunk_init(self, game_roles):
        ''' Initializes Drunk - switches with a card in the center. '''
        assert const.NUM_CENTER != 0
        drunk_choice_index = util.get_center(self)
        logger.debug('[Hidden] Drunk switches with Center Card %d and unknowingly becomes a %s.',
                     drunk_choice_index - const.NUM_PLAYERS, str(game_roles[drunk_choice_index]))
        if self.is_user: logger.info('You do not know your new role.')
        util.swap_characters(game_roles, self.player_index, drunk_choice_index)
        return drunk_choice_index

    @staticmethod
    def get_drunk_statements(player_index, drunk_choice_index):
        ''' Gets Drunk Statement. '''
        sentence = 'I am a Drunk and I swapped with Center ' \
                    + str(drunk_choice_index - const.NUM_PLAYERS) + '.'
        knowledge = [(player_index, {'Drunk'})]
        switches = [(const.DRUNK_PRIORITY, drunk_choice_index, player_index)]
        return [Statement(sentence, knowledge, switches)]

    @staticmethod
    def get_all_statements(player_index):
        ''' Required for all player types. Returns all possible role statements. '''
        statements = []
        for k in range(const.NUM_CENTER):
            statements += Drunk.get_drunk_statements(player_index, const.NUM_PLAYERS + k)
        return statements
