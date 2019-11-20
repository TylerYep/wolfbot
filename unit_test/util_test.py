''' util_test.py '''
import pytest

from src import util, const

class TestSwapCharacters:
    ''' Tests for the swap_characters function. '''

    @staticmethod
    def test_same_index_error(small_game_roles):
        ''' Don't attempt to swap the same index. '''
        roles = list(small_game_roles)

        with pytest.raises(AssertionError):
            util.swap_characters(roles, 2, 2)

    @staticmethod
    def test_swap(small_game_roles):
        ''' Correctly swap two players. '''
        roles = list(small_game_roles)

        util.swap_characters(roles, 0, 2)

        assert roles == ['Robber', 'Seer', 'Villager']


class TestFindAllPlayerIndices:
    ''' Tests for the find_all_player_indices function. '''

    @staticmethod
    def test_returns_correct_indices(large_game_roles):
        ''' Don't attempt to swap the same index. '''
        roles = list(large_game_roles)

        result = util.find_all_player_indices(roles, 'Villager')

        assert result == [1, 4, 11]


class TestGetPlayer:
    ''' Tests for the get_player function. '''

    pass


class TestGetCenter:
    ''' Tests for the get_center function. '''

    pass


class TestGetRandomPlayer:
    ''' Tests for the get_random_player function. '''

    @staticmethod
    def test_generates_different_indices(large_game_roles):
        ''' Generated indices should be random. '''
        const.ROLES = large_game_roles

        result = [util.get_random_player() for _ in range(10)]

        assert result == [6, 6, 0, 4, 8, 7, 6, 4, 7, 5]

    @staticmethod
    def test_excludes_specified_values(large_game_roles):
        ''' Generated indices should exclude specified values. '''
        const.ROLES = large_game_roles
        exclude = (6, 7, 8)

        result = [util.get_random_player(exclude) for _ in range(10)]

        assert not set(result).intersection(exclude)
        assert result == [0, 4, 4, 5, 9, 3, 2, 4, 2, 1]


class TestGetRandomCenter:
    ''' Tests for the get_random_center function. '''

    @staticmethod
    def test_generates_different_indices(large_game_roles):
        ''' Generated indices should be random. '''
        const.ROLES = large_game_roles

        result = [util.get_random_center() for _ in range(10)]

        assert result == [13, 13, 12, 13, 14, 13, 13, 13, 13, 13]

    @staticmethod
    def test_excludes_specified_values(large_game_roles):
        ''' Generated indices should exclude specified values. '''
        const.ROLES = large_game_roles
        exclude = (12, 13)

        result = [util.get_random_center(exclude) for _ in range(10)]

        assert not set(result).intersection(exclude)
        assert result == [14]*10


class TestInputPlayer:
    ''' Tests for the input_player function. '''

    pass


class TestInputCenter:
    ''' Tests for the input_center function. '''

    pass


class TestGetNumericInput:
    ''' Tests for the get_numeric_input function. '''

    pass
