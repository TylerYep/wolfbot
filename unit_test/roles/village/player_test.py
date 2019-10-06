''' player_test.py '''
from src.statements import Statement
from src.roles.village import Player, Robber, Villager

class TestPlayer:
    @staticmethod
    def test_constructor():
        ''' Should initialize a Player. '''
        player_index = 5

        empty_player = Player(player_index)

        assert empty_player.role == 'Player'
        assert empty_player.statements == []

    @staticmethod
    def test_inheritance():
        ''' Classes extending Player should be able to access Player fields. '''
        robber = Robber(2, 3, 'Villager')

        assert robber.choice_ind == 3
        assert robber.new_role == 'Villager'
        assert not robber.is_user

    @staticmethod
    def test_get_statement_inheritance():
        ''' Classes extending Player should contain a get_statement method. '''
        villager = Villager(0)

        statement = villager.get_statement([], [])

        assert statement == Statement('I am a Villager.', [(0, {'Villager'})])

    @staticmethod
    def test_json_repr():
        ''' Should convert a Player into a dict with all of its fields. '''
        pass

    @staticmethod
    def test_repr():
        ''' Should convert a Player into a representative string. '''
        pass
