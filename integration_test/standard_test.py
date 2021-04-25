""" standard_test.py """
import logging
import random

from conftest import set_roles, write_results
from src import const, one_night
from src.const import Role, Team
from src.stats import Statistics


class TestStandard:
    """Tests for the play_one_night_werewolf function."""

    @staticmethod
    def test_perfect_villagers() -> None:
        """Correctly play one round of one night werewolf."""
        const.NUM_PLAYERS = 10
        const.NUM_CENTER = 3
        const.RANDOMIZE_ROLES = False
        set_roles(
            Role.INSOMNIAC,
            Role.VILLAGER,
            Role.ROBBER,
            Role.VILLAGER,
            Role.SEER,
            Role.MASON,
            Role.TROUBLEMAKER,
            Role.VILLAGER,
            Role.MASON,
            Role.HUNTER,
            Role.WOLF,
            Role.WOLF,
            Role.MINION,
        )
        random.seed()

        stat_tracker = one_night.simulate_game(num_games=10)

        stat_results = stat_tracker.get_metric_results()
        assert stat_results["villager_wins"] == 1
        assert stat_results["correctness_lenient_center"] == 1
        assert stat_results["wolf_predictions_one"] == 0
        assert stat_results["wolf_predictions_all"] == 1

    @staticmethod
    def test_small_game(small_game_roles: tuple[Role, ...]) -> None:
        """Correctly play one round of one night werewolf."""
        random.seed()

        stat_tracker = one_night.simulate_game(num_games=10)

        stat_results = stat_tracker.get_metric_results()
        assert stat_results["villager_wins"] == 1

    @staticmethod
    def test_random_wolf(standard_game_roles: tuple[Role, ...]) -> None:
        """Correctly play one round of one night werewolf."""
        stat_tracker = one_night.simulate_game(num_games=1000)

        stat_results = stat_tracker.get_metric_results()
        write_results(stat_results, "standard/random_wolf.csv")
        assert stat_results["villager_wins"] > 0.8
        assert stat_results["tanner_wins"] == 0
        assert stat_results["werewolf_wins"] < 0.2

    @staticmethod
    def test_reg_wolf(standard_game_roles: tuple[Role, ...]) -> None:
        """Correctly play one round of one night werewolf."""
        const.USE_REG_WOLF = True

        stat_tracker = one_night.simulate_game(num_games=1000)

        stat_results = stat_tracker.get_metric_results()
        write_results(stat_results, "standard/reg_wolf.csv")
        assert stat_results["villager_wins"] < 0.7
        assert stat_results["tanner_wins"] == 0
        assert stat_results["werewolf_wins"] > 0.3

    @staticmethod
    def test_expectimax_wolf(standard_game_roles: tuple[Role, ...]) -> None:
        """Correctly play one round of one night werewolf."""
        const.USE_REG_WOLF = True
        const.EXPECTIMAX_WOLF = True

        stat_tracker = one_night.simulate_game(num_games=500)

        stat_results = stat_tracker.get_metric_results()
        write_results(stat_results, "standard/expectimax_wolf.csv")
        assert stat_results["villager_wins"] < 0.6
        assert stat_results["tanner_wins"] == 0
        assert stat_results["werewolf_wins"] > 0.4

    # @staticmethod
    # def test_rl_wolf(medium_game_roles: tuple[Role, ...]) -> None:
    #     """ Correctly play one round of one night werewolf. """
    #     const.USE_RL_WOLF = True

    #     stat_tracker = one_night.simulate_game(num_games=500)

    #     stat_results = stat_tracker.get_metric_results()
    #     write_results(stat_results, "standard/rl_wolf.csv")
    #     assert stat_results["villager_wins"] < 0.6
    #     assert stat_results["tanner_wins"] == 0
    #     assert stat_results["werewolf_wins"] > 0.4

    @staticmethod
    def test_random_villagers(standard_game_roles: tuple[Role, ...]) -> None:
        """Correctly play one round of one night werewolf."""
        const.USE_REG_WOLF = True
        const.EXPECTIMAX_WOLF = True
        const.SMART_VILLAGERS = False

        stat_tracker = one_night.simulate_game(num_games=100)

        stat_results = stat_tracker.get_metric_results()
        write_results(stat_results, "standard/random_villagers.csv")
        assert stat_results["villager_wins"] < 0.4
        assert stat_results["tanner_wins"] == 0
        assert stat_results["werewolf_wins"] > 0.6

    @staticmethod
    def test_expectimax_tanner() -> None:
        """Correctly play one round of one night werewolf."""
        const.NUM_PLAYERS = 9
        const.NUM_CENTER = 3
        const.EXPECTIMAX_TANNER = True
        const.RANDOMIZE_ROLES = False
        set_roles(
            Role.INSOMNIAC,
            Role.HUNTER,
            Role.MASON,
            Role.MASON,
            Role.ROBBER,
            Role.SEER,
            Role.TANNER,
            Role.TROUBLEMAKER,
            Role.VILLAGER,
            Role.VILLAGER,
            Role.VILLAGER,
            Role.WOLF,
        )

        stat_tracker = one_night.simulate_game(num_games=20)

        stat_results = stat_tracker.get_metric_results()
        write_results(stat_results, "standard/expectimax_tanner.csv")
        assert stat_results["tanner_wins"] > 0.8

    @staticmethod
    def test_relaxed_solver_improvement(large_game_roles: tuple[Role, ...]) -> None:
        """Correctly play one round of one night werewolf."""
        const.USE_REG_WOLF = True
        const.logger.set_level(logging.WARNING)
        stat_tracker_1, stat_tracker_2 = Statistics(), Statistics()

        games_won_with_relaxed_solver = 0
        for i in range(5):
            random.seed(i)
            const.USE_RELAXED_SOLVER = True
            game_result_1 = one_night.play_one_night_werewolf(save_replay=False)
            stat_tracker_1.add_result(game_result_1)

            random.seed(i)
            const.USE_RELAXED_SOLVER = False
            game_result_2 = one_night.play_one_night_werewolf(save_replay=False)
            stat_tracker_2.add_result(game_result_2)

            if (
                game_result_1.winning_team is Team.VILLAGE
                and game_result_2.winning_team is not Team.VILLAGE
            ):
                games_won_with_relaxed_solver += 1

        stat_tracker_1.print_statistics()
        stat_tracker_2.print_statistics()
        assert games_won_with_relaxed_solver > 0
