''' stats.py '''
from collections import Counter
from dataclasses import dataclass
from typing import Dict, List, Tuple

from src import const
from src.const import logger
from src.roles import Player
from src.statements import Statement


@dataclass
class SavedGame:
    ''' All of the necessary data needed to rerun a game. '''
    original_roles: Tuple[str, ...]
    game_roles: List[str]
    all_statements: List[Statement]
    player_objs: List[Player]

    def load_game(self) -> Tuple[Tuple[str, ...], List[str], List[Statement], List[Player]]:
        ''' Returns game data. '''
        return self.original_roles, self.game_roles, self.all_statements, self.player_objs

    def json_repr(self) -> Dict:
        ''' Returns json representation of the GameResult. '''
        return {
            'type': 'SavedGame',
            'original_roles': self.original_roles,
            'game_roles': self.game_roles,
            'all_statements': self.all_statements,
            'player_objs': self.player_objs
        }


@dataclass
class GameResult:
    ''' Each round of one_night returns a GameResult. '''
    actual: List[str]
    guessed: List[str]
    wolf_inds: List[int]
    winning_team: str = ''

    def json_repr(self) -> Dict:
        ''' Returns json representation of the GameResult. '''
        return {
            'type': 'GameResult',
            'actual': self.actual,
            'guessed': self.guessed,
            'wolf_inds': self.wolf_inds,
            'winning_team': self.winning_team
        }


class Statistics:
    ''' Initialize a Statistics object. '''

    def __init__(self):
        self.metrics = [self.correctness_strict, self.correctness_lenient_center,
                        self.wolf_predictions_one, self.wolf_predictions_all,
                        self.wolf_predictions_center]
        if const.USE_VOTING:
            self.metrics += [self.villager_wins, self.tanner_wins, self.werewolf_wins]
        self.correct = [0.0] * len(self.metrics)
        self.total = [0.0] * len(self.metrics)
        self.num_games = 0

    def add_result(self, game_result: GameResult) -> None:
        ''' Updates the Statistics object with a GameResult. '''
        self.num_games += 1
        for metric_index in range(len(self.metrics)):
            func = self.metrics[metric_index]
            corr, tot = func(game_result)
            self.correct[metric_index] += corr
            self.total[metric_index] += tot

    def get_metric_results(self) -> Dict[str, float]:
        ''' Returns the dictionary of metric name to numeric result. '''
        output = self.compute_statistics()
        return {metric.__name__: output[i] for i, metric in enumerate(self.metrics)}

    def compute_statistics(self) -> List[float]:
        ''' Computes overall statistics of inputed game results. '''
        output = []
        for i in range(len(self.metrics)):
            total = self.total[i] if self.total[i] != 0 else 1
            output.append(self.correct[i] / total)
        return output

    def print_statistics(self) -> None:
        ''' Outputs overall statistics of inputed game results. '''
        logger.warning(f'\nNumber of Games: {self.num_games}')
        sentences = [
            'Accuracy for all predictions: ',
            'Accuracy with lenient center scores: ',
            'S1: Found at least 1 Wolf player: ',
            'S2: Found all Wolf players: ',
            'Percentage of correct Wolf guesses (including center Wolves): ',
            'Percentage of Villager Team wins: ',
            'Percentage of Tanner Team wins: ',
            'Percentage of Werewolf Team wins: '
        ]
        assert len(sentences) >= len(self.metrics)
        results = self.compute_statistics()
        for i in range(len(self.metrics)):
            logger.warning(f'{sentences[i]}{results[i]}')

    @staticmethod
    def correctness_strict(game_result: GameResult) -> Tuple[int, int]:
        ''' Returns fraction of how many roles were guessed correctly out of all roles. '''
        correct = 0
        for i in range(const.NUM_ROLES):
            if game_result.actual[i] == game_result.guessed[i]:
                correct += 1
        return correct, const.NUM_ROLES

    @staticmethod
    def correctness_lenient_center(game_result: GameResult) -> Tuple[int, int]:
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

    @staticmethod
    def wolf_predictions_one(game_result: GameResult) -> Tuple[int, int]:
        ''' Returns 1/1 if at least one Wolf was correctly identified. '''
        correct_guesses, total_wolves = 0, 1
        for i in range(const.NUM_PLAYERS):
            if game_result.actual[i] == 'Wolf' == game_result.guessed[i]:
                correct_guesses += 1
        return int(correct_guesses > 0), total_wolves

    @staticmethod
    def wolf_predictions_all(game_result: GameResult) -> Tuple[int, int]:
        ''' Returns 1/1 if all Wolves were correctly identified. '''
        correct_guesses, total_wolves = 0, 0
        for i in range(const.NUM_PLAYERS):
            if game_result.actual[i] == 'Wolf':
                total_wolves += 1
                if game_result.guessed[i] == 'Wolf':
                    correct_guesses += 1
        return int(correct_guesses == total_wolves), 1

    @staticmethod
    def wolf_predictions_center(game_result: GameResult) -> Tuple[int, int]:
        ''' Returns fraction of how many Wolves were correctly identified. '''
        correct_guesses, total_wolves = 0, 0
        for i in range(const.NUM_ROLES):
            if game_result.actual[i] == 'Wolf':
                total_wolves += 1
                if game_result.guessed[i] == 'Wolf':
                    correct_guesses += 1
        return correct_guesses, total_wolves

    @staticmethod
    def villager_wins(game_result: GameResult) -> Tuple[int, int]:
        ''' Returns 1/1 if the Villager team won. '''
        return int(game_result.winning_team == 'Villager'), 1

    @staticmethod
    def tanner_wins(game_result: GameResult) -> Tuple[int, int]:
        ''' Returns 1/1 if the Tanner won. '''
        return int(game_result.winning_team == 'Tanner'), 1

    @staticmethod
    def werewolf_wins(game_result: GameResult) -> Tuple[int, int]:
        ''' Returns 1/1 if the Werewolf team won. '''
        return int(game_result.winning_team == 'Werewolf'), 1

    def __eq__(self, other) -> bool:
        ''' Checks for equality between Statistics objects. '''
        assert isinstance(other, Statistics)
        return self.__dict__ == other.__dict__
