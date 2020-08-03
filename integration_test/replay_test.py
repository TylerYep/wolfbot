""" replay_test.py """
from src import const, one_night, replay, stats
from src.stats import GameResult


class TestReplay:
    """ Tests for the replay_game function. """

    @staticmethod
    def test_replay_game_state_small(
        example_small_game_result: GameResult, override_random: None
    ) -> None:
        """
        Correctly replay last round of one night werewolf using saved random numbers.
        """
        const.REPLAY_FILE = "unit_test/test_data/replay.json"
        one_night.play_one_night_werewolf()

        result_stats = replay.replay_game_from_state()

        stat_tracker = stats.Statistics()
        stat_tracker.add_result(example_small_game_result)
        assert result_stats == stat_tracker

    @staticmethod
    def test_replay_game_state_medium(
        example_medium_game_result: GameResult, override_random: None
    ) -> None:
        """
        Correctly replay last round of one night werewolf using saved random numbers.
        """
        const.REPLAY_FILE = "unit_test/test_data/replay.json"
        one_night.play_one_night_werewolf()

        result_stats = replay.replay_game_from_state()

        stat_tracker = stats.Statistics()
        stat_tracker.add_result(example_medium_game_result)
        assert result_stats == stat_tracker

    @staticmethod
    def test_replay_game_state_large(
        example_large_game_result: GameResult, override_random: None
    ) -> None:
        """
        Correctly replay last round of one night werewolf using saved random numbers.
        """
        const.REPLAY_FILE = "unit_test/test_data/replay.json"
        one_night.play_one_night_werewolf()

        result_stats = replay.replay_game_from_state()

        stat_tracker = stats.Statistics()
        stat_tracker.add_result(example_large_game_result)
        assert result_stats == stat_tracker
