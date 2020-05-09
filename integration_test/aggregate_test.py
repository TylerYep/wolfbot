""" aggregate_test.py """
import csv
import os
import random

from src import const, one_night


class TestAggregate:
    """ Tests for the play_one_night_werewolf function. """

    @staticmethod
    def test_small_aggregate_game(small_game_roles):
        """ Correctly play one round of one night werewolf. """
        const.ROLES = small_game_roles
        random.seed()

        stat_results = one_night.simulate_game(num_games=10)

        assert stat_results["villager_wins"] == 1.0

    @staticmethod
    def test_standard_aggregate_game(standard_game_roles):
        """ Correctly play one round of one night werewolf. """
        const.ROLES = standard_game_roles

        stat_results = one_night.simulate_game(num_games=1000)

        write_results("standard_results.csv", stat_results)
        assert stat_results["villager_wins"] > 0.8
        assert stat_results["tanner_wins"] == 0
        assert stat_results["werewolf_wins"] < 0.2

    @staticmethod
    def test_standard_aggregate_game_expectimax_wolf(standard_game_roles):
        """ Correctly play one round of one night werewolf. """
        const.ROLES = standard_game_roles
        const.USE_REG_WOLF = True
        const.USE_EXPECTIMAX_WOLF = True

        stat_results = one_night.simulate_game(num_games=500)

        write_results("expectimax_wolf_results.csv", stat_results)
        assert stat_results["villager_wins"] < 0.6
        assert stat_results["tanner_wins"] == 0
        assert stat_results["werewolf_wins"] > 0.4


def write_results(filename, stat_results):
    """ Writes stat_results to corresponding csv file. """
    results_filename = os.path.join("integration_test/results/", filename)
    with open(results_filename, "a+") as out_file:
        writer = csv.DictWriter(out_file, fieldnames=stat_results.keys())
        if os.path.getsize(results_filename) == 0:
            writer.writeheader()
        writer.writerow(stat_results)
