''' util_test.py '''
import pytest

from src import util, const

class TestSwapCharacters:
    def test_same_index_error(self, small_game_roles):
        ''' Don't attempt to swap the same index. '''
        roles = list(small_game_roles)

        with pytest.raises(AssertionError):
            util.swap_characters(roles, 2, 2)

    def test_swap(self, small_game_roles):
        ''' Correctly swap two players. '''
        roles = list(small_game_roles)

        util.swap_characters(roles, 0, 2)

        assert roles == ['Robber', 'Seer', 'Villager']


class TestFindAllPlayerIndices:
    def test_returns_correct_indices(self, large_game_roles):
        ''' Don't attempt to swap the same index. '''
        roles = list(large_game_roles)

        result = util.find_all_player_indices(roles, 'Villager')

        assert result == [1, 4, 11]


class TestGetPlayer:
    pass


class TestGetCenter:
    pass


class TestGetRandomPlayer:
    def test_generates_different_indices(self, large_game_roles):
        ''' Generated indices should be random. '''
        const.ROLES = large_game_roles

        result = [util.get_random_player() for _ in range(10)]

        assert result == [6, 6, 0, 4, 8, 7, 6, 4, 7, 5]

    def test_excludes_specified_values(self, large_game_roles):
        ''' Generated indices should exclude specified values. '''
        const.ROLES = large_game_roles
        exclude = (6, 7, 8)

        result = [util.get_random_player(exclude) for _ in range(10)]

        assert not set(result).intersection(exclude)
        assert result == [0, 4, 4, 5, 9, 3, 2, 4, 2, 1]


class TestGetRandomCenter:
    def test_generates_different_indices(self, large_game_roles):
        ''' Generated indices should be random. '''
        const.ROLES = large_game_roles

        result = [util.get_random_center() for _ in range(10)]

        assert result == [13, 13, 12, 13, 14, 13, 13, 13, 13, 13]

    def test_excludes_specified_values(self, large_game_roles):
        ''' Generated indices should exclude specified values. '''
        const.ROLES = large_game_roles
        exclude = (12, 13)

        result = [util.get_random_center(exclude) for _ in range(10)]

        assert not set(result).intersection(exclude)
        assert result == [14]*10


class TestInputPlayer:
    pass


class TestInputCenter:
    pass


class TestGetNumericInput:
    pass


class TestPrintRoles:
    def test_print_roles(self, caplog, small_game_roles):
        ''' Correctly print and format roles. '''
        const.ROLES = small_game_roles
        shuffled_roles = ['Seer', 'Villager', 'Wolf', 'Robber']

        util.print_roles(shuffled_roles)

        captured = caplog.records[0].getMessage()
        expected = '[Hidden] Current roles: [Seer, Villager, Wolf]\n' + \
                   '          Center cards: [Robber]\n'
        assert captured == expected
