import time
from collections import Counter
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, override

from wolfbot import const
from wolfbot.enums import Role, Team
from wolfbot.log import logger
from wolfbot.roles import Player
from wolfbot.statements import Statement


@dataclass(slots=True)
class SavedGame:
    """All of the necessary data needed to rerun a game."""

    original_roles: tuple[Role, ...]
    game_roles: tuple[Role, ...]
    all_statements: tuple[Statement, ...]
    player_objs: tuple[Player, ...]

    def load_game(
        self,
    ) -> tuple[
        tuple[Role, ...], tuple[Role, ...], tuple[Statement, ...], tuple[Player, ...]
    ]:
        """Returns game data."""
        return (
            self.original_roles,
            self.game_roles,
            self.all_statements,
            self.player_objs,
        )

    def json_repr(self) -> dict[str, Any]:
        """Returns json representation of the GameResult."""
        return {
            "type": "SavedGame",
            "original_roles": self.original_roles,
            "game_roles": self.game_roles,
            "all_statements": self.all_statements,
            "player_objs": self.player_objs,
        }


@dataclass(slots=True)
class GameResult:
    """Each round of one_night returns a GameResult."""

    actual: tuple[Role, ...]
    guessed: tuple[Role, ...]
    wolf_inds: tuple[int, ...]
    winning_team: Team
    statements: tuple[Statement, ...]

    def json_repr(self) -> dict[str, Any]:
        """Returns json representation of the GameResult."""
        return {
            "type": "GameResult",
            "actual": self.actual,
            "guessed": self.guessed,
            "statements": self.statements,
            "wolf_inds": self.wolf_inds,
            "winning_team": self.winning_team,
        }


@dataclass(slots=True)
class Metric:
    """One metric for a game."""

    function: Callable[..., tuple[int, int]]
    sentence: str
    correct: int = 0
    total: int = 0
    average: float = 0

    def update(self, game_result: GameResult) -> None:
        """Update the Metric by aggregating a new result."""
        correct, total = self.function(game_result)
        self.correct += correct
        self.total += total
        self.average = self.correct / (self.total or 1)


class Statistics:
    """Initialize a Statistics object."""

    def __init__(self) -> None:
        metric_fns = [
            self.correctness_strict,
            self.correctness_lenient_center,
            self.wolf_predictions_one,
            self.wolf_predictions_all,
            self.wolf_predictions_center,
            self.villager_wins,
            self.tanner_wins,
            self.werewolf_wins,
        ]
        sentences = [
            "Accuracy for all predictions",
            "Accuracy with lenient center scores",
            "S1: Found at least 1 Wolf player",
            "S2: Found all Wolf players",
            "Percentage of correct Wolf guesses",
            "Percentage of Villager Team wins",
            "Percentage of Tanner Team wins",
            "Percentage of Werewolf Team wins",
        ]
        if const.INTERACTIVE_MODE:
            metric_fns = metric_fns[-3:]
            sentences = sentences[-3:]
        self.num_games = 0
        self.metrics = [
            Metric(metric_fns[i], sentences[i]) for i in range(len(metric_fns))
        ]
        self.start_time = time.perf_counter()
        self.end_time = 0.0

    @override
    def __eq__(self, other: object) -> bool:
        """Checks for equality between Statistics objects."""
        if isinstance(other, Statistics):
            return self.get_metric_results(False) == other.get_metric_results(False)
        return NotImplemented

    @staticmethod
    def correctness_strict(game_result: GameResult) -> tuple[int, int]:
        """
        Returns fraction of how many roles were guessed correctly out of all roles.
        """
        correct = 0
        for i in range(const.NUM_ROLES):
            if game_result.actual[i] is game_result.guessed[i]:
                correct += 1
        return correct, const.NUM_ROLES

    @staticmethod
    def correctness_lenient_center(game_result: GameResult) -> tuple[int, int]:
        """
        Returns fraction of how many player roles were guessed correctly.
        Optionally adds a bonus for a matching center set.
        """
        correct = const.NUM_CENTER
        for i in range(const.NUM_PLAYERS):
            if game_result.actual[i] is game_result.guessed[i]:
                correct += 1
        center_set = Counter(game_result.actual[const.NUM_PLAYERS :])
        center_set2 = game_result.guessed[const.NUM_PLAYERS :]
        for guess in center_set2:
            if guess not in center_set or center_set[guess] == 0:
                correct -= 1
            else:
                center_set[guess] -= 1
        return correct, const.NUM_ROLES

    @staticmethod
    def wolf_predictions_one(game_result: GameResult) -> tuple[int, int]:
        """Returns 1/1 if at least one Wolf was correctly identified."""
        correct_guesses, total_wolves = 0, 1
        for i in range(const.NUM_PLAYERS):
            if game_result.actual[i] is Role.WOLF is game_result.guessed[i]:
                correct_guesses += 1
        return int(correct_guesses > 0), total_wolves

    @staticmethod
    def wolf_predictions_all(game_result: GameResult) -> tuple[int, int]:
        """Returns 1/1 if all Wolves were correctly identified."""
        correct_guesses, total_wolves = 0, 0
        for i in range(const.NUM_PLAYERS):
            if game_result.actual[i] is Role.WOLF:
                total_wolves += 1
                if game_result.guessed[i] is Role.WOLF:
                    correct_guesses += 1
        return int(correct_guesses == total_wolves), 1

    @staticmethod
    def wolf_predictions_center(game_result: GameResult) -> tuple[int, int]:
        """Returns fraction of how many Wolves were correctly identified."""
        correct_guesses, total_wolves = 0, 0
        for i in range(const.NUM_ROLES):
            if game_result.actual[i] is Role.WOLF:
                total_wolves += 1
                if game_result.guessed[i] is Role.WOLF:
                    correct_guesses += 1
        return correct_guesses, total_wolves

    @staticmethod
    def villager_wins(game_result: GameResult) -> tuple[int, int]:
        """Returns 1/1 if the Village team won."""
        return int(game_result.winning_team is Team.VILLAGE), 1

    @staticmethod
    def tanner_wins(game_result: GameResult) -> tuple[int, int]:
        """Returns 1/1 if the Tanner won."""
        return int(game_result.winning_team is Team.TANNER), 1

    @staticmethod
    def werewolf_wins(game_result: GameResult) -> tuple[int, int]:
        """Returns 1/1 if the Werewolf team won."""
        return int(game_result.winning_team is Team.WEREWOLF), 1

    def add_result(self, game_result: GameResult) -> None:
        """Updates the Statistics object with a GameResult."""
        self.num_games += 1
        for metric in self.metrics:
            metric.update(game_result)
        self.end_time = time.perf_counter() - self.start_time

    def get_metric_results(self, include_time: bool = True) -> dict[str, float]:
        """
        Returns the dictionary of metric name to metric name.
        """
        results = {metric.function.__name__: metric.average for metric in self.metrics}
        results["num_games"] = self.num_games
        if include_time:
            results["time_elapsed"] = self.end_time
        return results

    def print_statistics(self) -> None:
        """Outputs overall statistics of inputed game results."""
        logger.warning(f"\nNumber of Games: {self.num_games}")
        max_len_sentence = max(len(m.sentence) for m in self.metrics)
        for metric in self.metrics:
            logger.warning(
                f"{metric.sentence:<{max_len_sentence}}: "
                f"{metric.correct}/{metric.total} ({metric.average:.1%})"
            )
        print(f"\nTime Elapsed: {self.end_time}")
