''' drunk.py '''
from statements import Statement
from util import get_random_center, swap_characters
from const import logger
import const

from .player import Player

class Drunk(Player):
    ''' Drunk Player class. '''
    def __init__(self, player_index, game_roles, ORIGINAL_ROLES):
        super().__init__(player_index)
        drunk_choice_index = self.drunk_init(game_roles)
        self.role = 'Drunk'
        self.new_role = ''
        self.statements = self.get_drunk_statements(player_index, drunk_choice_index)

    def drunk_init(self, game_roles):
        ''' Initializes Drunk - switches with a card in the center. '''
        assert const.NUM_CENTER != 0
        drunk_choice_index = get_random_center()
        logger.debug('[Hidden] Drunk switches with Center Card %d and unknowingly becomes a %s.',
                     drunk_choice_index - const.NUM_PLAYERS, str(game_roles[drunk_choice_index]))
        swap_characters(game_roles, self.player_index, drunk_choice_index)
        return drunk_choice_index

    @staticmethod
    def get_drunk_statements(player_index, drunk_choice_index):
        ''' Gets Drunk Statement. '''
        sentence = 'I am a Drunk and I swapped with Center ' + \
                    str(drunk_choice_index - const.NUM_PLAYERS) + '.'
        knowledge = [(player_index, {'Drunk'})]
        switches = [(const.DRUNK_PRIORITY, drunk_choice_index, player_index)]
        return [Statement(sentence, knowledge, switches)]
