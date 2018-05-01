import random
from statements import get_seer_statements, get_wolf_statements, get_villager_statements, Statement


class Player():
    def __init__(self):
        self.NUM_PLAYERS = 6
        self.ROLES = ('Villager', 'Villager', 'Villager', 'Wolf', 'Wolf', 'Seer')

    def getSeerStatement(index, role):
        return "I am a Seer and I saw that Player " + str(index) + " was a " + str(role) + "."


class Wolf(Player):
    def __init__(self, playerIndex, wolfIndices):
        super().__init__()

        self.player = playerIndex
        self.wolfIndices = wolfIndices
        # Select who i'm gonna imitate and then select the statement

        self.statements = get_villager_statements(playerIndex)

    def getNextStatement(self):
        return random.choice(self.statements)

    def __repr__(self):
        return 'Wolf'



class Villager(Player):
    def __init__(self, playerIndex):
        super().__init__()
        self.player = playerIndex
        self.statements = get_villager_statements(playerIndex)

    def getNextStatement(self):
        return random.choice(self.statements)

    def __repr__(self):
        return 'Villager'



class Seer(Player):
    def __init__(self, playerIndex, seerPeekIndex, seerPeekCharacter):
        super().__init__()
        self.player = playerIndex
        #TODO Fix this call
        self.statements = get_seer_statements(playerIndex)

    def getNextStatement(self):
        return random.choice(self.statements)

    def __repr__(self):
        return 'Seer'
