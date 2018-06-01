import const
from collections import Counter
from const import logger

class GameResult:
    def __init__(self, actual, guessed, statements, wi):
        self.actual = actual
        self.guessed = guessed
        self.statements = statements
        self.wolf_inds = wi
        

class Statistics:
    def __init__(self):
        self.metrics = [self.correctness_strict, self.correctness_lenient_center, self.verify_predictions]
        self.NUM_METRICS = len(self.metrics)
        self.correct = [0.0 for _ in range(self.NUM_METRICS)]
        self.total = [0.0 for _ in range(self.NUM_METRICS)]
        self.match1, self.match2 = 0.0, 0.0

    def add_result(self, game_result):
        for i in range(self.NUM_METRICS):
            fn = self.metrics[i]
            c, t = fn(game_result)
            self.correct[i] += c
            self.total[i] += t
            if c >= 1 and i == 2: self.match1 += 1 # Found at least 1 Wolf
            if c == t and i == 2: self.match2 += 1 # Found two player wolves

    def print_results(self):
        for i in range(self.NUM_METRICS):
            if self.total[i] == 0: self.total[i] += 1
        logger.warning("Accuracy for all predictions: " + str(self.correct[0] / self.total[0]))
        logger.warning("Accuracy with lenient center scores: " + str(self.correct[1] / self.total[1]))
        logger.warning("S1: Found at least 1 Wolf: " + str(self.match1 / const.NUM_GAMES))
        logger.warning("S2: Found two player Wolves: " + str(self.match2 / const.NUM_GAMES))
        logger.warning("Correct guesses (not accusing extraneous wolves): " + str(self.correct[2] / self.total[2]))

    # Returns fraction of how many roles were guessed correctly out of all roles.
    def correctness_strict(self, game_result):
        correct = 0.0
        for i in range(const.NUM_ROLES):
            if game_result.actual[i] == game_result.guessed[i]:
                correct += 1
        return correct, const.NUM_ROLES

    # Returns fraction of how many player roles were guessed correctly.
    # Optionally adds a bonus for a matching center set.
    def correctness_lenient_center(self, game_result):
        correct = const.NUM_CENTER
        for i in range(const.NUM_PLAYERS):
            if game_result.actual[i] == game_result.guessed[i]:
                correct += 1
        center_set = dict(Counter(game_result.actual[const.NUM_PLAYERS:]))
        center_set2 = game_result.guessed[const.NUM_PLAYERS:]
        for guess in center_set2:
            if guess not in center_set or center_set[guess] == 0:
                correct -= 1
            else:
                center_set[guess] -= 1
        return correct, const.NUM_ROLES

    # Returns fraction of how many Wolves were correctly identified.
    # Only counts Wolves that are players.
    def verify_predictions(self, game_result):
        correctGuesses = 0
        totalWolves = 0
        for r in range(const.NUM_ROLES):
            if game_result.actual[r] == 'Wolf' == game_result.guessed[r]:
                correctGuesses += 1
        for card in game_result.actual[:const.NUM_PLAYERS]:
            if card == 'Wolf':
                totalWolves += 1
        return correctGuesses, totalWolves
