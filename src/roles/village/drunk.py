''' drunk.py '''
from typing import Dict, List

from src.statements import Statement
from src.const import logger, Priority
from src import const, util

from ..player import Player


class Drunk(Player):
    ''' Drunk Player class. '''

    def __init__(self, player_index: int, choice_ind: int):
        super().__init__(player_index)
        self.choice_ind = choice_ind
        self.statements = self.get_drunk_statements(player_index, choice_ind)

    @classmethod
    def awake_init(cls, player_index: int, game_roles: List[str], original_roles: List[str]):
        ''' Initializes Drunk - switches with a card in the center. '''
        del original_roles
        assert const.NUM_CENTER != 0
        is_user = const.IS_USER[player_index]
        choice_ind = util.get_center(is_user)
        logger.debug(f'[Hidden] Drunk switches with Center Card {choice_ind - const.NUM_PLAYERS}'
                     f' and unknowingly becomes a {game_roles[choice_ind]}.')
        if is_user:
            logger.info('You do not know your new role.')
        util.swap_characters(game_roles, player_index, choice_ind)
        return cls(player_index, choice_ind)

    @staticmethod
    def get_drunk_statements(player_index: int, choice_ind: int) -> List[Statement]:
        ''' Gets Drunk Statement. '''
        sentence = f'I am a Drunk and I swapped with Center {choice_ind - const.NUM_PLAYERS}.'
        knowledge = [(player_index, {'Drunk'})]
        switches = [(Priority.DRUNK, player_index, choice_ind)]
        return [Statement(sentence, knowledge, switches)]

    @staticmethod
    def get_all_statements(player_index: int) -> List[Statement]:
        ''' Required for all player types. Returns all possible role statements. '''
        statements: List[Statement] = []
        for k in range(const.NUM_CENTER):
            statements += Drunk.get_drunk_statements(player_index, const.NUM_PLAYERS + k)
        return statements

    def json_repr(self) -> Dict:
        ''' Gets JSON representation of a Drunk player. '''
        return {'type': self.role, 'player_index': self.player_index, 'choice_ind': self.choice_ind}
