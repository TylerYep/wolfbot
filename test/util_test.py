''' util_test.py '''
import pytest

from src import util, const
from fixtures import example_game_roles, large_game_roles

class TestSwapCharacters:
    def test_same_index_error(self, caplog):
        '''Don't attempt to swap the same index.'''
        roles = example_game_roles()

        with pytest.raises(AssertionError):
            util.swap_characters(roles, 2, 2)

    def test_swap(self):
        '''Correctly swap two players.'''
        roles = example_game_roles()

        util.swap_characters(roles, 0, 2)

        assert roles == ['Robber', 'Seer', 'Villager']


class TestFindAllPlayerIndices:
    def test_returns_correct_indices(self):
        '''Don't attempt to swap the same index.'''
        roles = large_game_roles()

        result = util.find_all_player_indices(roles, 'Villager')

        assert result == [1, 4, 11]


class TestGetPlayer:
    pass


class TestGetCenter:
    pass


class TestGetRandomPlayer:
    pass


class TestGetRandomCenter:
    pass


class TestInputPlayer:
    pass


class TestInputCenter:
    pass


class TestGetNumericInput:
    pass


class TestPrintRoles:
    def test_print_roles(self, caplog):
        '''Correctly print and format roles.'''
        const.ROLES = ('Robber', 'Villager', 'Wolf')
        const.NUM_PLAYERS = 2
        shuffled_roles = ['Villager', 'Wolf', 'Robber']

        util.print_roles(shuffled_roles)
        captured = caplog.records[0].getMessage()

        expected = '[Hidden] Current roles: [Villager, Wolf]' \
                    + ' '*17 \
                    + '\n\t  Center cards: [Robber]\n'
        assert captured == expected
