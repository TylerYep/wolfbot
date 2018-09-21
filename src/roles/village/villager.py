from statements import Statement
from .player import Player

class Villager(Player):
    def __init__(self, player_index):
        super().__init__(player_index)
        self.role = 'Villager'
        self.new_role = ''
        self.statements = self.get_villager_statements(player_index)

    @staticmethod
    def get_villager_statements(player_index):
        return [Statement('I am a Villager.' , [(player_index, {'Villager'})])]
