''' villager.py '''
from typing import List

from src.statements import Statement

from .player import Player

class Villager(Player):
    ''' Villager Player class. '''

    def __init__(self, player_index: int, game_roles: List[str], original_roles: List[str]):
        super().__init__(player_index)
        self.statements = self.get_villager_statements(player_index)

    @staticmethod
    def get_villager_statements(player_index: int) -> List[Statement]:
        ''' Gets Villager Statements. '''
        return [Statement('I am a Villager.', [(player_index, {'Villager'})])]

    @staticmethod
    def get_all_statements(player_index: int) -> List[Statement]:
        ''' Required for all player types. Returns all possible role statements. '''
        return Villager.get_villager_statements(player_index)
