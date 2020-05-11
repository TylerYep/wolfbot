""" standard_test.py """
import random

from conftest import write_results
from src import const, one_night


class TestStandard:
    """ Tests for the play_one_night_werewolf function. """

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
        const.USE_EXPECTIMAX_WOLF = True

        stat_tracker = one_night.simulate_game(num_games=500)

        stat_results = stat_tracker.get_metric_results()
        write_results("expectimax_wolf_results.csv", stat_results)
        assert stat_results["villager_wins"] < 0.5
        assert stat_results["tanner_wins"] == 0
        assert stat_results["werewolf_wins"] > 0.5
