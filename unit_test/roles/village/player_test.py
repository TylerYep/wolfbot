''' player_test.py '''
from src.statements import Statement
from src.roles import Player
from src.roles.village import Robber, Villager

class TestPlayer:
    ''' Tests for the Player class. '''

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
        assert robber.is_user is False

    @staticmethod
    def test_get_statement_inheritance():
        ''' Classes extending Player should contain a get_statement method. '''
        villager = Villager(0)

        statement = villager.get_statement([], [])

        assert statement == Statement('I am a Villager.', [(0, {'Villager'})])

    @staticmethod
    def test_json_repr():
        ''' Should convert a Player into a dict with all of its fields. '''
        villager = Villager(0)

        result = villager.json_repr()

        assert result == {'type': 'Villager', 'player_index': 0}

    @staticmethod
    def test_repr():
        ''' Should convert a Player into a representative string. '''
        villager = Villager(3)

        result = str(villager)

        assert result == 'Villager(3)'
