''' aggregate_test.py '''
import json
import random

from src import one_night, const, stats

class TestAggregate:
    ''' Tests for the play_one_night_werewolf function. '''

    @staticmethod
    def test_small_aggregate_game(small_game_roles):
        ''' Correctly play one round of one night werewolf. '''
        const.ROLES = small_game_roles
        random.seed()
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
        random.seed()
        num_games = 1000
        stat_tracker = stats.Statistics()

        for _ in range(num_games):
            game_result = one_night.play_one_night_werewolf(False)
            stat_tracker.add_result(game_result)
        stat_tracker.print_statistics()
        metric_map = stat_tracker.get_metric_results()
        with open('integration_test/results/standard_results.json', 'w') as out_file:
            json.dump(metric_map, out_file, indent=2)

        assert metric_map['villager_wins'] >= 0.75
        assert metric_map['tanner_wins'] == 0
        assert metric_map['werewolf_wins'] <= 0.25

    @staticmethod
    def test_standard_aggregate_game_expectimax_wolf(standard_game_roles):
        ''' Correctly play one round of one night werewolf. '''
        const.ROLES = standard_game_roles
        const.USE_REG_WOLF = True
        const.USE_EXPECTIMAX_WOLF = True
        random.seed()
        num_games = 500
        stat_tracker = stats.Statistics()

        for _ in range(num_games):
            game_result = one_night.play_one_night_werewolf(False)
            stat_tracker.add_result(game_result)
        stat_tracker.print_statistics()
        metric_map = stat_tracker.get_metric_results()
        with open('integration_test/results/expectimax_wolf_results.json', 'w') as out_file:
            json.dump(metric_map, out_file, indent=2)

        assert metric_map['villager_wins'] < 0.6
        assert metric_map['tanner_wins'] == 0
        assert metric_map['werewolf_wins'] > 0.4
