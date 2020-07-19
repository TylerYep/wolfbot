""" hunter_test.py """
from src.roles.village import Hunter
from src.statements import Statement


class TestHunter:
    """ Tests for the Hunter player class. """

    @staticmethod
    def test_awake_init():
        """ Should initialize a Hunter. """
        player_index = 5

        hunter = Hunter.awake_init(player_index, [], [])  # Other params are unused.

        assert hunter.statements == (Statement("I am a Hunter.", ((5, frozenset({"Hunter"})),)),)

    @staticmethod
    def test_get_hunter_statements():
        """ Should execute initialization actions and return the possible statements. """
        player_index = 0

        result = Hunter.get_hunter_statements(player_index)

        assert result == (Statement("I am a Hunter.", ((0, frozenset({"Hunter"})),)),)

    @staticmethod
    def test_get_all_statements():
        """ Should return the possible statements from all possible initialization actions. """
        player_index = 2

        result = Hunter.get_all_statements(player_index)

        assert result == (Statement("I am a Hunter.", ((2, frozenset({"Hunter"})),)),)
