""" util_test.py """
import pytest

from conftest import override_input
from src import const, util


class TestSwapCharacters:
    """ Tests for the swap_characters function. """

    @staticmethod
    def test_same_index_error(small_game_roles):
        """ Don't attempt to swap the same index. """
        roles = list(small_game_roles)

        with pytest.raises(AssertionError):
            util.swap_characters(roles, 2, 2)

    @staticmethod
    def test_swap(small_game_roles):
        """ Correctly swap two players. """
        roles = list(small_game_roles)

        util.swap_characters(roles, 0, 2)

        assert roles == ["Robber", "Seer", "Villager"]


class TestFindAllPlayerIndices:
    """ Tests for the find_all_player_indices function. """

    @staticmethod
    def test_returns_correct_indices(large_game_roles):
        """ Don't attempt to swap the same index. """
        roles = list(large_game_roles)

        result = util.find_all_player_indices(roles, "Villager")

        assert result == [1, 4, 11]


class TestGetPlayer:
    """ Tests for the get_player function. """

    @staticmethod
    def test_generates_random_indices(large_game_roles):
        """ Generated indices should be random. """
        const.ROLES = large_game_roles

        result = [util.get_player(is_user=False) for _ in range(10)]

        assert result == [6, 6, 0, 4, 8, 7, 6, 4, 7, 5]

    @staticmethod
    def test_random_excludes_values(large_game_roles):
        """ Generated indices should exclude specified values. """
        const.ROLES = large_game_roles
        exclude = (6, 7, 8)

        result = [util.get_player(is_user=False, vals_to_exclude=exclude) for _ in range(10)]

        assert not set(result).intersection(exclude)
        assert result == [0, 4, 4, 5, 9, 3, 2, 4, 2, 1]

    @staticmethod
    def test_user_input_indices(monkeypatch, large_game_roles):
        """ Generated indices should be random. """
        const.ROLES = large_game_roles
        inputs = [0, 2, 20, 1]
        monkeypatch.setattr("builtins.input", override_input(inputs))

        result = [util.get_player(is_user=True) for _ in range(3)]

        assert result == [0, 2, 1]

    @staticmethod
    def test_user_excludes_values(monkeypatch, large_game_roles):
        """ Generated indices should exclude specified values. """
        const.ROLES = large_game_roles
        exclude = (6, 7, 8)
        inputs = [0, 20, 4, 7, 5, 6]
        monkeypatch.setattr("builtins.input", override_input(inputs))

        result = [util.get_player(is_user=True, vals_to_exclude=exclude) for _ in range(3)]

        assert not set(result).intersection(exclude)
        assert result == [0, 4, 5]


class TestGetCenter:
    """ Tests for the get_center function. """

    @staticmethod
    def test_generates_random_indices(large_game_roles):
        """ Generated indices should be random. """
        const.ROLES = large_game_roles

        result = [util.get_center(is_user=False) for _ in range(10)]

        assert result == [13, 13, 12, 13, 14, 13, 13, 13, 13, 13]

    @staticmethod
    def test_excludes_values(large_game_roles):
        """ Generated indices should exclude specified values. """
        const.ROLES = large_game_roles
        exclude = (12, 13)

        result = [util.get_center(is_user=False, vals_to_exclude=exclude) for _ in range(10)]

        assert not set(result).intersection(exclude)
        assert result == [14] * 10

    @staticmethod
    def test_user_center_indices(monkeypatch, large_game_roles):
        """ Generated indices should be random. """
        const.ROLES = large_game_roles
        inputs = [1, 2, 0, 2]
        monkeypatch.setattr("builtins.input", override_input(inputs))

        result = [util.get_center(is_user=True) for _ in range(3)]

        assert result == [13, 14, 12]

    @staticmethod
    def test_user_excludes_values(monkeypatch, large_game_roles):
        """ Generated indices should exclude specified values. """
        const.ROLES = large_game_roles
        exclude = (12, 13)
        inputs = [2, 0, 4, 1, 2, 2]
        monkeypatch.setattr("builtins.input", override_input(inputs))

        result = [util.get_center(is_user=True, vals_to_exclude=exclude) for _ in range(3)]

        assert not set(result).intersection(exclude)
        assert result == [14] * 3


class TestGetNumericInput:
    """ Tests for the get_numeric_input function. """

    @staticmethod
    def test_numeric_input(monkeypatch):
        """ Generated indices should be random. """
        inputs = [1, 7, 10, 15, 2, 0]
        monkeypatch.setattr("builtins.input", override_input(inputs))

        result = [util.get_numeric_input(10) for _ in range(4)]

        assert result == [1, 7, 2, 0]

    @staticmethod
    def test_numeric_input_range(monkeypatch):
        """ Generated indices should be random. """
        inputs = [1, 37, 30, 34, 0, 33]
        monkeypatch.setattr("builtins.input", override_input(inputs))

        result = [util.get_numeric_input(30, 34) for _ in range(2)]

        assert result == [30, 33]
