''' aggregate_test.py '''
import pytest

from src import one_night, const, stats

class TestAggregate:
    ''' Tests for the play_one_night_werewolf function. '''

    @staticmethod
    def test_small_aggregate_game(small_game_roles):
        ''' Correctly play one round of one night werewolf. '''
        const.ROLES = small_game_roles
        num_games = 10
        stat_tracker = stats.Statistics()

        for _ in range(num_games):
            game_result = one_night.play_one_night_werewolf(False)
            stat_tracker.add_result(game_result)
        stat_tracker.print_statistics()
        metric_map = stat_tracker.get_metric_results()

        assert metric_map['villager_wins'] == 1.0

    @staticmethod
    def test_standard_aggregate_game(standard_game_roles):
        ''' Correctly play one round of one night werewolf. '''
        const.ROLES = standard_game_roles
        num_games = 100
        stat_tracker = stats.Statistics()

        for _ in range(num_games):
            game_result = one_night.play_one_night_werewolf(False)
            stat_tracker.add_result(game_result)
        stat_tracker.print_statistics()
        metric_map = stat_tracker.get_metric_results()

        assert metric_map['villager_wins'] >= 0.65
        assert metric_map['tanner_wins'] == 0
        assert metric_map['werewolf_wins'] <= 0.35

    @staticmethod
    def test_standard_aggregate_game_smart_wolf(standard_game_roles):
        ''' Correctly play one round of one night werewolf. '''
        const.ROLES = standard_game_roles
        const.USE_REG_WOLF = True
        const.USE_EXPECTIMAX_WOLF = True
        num_games = 100
        stat_tracker = stats.Statistics()

        for _ in range(num_games):
            game_result = one_night.play_one_night_werewolf(False)
            stat_tracker.add_result(game_result)
        stat_tracker.print_statistics()
        metric_map = stat_tracker.get_metric_results()

        assert metric_map['villager_wins'] <= 0.45
        assert metric_map['tanner_wins'] == 0
        assert metric_map['werewolf_wins'] >= 0.55
