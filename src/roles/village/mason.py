''' mason.py '''
from typing import List

from src.statements import Statement
from src.const import logger
from src import const, util

from .player import Player

class Mason(Player):
    ''' Mason Player class. '''

    def __init__(self, player_index: int, game_roles: List[str], original_roles: List[str]):
        super().__init__(player_index)
        self.mason_indices = self.mason_init(original_roles)
        self.statements = self.get_mason_statements(player_index, self.mason_indices)

    def mason_init(self, original_roles: List[str]) -> List[int]:
        ''' Initializes Mason - sees all other Masons. '''
        mason_indices = util.find_all_player_indices(original_roles, 'Mason')
        logger.debug(f'[Hidden] Masons are at indices: {mason_indices}')
        if self.is_user:
            logger.info(f'Masons are players: {mason_indices} (You are player {self.player_index})')
        return mason_indices

    @staticmethod
    def get_mason_statements(player_index: int, mason_indices: List[int]) -> List[Statement]:
        ''' Gets Mason Statement. '''
        if len(mason_indices) == 1:
            sentence = 'I am a Mason. The other Mason is not present.'
            knowledge = [(player_index, {'Mason'})]
            for ind in range(const.NUM_PLAYERS):
                if ind != player_index:
                    knowledge.append((ind, set(const.ROLE_SET) - {'Mason'}))
        else:
            other_mason = mason_indices[0] if mason_indices[0] != player_index else mason_indices[1]
            sentence = f'I am a Mason. The other Mason is Player {other_mason}.'
            knowledge = [(player_index, {'Mason'}), (other_mason, {'Mason'})]
        return [Statement(sentence, knowledge)]

    @staticmethod
    def get_all_statements(player_index: int) -> List[Statement]:
        ''' Required for all player types. Returns all possible role statements. '''
        statements = Mason.get_mason_statements(player_index, [player_index])
        for i in range(const.NUM_PLAYERS):
            if player_index != i:
                mason_indices = [player_index, i]
                statements += Mason.get_mason_statements(player_index, mason_indices)
        return statements
