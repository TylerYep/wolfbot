import random
from statements import get_seer_statements, get_wolf_statements, get_villager_statements, Statement

class Player():
    def __init__(self):
        self.NUM_PLAYERS = 6
        self.ROLES = ('Villager', 'Villager', 'Villager', 'Wolf', 'Wolf', 'Seer')


class Wolf(Player):
    def __init__(self, player_index, wolf_indices):
        super().__init__()
        self.player = player_index
        self.wolf_indices = wolf_indices
        self.statements = get_wolf_statements(player_index, wolf_indices)

    def getNextStatement(self):
        return random.choice(tuple(self.statements))

    def __repr__(self):
        return 'Wolf'


class Seer(Player):
    def __init__(self, player_index, seer_peek_index, seer_peek_character):
        super().__init__()
        self.player = player_index
        self.statements = get_seer_statements(player_index, seer_peek_index, seer_peek_character)

    def getNextStatement(self):
        return random.choice(tuple(self.statements))

    def __repr__(self):
        return 'Seer'


class Villager(Player):
    def __init__(self, player_index):
        super().__init__()
        self.player = player_index
        self.statements = get_villager_statements(player_index)

    def getNextStatement(self):
        return random.choice(tuple(self.statements))

    def __repr__(self):
        return 'Villager'
