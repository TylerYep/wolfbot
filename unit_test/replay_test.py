""" replay_test.py """
from typing import Tuple

from src import one_night, replay
from src.const import Role


class TestReplay:
    """ Tests for the replay_game function. """

    @staticmethod
    def test_replay_game_state_small(
        small_game_roles: Tuple[Role, ...], override_random: None
    ) -> None:
        """
        Correctly replay last round of one night werewolf using saved random numbers.
        """
        game_result = one_night.play_one_night_werewolf()

        replay_game_result = replay.replay_game_from_state()

        assert game_result == replay_game_result

    @staticmethod
    def test_replay_game_state_medium(
        medium_game_roles: Tuple[Role, ...], override_random: None
    ) -> None:
        """
        Correctly replay last round of one night werewolf using saved random numbers.
        """
        game_result = one_night.play_one_night_werewolf()

        replay_game_result = replay.replay_game_from_state()

        assert game_result == replay_game_result

    # @staticmethod
    # def test_replay_game_state_large(
    #     large_game_roles: Tuple[Role, ...], override_random: None
    # ) -> None:
    #     """
    #     Correctly replay last round of one night werewolf using saved random numbers.
    #     """
    #     game_result = one_night.play_one_night_werewolf()

    #     replay_game_result = replay.replay_game_from_state()

    #     assert game_result == replay_game_result
