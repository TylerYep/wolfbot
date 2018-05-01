import random

class Player():
    def __init__(self):
        self.NUM_PLAYERS = 6
        self.ROLES = ('Villager', 'Villager', 'Villager', 'Wolf', 'Wolf', 'Seer')

    @staticmethod
    def getSeerStatement(index, role):
        return "I am a Seer and I saw that Player " + str(index) + " was a " + str(role) + "."


class Wolf(Player):
    def __init__(self, playerIndex, wolfIndices):
        super().__init__()

        self.player = playerIndex
        self.wolfIndices = wolfIndices
        # Select who i'm gonna imitate and then select the statement

        self.statements = ["I am a Villager!"]
        for index in range(self.NUM_PLAYERS):
            for role in self.ROLES:
                self.statements.append(self.getSeerStatement(index, role))

    def getNextStatement(self):
        return random.choice(self.statements)

    def __repr__(self):
        return 'Wolf'



class Villager(Player):
    def __init__(self, playerIndex):
        super().__init__()
        self.player = playerIndex
        self.statements = ["I am a Villager!"]

    def getNextStatement(self):
        return random.choice(self.statements)

    def __repr__(self):
        return 'Villager'



class Seer(Player):
    def __init__(self, playerIndex, seerPeekIndex, seerPeekCharacter):
        super().__init__()
        self.player = playerIndex
        self.statements = [self.getSeerStatement(seerPeekIndex, seerPeekCharacter)]

    def getNextStatement(self):
        return random.choice(self.statements)

    def __repr__(self):
        return 'Seer'
