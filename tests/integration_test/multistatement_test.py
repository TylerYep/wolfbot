""" multistatement_test.py """
from tests.conftest import write_results
from wolfbot import const, one_night
from wolfbot.enums import Role


class TestMultistatement:
    """Tests for the play_one_night_werewolf function."""

    @staticmethod
    def test_random_wolf(standard_game_roles: tuple[Role, ...]) -> None:
        """Correctly play one round of one night werewolf."""
        const.MULTI_STATEMENT = True

        stat_tracker = one_night.simulate_game(num_games=1000)

        stat_results = stat_tracker.get_metric_results()
        write_results(stat_results, "multistatement/random_wolf.csv")
        assert stat_results["villager_wins"] > 0.8
        assert stat_results["tanner_wins"] == 0
        assert stat_results["werewolf_wins"] < 0.2

    @staticmethod
    def test_reg_wolf(standard_game_roles: tuple[Role, ...]) -> None:
        """Correctly play one round of one night werewolf."""
        const.MULTI_STATEMENT = True
        const.USE_REG_WOLF = True

        stat_tracker = one_night.simulate_game(num_games=1000)

        stat_results = stat_tracker.get_metric_results()
        write_results(stat_results, "multistatement/reg_wolf.csv")
        assert stat_results["villager_wins"] < 0.51
        assert stat_results["tanner_wins"] == 0
        assert stat_results["werewolf_wins"] > 0.49

    @staticmethod
    def test_expectimax_wolf(standard_game_roles: tuple[Role, ...]) -> None:
        """Correctly play one round of one night werewolf."""
        const.USE_REG_WOLF = True
        const.EXPECTIMAX_WOLF = True
        const.MULTI_STATEMENT = True

        stat_tracker = one_night.simulate_game(num_games=500)

        stat_results = stat_tracker.get_metric_results()
        write_results(stat_results, "multistatement/expectimax_wolf.csv")
        assert stat_results["villager_wins"] < 0.6
        assert stat_results["tanner_wins"] == 0
        assert stat_results["werewolf_wins"] > 0.4
