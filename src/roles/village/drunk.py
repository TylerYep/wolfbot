from .player import Player
from statements import Statement
from util import get_random_center, swap_characters
from const import logger
import const
import random

class Drunk(Player):
    def __init__(self, player_index, game_roles, ORIGINAL_ROLES):
        super().__init__(player_index)
        drunk_choice_index = self.drunk_init(game_roles)
        self.role = 'Drunk'
        self.new_role = ''
        self.statements = self.get_drunk_statements(player_index, drunk_choice_index)

    def drunk_init(self, game_roles):
        ''' Initializes Drunk - switches with a card in the center. '''
        assert(const.NUM_CENTER != 0)
        drunk_choice_index = get_random_center()
        logger.debug('[Hidden] Drunk switches with Center Card ' + str(drunk_choice_index - const.NUM_PLAYERS) +
                    ' and unknowingly becomes a ' + str(game_roles[drunk_choice_index]))
        swap_characters(game_roles, self.player_index, drunk_choice_index)
        return drunk_choice_index

    @staticmethod
    def get_drunk_statements(player_index, drunk_choice_index):
        sentence = 'I am a Drunk and I swapped with Center ' + \
                    str(drunk_choice_index - const.NUM_PLAYERS) + '.'
        knowledge = [(player_index, {'Drunk'})]
        switches = [(const.DRUNK_PRIORITY, drunk_choice_index, player_index)]
        return [Statement(sentence, knowledge, switches)]
