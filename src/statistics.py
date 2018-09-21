import const
from collections import Counter
from const import logger

class GameResult:
    ''' Each round of one_night returns a GameResult. '''
    def __init__(self, actual, guessed, statements, wolf_inds, found_single_vote_wolf=False):
        self.actual = actual
        self.guessed = guessed
        self.statements = statements
        self.wolf_inds = wolf_inds
        self.found_single_vote_wolf = found_single_vote_wolf

    def json_repr(self):
        return {
            'type': 'GameResult',
            'actual': self.actual,
            'guessed': self.guessed,
            'statements': self.statements,
            'wolf_inds': self.wolf_inds,
            'found_single_vote_wolf': self.found_single_vote_wolf
        }


class Statistics:
    ''' Initialize a Statistics object. '''
    def __init__(self):
        self.metrics = [self.correctness_strict, self.correctness_lenient_center, self.wolf_predictions_one,
                        self.wolf_predictions_all, self.wolf_predictions_center]
        if const.USE_VOTING: self.metrics.append(self.voted_wolf)
        self.NUM_METRICS = len(self.metrics)
        self.correct = [0.0 for _ in range(self.NUM_METRICS)]
        self.total = [0.0 for _ in range(self.NUM_METRICS)]
        self.match1, self.match2 = 0.0, 0.0
        self.num_games = 0

    def add_result(self, game_result):
        ''' Updates the Statistics object with a GameResult. '''
        self.num_games += 1
        for metric_index in range(self.NUM_METRICS):
            fn = self.metrics[metric_index]
            c, t = fn(game_result)
            self.correct[metric_index] += c
            self.total[metric_index] += t

    def print_statistics(self):
        ''' Outputs overall statistics of inputed game results. '''
        logger.warning('\nNumber of Games: ' + str(self.num_games))
        sentences = [
            'Accuracy for all predictions: ',
            'Accuracy with lenient center scores: ',
            'S1: Found at least 1 Wolf player: ',
            'S2: Found all Wolf players: ',
            'Percentage of correct Wolf guesses (including center Wolves): ',
            'Percentage of correct Wolf votes: '
        ]
        for i in range(self.NUM_METRICS):
            if self.total[i] == 0: self.total[i] += 1
            logger.warning(sentences[i] + str(self.correct[i] / self.total[i]))

    def correctness_strict(self, game_result):
        ''' Returns fraction of how many roles were guessed correctly out of all roles. '''
        correct = 0.0
        for i in range(const.NUM_ROLES):
            if game_result.actual[i] == game_result.guessed[i]:
                correct += 1
        return correct, const.NUM_ROLES

    def correctness_lenient_center(self, game_result):
        '''
        Returns fraction of how many player roles were guessed correctly.
        Optionally adds a bonus for a matching center set.
        '''
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

    def wolf_predictions_one(self, game_result):
        ''' Returns 1/1 if at least one Wolf was correctly identified. '''
        correctGuesses = 0
        totalWolves = 1
        for r in range(const.NUM_PLAYERS):
            if game_result.actual[r] == 'Wolf' == game_result.guessed[r]:
                correctGuesses += 1
        return int(correctGuesses > 0), totalWolves

    def wolf_predictions_all(self, game_result):
        ''' Returns 1/1 if all Wolves were correctly identified. '''
        correctGuesses = 0
        totalWolves = 0
        for r in range(const.NUM_PLAYERS):
            if game_result.actual[r] == 'Wolf':
                totalWolves += 1
                if game_result.guessed[r] == 'Wolf':
                    correctGuesses += 1
        return int(correctGuesses == totalWolves), 1

    def wolf_predictions_center(self, game_result):
        ''' Returns fraction of how many Wolves were correctly identified. '''
        correctGuesses = 0
        totalWolves = 0
        for r in range(const.NUM_ROLES):
            if game_result.actual[r] == 'Wolf':
                totalWolves += 1
                if game_result.guessed[r] == 'Wolf':
                    correctGuesses += 1
        return correctGuesses, totalWolves

    def voted_wolf(self, game_result):
        ''' Returns 1/1 if the voted character was truly a Wolf. '''
        return int(game_result.found_single_vote_wolf), 1
