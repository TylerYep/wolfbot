''' troublemaker.py '''
from typing import Dict, List

from src import const, util
from src.const import Priority, logger
from src.statements import Statement

from ..player import Player


class Troublemaker(Player):
    ''' Troublemaker Player class. '''

    def __init__(self, player_index: int, choice_ind1: int, choice_ind2: int):
        super().__init__(player_index)
        self.choice_ind1, self.choice_ind2 = choice_ind1, choice_ind2
        self.statements = self.get_troublemaker_statements(player_index, choice_ind1, choice_ind2)

    @classmethod
    def awake_init(cls, player_index: int, game_roles: List[str], original_roles: List[str]):
        ''' Initializes Troublemaker - switches one player with another player. '''
        del original_roles
        is_user = const.IS_USER[player_index]
        choice_1 = util.get_player(is_user, (player_index,))
        choice_2 = util.get_player(is_user, (player_index, choice_1))

        util.swap_characters(game_roles, choice_1, choice_2)
        logger.debug(f'[Hidden] Troublemaker switches Player {choice_1} and Player {choice_2}.')
        return cls(player_index, choice_1, choice_2)

    @staticmethod
    def get_troublemaker_statements(player_index: int,
                                    tmkr_ind1: int,
                                    tmkr_ind2: int) -> List[Statement]:
        ''' Gets Troublemaker Statement. '''
        sentence = f'I am a Troublemaker and I swapped Player {tmkr_ind1} and Player {tmkr_ind2}.'
        knowledge = [(player_index, {'Troublemaker'})]
        switches = [(Priority.TROUBLEMAKER, tmkr_ind1, tmkr_ind2)]
        return [Statement(sentence, knowledge, switches)]

    @staticmethod
    def get_all_statements(player_index: int) -> List[Statement]:
        ''' Required for all player types. Returns all possible role statements. '''
        statements: List[Statement] = []
        for i in range(const.NUM_PLAYERS):
            for j in range(i + 1, const.NUM_PLAYERS):
                # Troublemaker should not refer to other wolves or themselves
                # Ensure all three values are unique
                if len({i, j, player_index}) == 3:
                    statements += Troublemaker.get_troublemaker_statements(player_index, i, j)
        return statements

    def json_repr(self) -> Dict:
        ''' Gets JSON representation of a Troublemaker player. '''
        return {'type': self.role,
                'player_index': self.player_index,
                'choice_ind1': self.choice_ind1,
                'choice_ind2': self.choice_ind2}
