''' wolf_test.py '''
from src import const
from src.roles import Wolf

class TestWolf:
    ''' Tests for the Wolf player class. '''
    @staticmethod
    def test_awake_init_medium(medium_game_roles):
        '''
        Should initialize a Wolf. Note that the player_index of the Wolf is
        not necessarily the index where the true Wolf is located.
        '''
        const.ROLES = ('Wolf', *medium_game_roles[1:])
        player_index = 2

        wolf = Wolf.awake_init(player_index, const.ROLES, const.ROLES)
        assert wolf.wolf_indices == [0, 2]
        assert wolf.center_index is None
        assert wolf.center_role is None

    @staticmethod
    def test_awake_init_large(large_game_roles):
        '''
        Should initialize a Wolf. Note that the player_index of the Wolf is
        not necessarily the index where the true Wolf is located.
        '''
        const.ROLES = large_game_roles
        player_index = 7

        wolf = Wolf.awake_init(player_index, const.ROLES, const.ROLES)

        assert wolf.wolf_indices == [0, 7]
        assert wolf.center_index is None
        assert wolf.center_role is None

    @staticmethod
    def test_awake_init_center(large_game_roles):
        '''
        Should initialize a Center Wolf. Note that the player_index of the Wolf is
        not necessarily the index where the true Wolf is located.
        '''
        const.ROLES = ('Villager', *large_game_roles[1:])
        player_index = 7

        wolf = Wolf.awake_init(player_index, const.ROLES, const.ROLES)

        assert wolf.wolf_indices == [7]
        assert wolf.center_index == 13
        assert wolf.center_role == 'Insomniac'

    @staticmethod
    def test_get_wolf_statement():
        ''' Should execute initialization actions and return the possible statements. '''
        pass

    @staticmethod
    def test_eval_fn():
        ''' Should return the value from the chosen statement action. '''
        pass
