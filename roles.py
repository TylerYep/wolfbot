import random
import const
from statements import Statement, get_seer_statements, get_wolf_statements, get_villager_statements

class Player():
    def __init__(self):
        self.a = 1

    def getNextStatement(self):
        return random.choice(tuple(self.statements))

    def __repr__(self):
        return self.role

class Wolf(Player):
    def __init__(self, player_index, wolf_indices):
        super().__init__()
        self.role = 'Wolf'
        self.player = player_index
        self.wolf_indices = wolf_indices
        self.statements = get_wolf_statements(player_index, wolf_indices)


class Seer(Player):
    def __init__(self, player_index, seer_peek_index, seer_peek_character):
        super().__init__()
        self.role = 'Seer'
        self.player = player_index
        self.statements = get_seer_statements(player_index, seer_peek_index, seer_peek_character)


class Villager(Player):
    def __init__(self, player_index):
        super().__init__()
        self.role = 'Villager'
        self.player = player_index
        self.statements = get_villager_statements(player_index)
        
