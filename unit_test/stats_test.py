""" stats_test.py """
from src import stats
from src.roles import Robber, Seer, Villager
from src.statements import Statement


class TestSavedGame:
    """ Tests for the SavedGame class. """

    @staticmethod
    def test_constructor():
        """ Should initialize correctly. """
        villager_statement = Statement("I am a Villager.", ((0, {"Villager"}),), (), "Villager")

        result = stats.SavedGame(("Villager"), ["Villager"], [villager_statement], [Villager(0)])

        assert isinstance(result, stats.SavedGame)

    @staticmethod
    def test_json_repr(example_small_saved_game):
        """ Should convert a SavedGame into a dict with all of its fields. """
        result = example_small_saved_game.json_repr()

        assert result == {
            "all_statements": [
                Statement("I am a Villager.", ((0, {"Villager"}),), (), "Villager"),
                Statement(
                    "I am a Robber and I swapped with Player 2. I am now a Seer.",
                    ((1, {"Robber"}), (2, {"Seer"}),),
                    ((1, 1, 2),),
                    "Robber",
                ),
                Statement(
                    "I am a Seer and I saw that Player 1 was a Robber.",
                    ((2, {"Seer"}), (1, {"Robber"}),),
                    (),
                    "Seer",
                ),
            ],
            "game_roles": ["Villager", "Seer", "Robber"],
            "original_roles": ("Villager", "Robber", "Seer"),
            "player_objs": [
                Villager(0),
                Robber(1, 2, "Seer"),
                Seer(2, (1, "Robber"), (None, None)),
            ],
            "type": "SavedGame",
        }

    @staticmethod
    def test_eq(example_small_saved_game):
        """ Should declare two SavedGames with identical fields to be equal. """
        not_a_saved_game = "hello"

        result = stats.SavedGame(
            ("Villager", "Robber", "Seer"),
            ["Villager", "Seer", "Robber"],
            [
                Statement("I am a Villager.", ((0, {"Villager"}),), (), "Villager"),
                Statement(
                    "I am a Robber and I swapped with Player 2. I am now a Seer.",
                    ((1, {"Robber"}), (2, {"Seer"}),),
                    ((1, 1, 2),),
                    "Robber",
                ),
                Statement(
                    "I am a Seer and I saw that Player 1 was a Robber.",
                    ((2, {"Seer"}), (1, {"Robber"}),),
                    (),
                    "Seer",
                ),
            ],
            [Villager(0), Robber(1, 2, "Seer"), Seer(2, (1, "Robber"), (None, None))],
        )

        assert result == example_small_saved_game
        assert example_small_saved_game != not_a_saved_game


class TestGameResult:
    """ Tests for the GameResult class. """

    @staticmethod
    def test_constructor():
        """ Should initialize correctly. """
        result = stats.GameResult(["Wolf"], ["Wolf"], [0], "Werewolf")

        assert isinstance(result, stats.GameResult)

    @staticmethod
    def test_json_repr(example_small_game_result):
        """ Should convert a GameResult into a dict with all of its fields. """
        result = example_small_game_result.json_repr()

        assert result == {
            "actual": ["Villager", "Seer", "Robber"],
            "guessed": ["Villager", "Seer", "Robber"],
            "type": "GameResult",
            "winning_team": "Villager",
            "wolf_inds": [],
        }

    @staticmethod
    def test_repr(example_small_game_result):
        """ Should convert a GameResult into a string with all useful fields. """
        expected = (
            "GameResult(actual=['Villager', 'Seer', 'Robber'], "
            "guessed=['Villager', 'Seer', 'Robber'], "
            "wolf_inds=[], winning_team='Villager')"
        )

        result = str(example_small_game_result)

        assert result == expected

    @staticmethod
    def test_eq(example_small_game_result):
        """ Should declare two GameResults with identical fields to be equal. """
        not_a_game_result = "hello"

        result = stats.GameResult(
            ["Villager", "Seer", "Robber"], ["Villager", "Seer", "Robber"], [], "Villager"
        )

        assert result == example_small_game_result
        assert example_small_game_result != not_a_game_result


class TestStatistics:
    """ Tests for the Statistics class. """

    @staticmethod
    def test_constructor():
        """ Should initialize correctly. """
        result = stats.Statistics()

        assert result.num_games == 0
        assert len(result.metrics) == 8

    @staticmethod
    def test_add_result(example_medium_game_result):
        """ Should correctly add a single game result to the aggregate. """
        stat_tracker = stats.Statistics()

        stat_tracker.add_result(example_medium_game_result)

        correct = [6.0, 6.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0]
        total = [6.0, 6.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
        assert stat_tracker.num_games == 1
        assert all(
            metric.correct == correct[i] and metric.total == total[i]
            for i, metric in enumerate(stat_tracker.metrics)
        )

    @staticmethod
    def test_print_statistics(caplog, example_medium_game_result):
        """ Should correctly print out the current statistics for the games. """
        stat_tracker = stats.Statistics()
        stat_tracker.add_result(example_medium_game_result)
        expected = ""

        stat_tracker.print_statistics()

        captured = list(map(lambda x: x.getMessage(), caplog.records))
        expected = (
            "\nNumber of Games: 1",
            "Accuracy for all predictions: 1.0",
            "Accuracy with lenient center scores: 1.0",
            "S1: Found at least 1 Wolf player: 1.0",
            "S2: Found all Wolf players: 1.0",
            "Percentage of correct Wolf guesses (including center Wolves): 1.0",
            "Percentage of Villager Team wins: 1.0",
            "Percentage of Tanner Team wins: 0.0",
            "Percentage of Werewolf Team wins: 0.0",
        )
        assert "\n".join(captured) == "\n".join(expected)
