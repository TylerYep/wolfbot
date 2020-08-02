""" stats_test.py """
from _pytest.logging import LogCaptureFixture

from conftest import verify_output
from src import stats
from src.const import Role, SwitchPriority, Team
from src.roles import Robber, Seer, Villager
from src.statements import Statement
from src.stats import GameResult, SavedGame, Statistics


class TestSavedGame:
    """ Tests for the SavedGame class. """

    @staticmethod
    def test_constructor() -> None:
        """ Should initialize correctly. """
        villager_statement = Statement("I am a Villager.", ((0, frozenset({Role.VILLAGER})),))

        result = SavedGame(
            (Role.VILLAGER,), (Role.VILLAGER,), (villager_statement,), (Villager(0),)
        )

        assert isinstance(result, stats.SavedGame)

    @staticmethod
    def test_json_repr(example_small_saved_game: SavedGame) -> None:
        """ Should convert a SavedGame into a dict with all of its fields. """
        result = example_small_saved_game.json_repr()

        assert result == {
            "all_statements": (
                Statement("I am a Villager.", ((0, frozenset({Role.VILLAGER})),)),
                Statement(
                    "I am a Robber and I swapped with Player 2. I am now a Seer.",
                    ((1, frozenset({Role.ROBBER})), (2, frozenset({Role.SEER}))),
                    ((SwitchPriority.ROBBER, 1, 2),),
                ),
                Statement(
                    "I am a Seer and I saw that Player 1 was a Robber.",
                    ((2, frozenset({Role.SEER})), (1, frozenset({Role.ROBBER}))),
                ),
            ),
            "game_roles": (Role.VILLAGER, Role.SEER, Role.ROBBER),
            "original_roles": (Role.VILLAGER, Role.ROBBER, Role.SEER),
            "player_objs": (Villager(0), Robber(1, 2, Role.SEER), Seer(2, (1, Role.ROBBER))),
            "type": "SavedGame",
        }


class TestGameResult:
    """ Tests for the GameResult class. """

    @staticmethod
    def test_constructor() -> None:
        """ Should initialize correctly. """
        result = GameResult((Role.WOLF,), (Role.WOLF,), (0,), Team.WEREWOLF, ())

        assert isinstance(result, stats.GameResult)

    @staticmethod
    def test_json_repr(example_small_game_result: GameResult) -> None:
        """ Should convert a GameResult into a dict with all of its fields. """
        result = example_small_game_result.json_repr()

        assert result == {
            "actual": (Role.VILLAGER, Role.SEER, Role.ROBBER),
            "guessed": (Role.VILLAGER, Role.SEER, Role.ROBBER),
            "type": "GameResult",
            "winning_team": Team.VILLAGE,
            "wolf_inds": (),
            "statements": (
                Statement("I am a Villager.", ((0, frozenset({Role.VILLAGER})),)),
                Statement(
                    "I am a Robber and I swapped with Player 2. I am now a Seer.",
                    ((1, frozenset({Role.ROBBER})), (2, frozenset({Role.SEER}))),
                    ((SwitchPriority.ROBBER, 1, 2),),
                ),
                Statement(
                    "I am a Seer and I saw that Player 0 was a Villager.",
                    ((2, frozenset({Role.SEER})), (0, frozenset({Role.VILLAGER}))),
                ),
            ),
        }


class TestStatistics:
    """ Tests for the Statistics class. """

    @staticmethod
    def test_constructor() -> None:
        """ Should initialize correctly. """
        result = Statistics()

        assert result.num_games == 0
        assert len(result.metrics) == 8

    @staticmethod
    def test_add_result(example_medium_game_result: GameResult) -> None:
        """ Should correctly add a single game result to the aggregate. """
        stat_tracker = Statistics()

        stat_tracker.add_result(example_medium_game_result)

        # To update these, refer to the output of print_statistics.
        correct = [4.0, 4.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0]
        total = [6.0, 6.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
        assert stat_tracker.num_games == 1
        assert all(
            metric.correct == correct[i] and metric.total == total[i]
            for i, metric in enumerate(stat_tracker.metrics)
        )

    @staticmethod
    def test_print_statistics(
        caplog: LogCaptureFixture, example_medium_game_result: GameResult
    ) -> None:
        """ Should correctly print out the current statistics for the games. """
        stat_tracker = Statistics()
        stat_tracker.add_result(example_medium_game_result)

        stat_tracker.print_statistics()

        expected = (
            "\nNumber of Games: 1",
            "Accuracy for all predictions: 0.6666666666666666",
            "Accuracy with lenient center scores: 0.6666666666666666",
            "S1: Found at least 1 Wolf player: 0.0",
            "S2: Found all Wolf players: 0.0",
            "Percentage of correct Wolf guesses (including center Wolves): 0.0",
            "Percentage of Villager Team wins: 0.0",
            "Percentage of Tanner Team wins: 0.0",
            "Percentage of Werewolf Team wins: 1.0",
        )
        verify_output(caplog, expected)
