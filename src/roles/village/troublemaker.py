''' troublemaker.py '''
from statements import Statement
from util import get_random_player, swap_characters
from const import logger
import const

from .player import Player

class Troublemaker(Player):
    ''' Troublemaker Player class. '''

    def __init__(self, player_index, game_roles, ORIGINAL_ROLES):
        super().__init__(player_index)
        trblmkr_index1, trblmkr_index2 = self.troublemaker_init(game_roles)
        self.role = 'Troublemaker'
        self.new_role = ''
        self.statements = self.get_troublemaker_statements(player_index, trblmkr_index1, trblmkr_index2)

    def troublemaker_init(self, game_roles):
        ''' Initializes Troublemaker - switches one player with another player. '''
        troublemaker_choice_index1 = get_random_player()
        troublemaker_choice_index2 = get_random_player()
        while troublemaker_choice_index1 == self.player_index:
            troublemaker_choice_index1 = get_random_player()
        while troublemaker_choice_index2 in (self.player_index, troublemaker_choice_index1):
            troublemaker_choice_index2 = get_random_player()
        swap_characters(game_roles, troublemaker_choice_index1, troublemaker_choice_index2)
        logger.debug('[Hidden] Troublemaker switches Player %d with Player %d.',
                     troublemaker_choice_index1, troublemaker_choice_index2)
        return troublemaker_choice_index1, troublemaker_choice_index2

    @staticmethod
    def get_troublemaker_statements(player_index, trblmkr_index1, trblmkr_index2):
        ''' Gets Troublemaker Statement. '''
        sentence = 'I am a Troublemaker and I swapped Player ' + str(trblmkr_index1) + \
                    ' and Player ' + str(trblmkr_index2) + '.'
        knowledge = [(player_index, {'Troublemaker'})]
        switches = [(const.TROUBLEMAKER_PRIORITY, trblmkr_index1, trblmkr_index2)]
        return [Statement(sentence, knowledge, switches)]
