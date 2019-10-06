''' troublemaker.py '''
from typing import List, Tuple

from src.statements import Statement
from src.const import logger
from src import const, util

from .player import Player

class Troublemaker(Player):
    ''' Troublemaker Player class. '''

    def __init__(self, player_index: int, game_roles: List[str], original_roles: List[str]):
        super().__init__(player_index)
        self.choice_ind1, self.choice_ind2 = self.troublemaker_init(game_roles)
        self.statements = self.get_troublemaker_statements(player_index,
                                                           self.choice_ind1,
                                                           self.choice_ind2)

    def troublemaker_init(self, game_roles: List[str]) -> Tuple[int, int]:
        ''' Initializes Troublemaker - switches one player with another player. '''
        choice_1 = util.get_player(self.is_user, (self.player_index,))
        choice_2 = util.get_player(self.is_user, (self.player_index, choice_1))

        util.swap_characters(game_roles, choice_1, choice_2)
        logger.debug(f'[Hidden] Troublemaker switches Player {choice_1} and Player {choice_2}.')
        return choice_1, choice_2

    @staticmethod
    def get_troublemaker_statements(player_index: int,
                                    tmkr_ind1: int,
                                    tmkr_ind2: int) -> List[Statement]:
        ''' Gets Troublemaker Statement. '''
        sentence = f'I am a Troublemaker and I swapped Player {tmkr_ind1} and Player {tmkr_ind2}.'
        knowledge = [(player_index, {'Troublemaker'})]
        switches = [(const.TROUBLEMAKER_PRIORITY, tmkr_ind1, tmkr_ind2)]
        return [Statement(sentence, knowledge, switches)]

    @staticmethod
    def get_all_statements(player_index: int) -> List[Statement]:
        ''' Required for all player types. Returns all possible role statements. '''
        statements = []
        for i in range(const.NUM_PLAYERS):
            for j in range(i + 1, const.NUM_PLAYERS):
                # Troublemaker should not refer to other wolves or themselves
                # Ensure all three values are unique
                if len({i, j, player_index}) == 3:
                    statements += Troublemaker.get_troublemaker_statements(player_index, i, j)
        return statements
