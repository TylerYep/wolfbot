""" one_night_test.py """
from conftest import verify_output_file
from src import one_night


class TestPlayOneNightWerewolf:
    """ Tests for the play_one_night_werewolf function. """

    @staticmethod
    def test_one_night_small(caplog, example_small_game_result):
        """ Correctly play one round of one night werewolf. """
        result = one_night.play_one_night_werewolf()

        assert result == example_small_game_result
        verify_output_file(caplog, "unit_test/test_data/one_night_small.out")

    @staticmethod
    def test_one_night_medium(caplog, example_medium_game_result):
        """ Correctly play one round of one night werewolf. """
        result = one_night.play_one_night_werewolf()

        assert result == example_medium_game_result
        verify_output_file(caplog, "unit_test/test_data/one_night_medium.out")

    @staticmethod
    def test_one_night_large(caplog, example_large_game_result):
        """ Correctly play one round of one night werewolf. """
        result = one_night.play_one_night_werewolf()

        assert result == example_large_game_result
        verify_output_file(caplog, "unit_test/test_data/one_night_large.out")


# class TestPlayOneNightWerewolfInteractive:
#     """ Tests for the play_one_night_werewolf function. """

#     @staticmethod
#     def test_one_night_small(monkeypatch, example_small_game_result):
#         """ Correctly play one round of one night werewolf. """
#         const.INTERACTIVE_MODE_ON = True
#         monkeypatch.setattr('builtins.input', lambda x: "0")

#         result = one_night.play_one_night_werewolf()

#         assert result == example_small_game_result
