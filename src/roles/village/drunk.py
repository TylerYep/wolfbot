''' drunk.py '''
from typing import List

from src.statements import Statement
from src.const import logger
from src import const, util

from .player import Player

class Drunk(Player):
    ''' Drunk Player class. '''

    def __init__(self, player_index: int, game_roles: List[str], original_roles: List[str]):
        super().__init__(player_index)
        drunk_choice_index = self.drunk_init(game_roles)
        self.statements = self.get_drunk_statements(player_index, drunk_choice_index)

    def drunk_init(self, game_roles: List[str]) -> int:
        ''' Initializes Drunk - switches with a card in the center. '''
        assert const.NUM_CENTER != 0
        choice_index = util.get_center(self)
        logger.debug(f'[Hidden] Drunk switches with Center Card {choice_index - const.NUM_PLAYERS}'
                     f' and unknowingly becomes a {game_roles[choice_index]}.')
        if self.is_user: logger.info('You do not know your new role.')
        util.swap_characters(game_roles, self.player_index, choice_index)
        return choice_index

    @staticmethod
    def get_drunk_statements(player_index: int, choice_index: int) -> List[Statement]:
        ''' Gets Drunk Statement. '''
        sentence = f'I am a Drunk and I swapped with Center {choice_index - const.NUM_PLAYERS}.'
        knowledge = [(player_index, {'Drunk'})]
        switches = [(const.DRUNK_PRIORITY, choice_index, player_index)]
        return [Statement(sentence, knowledge, switches)]

    @staticmethod
    def get_all_statements(player_index: int) -> List[Statement]:
        ''' Required for all player types. Returns all possible role statements. '''
        statements = []
        for k in range(const.NUM_CENTER):
            statements += Drunk.get_drunk_statements(player_index, const.NUM_PLAYERS + k)
        return statements
