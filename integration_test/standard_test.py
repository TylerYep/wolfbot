""" standard_test.py """
import random

from conftest import reset_misc_const_fields, write_results
from src import const, one_night


class TestStandard:
    """ Tests for the play_one_night_werewolf function. """

    @staticmethod
    def test_perfect_villagers():
        """ Correctly play one round of one night werewolf. """
        const.ROLES = (
            "Insomniac",
            "Villager",
            "Robber",
            "Villager",
            "Seer",
            "Mason",
            "Troublemaker",
            "Villager",
            "Mason",
            "Hunter",
            "Wolf",
            "Wolf",
            "Minion",
        )
        const.NUM_PLAYERS = 10
        const.NUM_CENTER = 3
        const.RANDOMIZE_ROLES = False
        reset_misc_const_fields()
        random.seed()

        stat_tracker = one_night.simulate_game(num_games=10, disable_logging=False)

        stat_results = stat_tracker.get_metric_results()
        assert stat_results["villager_wins"] == 1.0
        assert stat_results["correctness_lenient_center"] == 1.0
        assert stat_results["wolf_predictions_one"] == 0.0
        assert stat_results["wolf_predictions_all"] == 1.0

    @staticmethod
    def test_small_game(small_game_roles):
        """ Correctly play one round of one night werewolf. """
        const.ROLES = small_game_roles
        random.seed()

        stat_tracker = one_night.simulate_game(num_games=10)

        stat_results = stat_tracker.get_metric_results()
        assert stat_results["villager_wins"] == 1.0

    @staticmethod
    def test_standard_game(standard_game_roles):
        """ Correctly play one round of one night werewolf. """
        const.ROLES = standard_game_roles

        stat_tracker = one_night.simulate_game(num_games=1000)

        stat_results = stat_tracker.get_metric_results()
        write_results("standard_results.csv", stat_results)
        assert stat_results["villager_wins"] > 0.8
        assert stat_results["tanner_wins"] == 0
        assert stat_results["werewolf_wins"] < 0.2

    @staticmethod
    def test_standard_game_expectimax_wolf(standard_game_roles):
        """ Correctly play one round of one night werewolf. """
        const.ROLES = standard_game_roles
        const.USE_REG_WOLF = True
        const.EXPECTIMAX_PLAYER = True

        stat_tracker = one_night.simulate_game(num_games=500)

        stat_results = stat_tracker.get_metric_results()
        write_results("expectimax_wolf_results.csv", stat_results)
        assert stat_results["villager_wins"] < 0.5
        assert stat_results["tanner_wins"] == 0
        assert stat_results["werewolf_wins"] > 0.5
