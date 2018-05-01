import random

NUM_PLAYERS = 6
ROLES = ('Villager', 'Villager', 'Villager', 'Wolf', 'Wolf', 'Seer')

class Wolf():
    def __init__(self, playerIndex, wolfIndices):
        self.player = playerIndex
        self.wolfIndices = wolfIndices
        # Select who i'm gonna imitate and then select the statement
        self.statements = ["I am a Villager!", "I am a Seer and ..."]

    def getNextStatement(self):
        return random.choice(self.statements)

    def __repr__(self):
        return 'Wolf'

class Villager():
    def __init__(self, playerIndex):
        self.player = playerIndex
        self.statements = ["I am a Villager!"]

    def getNextStatement(self):
        return random.choice(self.statements)

    def __repr__(self):
        return 'Villager'

class Seer():
    def __init__(self, playerIndex, seerPeekIndex, seerPeekCharacter):
        self.player = playerIndex
        self.statements = ["I am a Seer and I saw..."]

    def getNextStatement(self):
        return random.choice(self.statements)

    def __repr__(self):
        return 'Seer'
