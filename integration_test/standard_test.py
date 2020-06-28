""" standard_test.py """
import random

from conftest import set_roles, write_results
from src import const, one_night


class TestStandard:
    """ Tests for the play_one_night_werewolf function. """

    @staticmethod
    def test_perfect_villagers():
        """ Correctly play one round of one night werewolf. """
        const.NUM_PLAYERS = 10
        const.NUM_CENTER = 3
        const.RANDOMIZE_ROLES = False
        set_roles(
            (
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
        )
        random.seed()

        stat_tracker = one_night.simulate_game(num_games=10)

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
    def test_random_wolf(standard_game_roles):
        """ Correctly play one round of one night werewolf. """
        const.ROLES = standard_game_roles

        stat_tracker = one_night.simulate_game(num_games=1000)

        stat_results = stat_tracker.get_metric_results()
        write_results(stat_results, "standard/random.csv")
        assert stat_results["villager_wins"] > 0.8
        assert stat_results["tanner_wins"] == 0
        assert stat_results["werewolf_wins"] < 0.2

    @staticmethod
    def test_reg_wolf(standard_game_roles):
        """ Correctly play one round of one night werewolf. """
        const.ROLES = standard_game_roles
        const.USE_REG_WOLF = True

        stat_tracker = one_night.simulate_game(num_games=1000)

        stat_results = stat_tracker.get_metric_results()
        write_results(stat_results, "standard/reg_wolf.csv")
        assert stat_results["villager_wins"] < 0.7
        assert stat_results["tanner_wins"] == 0
        assert stat_results["werewolf_wins"] > 0.3

    @staticmethod
    def test_expectimax_wolf(standard_game_roles):
        """ Correctly play one round of one night werewolf. """
        const.ROLES = standard_game_roles
        const.USE_REG_WOLF = True
        const.EXPECTIMAX_WOLF = True

        stat_tracker = one_night.simulate_game(num_games=500)

        stat_results = stat_tracker.get_metric_results()
        write_results(stat_results, "standard/expectimax_wolf.csv")
        assert stat_results["villager_wins"] < 0.55
        assert stat_results["tanner_wins"] == 0
        assert stat_results["werewolf_wins"] > 0.45

    @staticmethod
    def test_random_villagers(standard_game_roles):
        """ Correctly play one round of one night werewolf. """
        const.ROLES = standard_game_roles
        const.USE_REG_WOLF = True
        const.EXPECTIMAX_WOLF = True
        const.SMART_VILLAGERS = False

        stat_tracker = one_night.simulate_game(num_games=100)

        stat_results = stat_tracker.get_metric_results()
        write_results(stat_results, "random_villagers.csv")
        assert stat_results["villager_wins"] < 0.35
        assert stat_results["tanner_wins"] == 0
        assert stat_results["werewolf_wins"] > 0.65

    @staticmethod
    def test_expectimax_tanner():
        """ Correctly play one round of one night werewolf. """
        const.NUM_PLAYERS = 9
        const.NUM_CENTER = 3
        const.EXPECTIMAX_TANNER = True
        const.RANDOMIZE_ROLES = False
        set_roles(
            (
                "Insomniac",
                "Hunter",
                "Mason",
                "Mason",
                "Robber",
                "Seer",
                "Tanner",
                "Troublemaker",
                "Villager",
                "Villager",
                "Villager",
                "Wolf",
            )
        )

        stat_tracker = one_night.simulate_game(num_games=20)

        stat_results = stat_tracker.get_metric_results()
        write_results(stat_results, "standard/expectimax_tanner.csv")
        assert stat_results["tanner_wins"] > 0.8
