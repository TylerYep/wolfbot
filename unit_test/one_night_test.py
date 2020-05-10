""" one_night_test.py """
from conftest import verify_output
from src import const, one_night


class TestPlayOneNightWerewolf:
    """ Tests for the play_one_night_werewolf function. """

    @staticmethod
    def test_one_night_small(caplog, example_small_game_result):
        """ Correctly play one round of one night werewolf. """
        result = one_night.play_one_night_werewolf()

        assert result == example_small_game_result
        verify_output(caplog, "unit_test/test_data/one_night_small.out")

    @staticmethod
    def test_one_night_medium(caplog, example_medium_game_result):
        """ Correctly play one round of one night werewolf. """
        result = one_night.play_one_night_werewolf()

        assert result == example_medium_game_result
        verify_output(caplog, "unit_test/test_data/one_night_medium.out")

    @staticmethod
    def test_one_night_large(caplog, example_large_game_result):
        """ Correctly play one round of one night werewolf. """
        result = one_night.play_one_night_werewolf()

        assert result == example_large_game_result
        verify_output(caplog, "unit_test/test_data/one_night_large.out")


# class TestPlayOneNightWerewolfInteractive:
#     """ Tests for the play_one_night_werewolf function. """

#     @staticmethod
#     def test_one_night_small(caplog, monkeypatch, example_small_game_result):
#         """ Correctly play one round of one night werewolf. """
#         const.INTERACTIVE_MODE_ON = True
#         monkeypatch.setattr('builtins.input', lambda x: "1")

#         result = one_night.play_one_night_werewolf()

#         assert result == example_small_game_result
#         verify_output(caplog, "unit_test/test_data/one_night_small.out")


class TestPrintRoles:
    """ Tests for the print_roles function. """

    @staticmethod
    def test_print_roles(caplog, small_game_roles):
        """ Correctly print and format roles. """
        const.ROLES = small_game_roles
        shuffled_roles = ["Seer", "Villager", "Wolf", "Robber"]

        one_night.print_roles(shuffled_roles, "Hidden")

        captured = caplog.records[0].getMessage()
        expected = (
            f"[Hidden] Current roles: [Seer, Villager, Wolf]\n{' ' * 10}Center cards: [Robber]\n"
        )
        assert captured == expected
