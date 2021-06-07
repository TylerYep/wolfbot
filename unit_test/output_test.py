""" output_test.py """
import pytest

from conftest import verify_output_file
from wolfbot import one_night
from wolfbot.stats import GameResult


class TestPlayOneNightWerewolf:
    """Tests for the play_one_night_werewolf function."""

    @staticmethod
    def test_one_night_small(
        caplog: pytest.LogCaptureFixture,
        example_small_game_result: GameResult,
        override_random: None,
    ) -> None:
        """Correctly play one round of one night werewolf."""
        result = one_night.play_one_night_werewolf()

        assert result == example_small_game_result
        verify_output_file(caplog, "unit_test/test_data/one_night_small.out")

    @staticmethod
    def test_one_night_medium(
        caplog: pytest.LogCaptureFixture,
        example_medium_game_result: GameResult,
        override_random: None,
    ) -> None:
        """Correctly play one round of one night werewolf."""
        result = one_night.play_one_night_werewolf()

        assert result == example_medium_game_result
        verify_output_file(caplog, "unit_test/test_data/one_night_medium.out")

    @staticmethod
    def test_one_night_large(
        caplog: pytest.LogCaptureFixture,
        example_large_game_result: GameResult,
        override_random: None,
    ) -> None:
        """Correctly play one round of one night werewolf."""
        result = one_night.play_one_night_werewolf()

        assert result == example_large_game_result
        verify_output_file(caplog, "unit_test/test_data/one_night_large.out")


# class TestPlayOneNightWerewolfInteractive:
#     """ Tests for the play_one_night_werewolf function. """

#     @staticmethod
#     def test_one_night_small(monkeypatch, example_small_game_result) -> None:
#         """ Correctly play one round of one night werewolf. """
#         const.INTERACTIVE_MODE = True
#         monkeypatch.setattr('builtins.input', lambda x: "0")

#         result = one_night.play_one_night_werewolf()

#         assert result == example_small_game_result
