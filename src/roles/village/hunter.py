''' villager.py '''
from src.statements import Statement

from .player import Player

class Hunter(Player):
    ''' Hunter Player class. '''

    def __init__(self, player_index, game_roles, original_roles):
        super().__init__(player_index)
        self.statements = self.get_hunter_statements(player_index)

    @staticmethod
    def get_hunter_statements(player_index):
        ''' Gets Hunter Statement. '''
        return [Statement('I am a Hunter.', [(player_index, {'Hunter'})])]

    @staticmethod
    def get_all_statements(player_index):
        ''' Required for all player types. Returns all possible role statements. '''
        return Hunter.get_hunter_statements(player_index)
