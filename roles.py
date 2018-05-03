import random
import const
from statements import *

class Player():
    def __init__(self, player_index):
        self.player = player_index

    def getNextStatement(self):
        return random.choice(tuple(self.statements))

    def __repr__(self):
        return self.role


class Wolf(Player):
    def __init__(self, player_index, wolf_indices):
        super().__init__(player_index)
        self.role = 'Wolf'
        # self.wolf_indices = wolf_indices
        self.statements = get_wolf_statements(player_index, wolf_indices)


class Seer(Player):
    def __init__(self, player_index, seer_peek_index, seer_peek_character):
        super().__init__(player_index)
        self.role = 'Seer'
        self.statements = get_seer_statements(player_index, seer_peek_index, seer_peek_character)


class Villager(Player):
    def __init__(self, player_index):
        super().__init__(player_index)
        self.role = 'Villager'
        self.statements = get_villager_statements(player_index)


class Mason(Player):
    def __init__(self, player_index, mason_indices):
        super().__init__(player_index)
        self.role = 'Mason'
        # self.mason_indices = mason_indices
        self.statements = get_mason_statements(player_index, mason_indices)


class Troublemaker(Player):
    def __init__(self, player_index):
        super().__init__(player_index)
        self.role = 'Troublemaker'
        self.statements = get_troublemaker_statements(player_index)


class Drunk(Player):
    def __init__(self, player_index):
        super().__init__(player_index)
        self.role = 'Drunk'
        self.statements = get_drunk_statements(player_index)


class Robber(Player):
    def __init__(self, player_index, robber_choice_index, robber_choice_character):
        super().__init__(player_index)
        self.role = 'Robber'
        self.statements = get_robber_statements(player_index, robber_choice_index, robber_choice_character)
