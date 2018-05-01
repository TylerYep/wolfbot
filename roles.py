import random

class Player():
    def __init__(self):
        self.NUM_PLAYERS = 6
        self.ROLES = ('Villager', 'Villager', 'Villager', 'Wolf', 'Wolf', 'Seer')


class Wolf(Player):
    def __init__(self, playerIndex, wolfIndices):
        super().__init__()

        self.player = playerIndex
        self.wolfIndices = wolfIndices
        # Select who i'm gonna imitate and then select the statement
        
        self.statements = ["I am a Villager!"]
        for i in range(self.NUM_PLAYERS):
            for r in self.ROLES:
                seerReveal = "I am a Seer and I saw that Player " + str(i) + " was a " + str(r) + "."
                self.statements.append(seerReveal)

    def getNextStatement(self):
        return random.choice(self.statements)

    def __repr__(self):
        return 'Wolf'

class Villager(Player):
    def __init__(self, playerIndex):
        self.player = playerIndex
        self.statements = ["I am a Villager!"]

    def getNextStatement(self):
        return random.choice(self.statements)

    def __repr__(self):
        return 'Villager'

class Seer(Player):
    def __init__(self, playerIndex, seerPeekIndex, seerPeekCharacter):
        self.player = playerIndex
        seerReveal = "I am a Seer and I saw that Player " + str(seerPeekIndex) + " was a " + str(seerPeekCharacter) + "."
        self.statements = [seerReveal]

    def getNextStatement(self):
        return random.choice(self.statements)

    def __repr__(self):
        return 'Seer'
