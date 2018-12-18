''' troublemaker.py '''
from statements import Statement
from util import get_random_player, swap_characters
from const import logger
import const

from .player import Player

class Troublemaker(Player):
    ''' Troublemaker Player class. '''

    def __init__(self, player_index, game_roles, original_roles):
        super().__init__(player_index)
        tmkr_index1, tmkr_index2 = self.troublemaker_init(player_index, game_roles)
        self.role = 'Troublemaker'
        self.statements = self.get_troublemaker_statements(player_index, tmkr_index1, tmkr_index2)

    @staticmethod
    def troublemaker_init(player_index, game_roles):
        ''' Initializes Troublemaker - switches one player with another player. '''
        troublemaker_choice_index1 = get_random_player()
        troublemaker_choice_index2 = get_random_player()
        while troublemaker_choice_index1 == player_index:
            troublemaker_choice_index1 = get_random_player()
        while troublemaker_choice_index2 in (player_index, troublemaker_choice_index1):
            troublemaker_choice_index2 = get_random_player()
        swap_characters(game_roles, troublemaker_choice_index1, troublemaker_choice_index2)
        logger.debug('[Hidden] Troublemaker switches Player %d with Player %d.',
                     troublemaker_choice_index1, troublemaker_choice_index2)
        return troublemaker_choice_index1, troublemaker_choice_index2

    @staticmethod
    def get_troublemaker_statements(player_index, tmkr_index1, tmkr_index2):
        ''' Gets Troublemaker Statement. '''
        sentence = 'I am a Troublemaker and I swapped Player ' + str(tmkr_index1) \
                    + ' and Player ' + str(tmkr_index2) + '.'
        knowledge = [(player_index, {'Troublemaker'})]
        switches = [(const.TROUBLEMAKER_PRIORITY, tmkr_index1, tmkr_index2)]
        return [Statement(sentence, knowledge, switches)]

    @staticmethod
    def get_all_statements(player_index):
        ''' Required for all player types. Returns all possible role statements. '''
        statements = []
        for i in range(const.NUM_PLAYERS):
            for j in range(i+1, const.NUM_PLAYERS):
                # Troublemaker should not refer to other wolves or themselves
                # Ensures all three values are unique
                if len({i, j, player_index}) == 3:
                    statements += Troublemaker.get_troublemaker_statements(player_index, i, j)
        return statements
