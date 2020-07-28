""" replay_test.py """
from src import const, one_night, replay, stats


class TestReplay:
    """ Tests for the replay_game function. """

    @staticmethod
    def test_replay_game_state_small(example_small_game_result) -> None:
        """
        Correctly replay last round of one night werewolf.
        Note that the result is currently not the same as the first run, since
        the second predictions receive different random numbers.
        """
        const.REPLAY_FILE = "unit_test/test_data/replay.json"
        one_night.play_one_night_werewolf()

        result_stats = replay.replay_game_from_state()

        stat_tracker = stats.Statistics()
        stat_tracker.add_result(example_small_game_result)
        assert result_stats == stat_tracker

    @staticmethod
    def test_replay_game_small(example_small_game_result) -> None:
        """
        Correctly replay last round of one night werewolf.
        Note that the result is always not the same as the first run, as
        the second predictions receive different random numbers.
        """
        const.REPLAY_FILE = "unit_test/test_data/replay.json"
        one_night.play_one_night_werewolf()

        result = replay.replay_game()

        assert result == example_small_game_result

    @staticmethod
    def test_replay_game_medium(example_medium_game_result) -> None:
        """
        Correctly replay last round of one night werewolf.
        Note that the result is always not the same as the first run, as
        the second predictions receive different random numbers.
        """
        const.REPLAY_FILE = "unit_test/test_data/replay.json"
        one_night.play_one_night_werewolf()

        result = replay.replay_game()

        assert result == example_medium_game_result

    @staticmethod
    def test_replay_game_large(example_large_game_result) -> None:
        """
        Correctly replay last round of one night werewolf.
        Note that the result is always not the same as the first run, as
        the second predictions receive different random numbers.
        """
        const.REPLAY_FILE = "unit_test/test_data/replay.json"
        one_night.play_one_night_werewolf()
        expected = example_large_game_result
        expected.guessed = [
            "Villager",
            "Insomniac",
            "Mason",
            "Wolf",
            "Villager",
            "Drunk",
            "Seer",
            "Tanner",
            "Minion",
            "Villager",
            "Wolf",
            "Hunter",
            "Troublemaker",
            "Mason",
            "Robber",
        ]
        expected.winning_team = "Tanner"

        result = replay.replay_game()

        assert result == expected
