""" player_test.py """
from src import const
from src.roles import Drunk, Minion, Player, Robber, Seer, Villager, Wolf
from src.statements import Statement


class TestPlayer:
    """ Tests for the Player class. """

    @staticmethod
    def test_constructor():
        """ Should initialize a Player. """
        player_index = 5

        empty_player = Player(player_index)

        assert empty_player.role == "Player"
        assert empty_player.statements == []

    @staticmethod
    def test_inheritance():
        """ Classes extending Player should be able to access Player fields. """
        robber = Robber(2, 3, "Villager")

        assert robber.choice_ind == 3
        assert robber.new_role == "Villager"
        assert robber.is_user is False

    @staticmethod
    def test_get_statement_inheritance():
        """ Classes extending Player should contain a get_statement method. """
        villager = Villager(0)

        statement = villager.get_statement([], [])

        assert statement == Statement("I am a Villager.", ((0, frozenset({"Villager"})),))

    @staticmethod
    def test_json_repr():
        """ Should convert a Player into a dict with all of its fields. """
        villager = Villager(0)

        result = villager.json_repr()

        assert result == {"type": "Villager", "player_index": 0}

    @staticmethod
    def test_repr():
        """ Should convert a Player into a representative string. """
        villager = Villager(3)

        result = str(villager)

        assert result == "Villager(3)"


class TestIsEvil:
    """ Tests for the is_evil function. """

    @staticmethod
    def test_no_evil_player(small_game_roles):
        """ Should determine if a player has turned evil after night falls. """
        const.ROLES = small_game_roles
        villager = Villager(0)
        wolf_inds = []

        result = villager.is_evil(wolf_inds)

        assert result is False

    @staticmethod
    def test_find_evil_players(medium_game_roles):
        """ Should determine if a player has turned evil after night falls. """
        const.ROLES = medium_game_roles
        player_list = [
            Seer(0, (2, "Drunk")),
            Wolf(1, [1], 5, "Troublemaker"),
            Drunk(2, 5),
            Robber(3, 2, "Drunk"),
            Minion(4, [1]),
        ]
        wolf_inds = [1]

        result = [player.is_evil(wolf_inds) for player in player_list]

        assert result == [False, True, False, False, True]

    @staticmethod
    def test_turned_evil_player(medium_game_roles):
        """ Should determine if a player has turned evil after night falls. """
        const.ROLES = medium_game_roles
        robber = Robber(3, 1, "Wolf")
        wolf_inds = [1]

        result = robber.is_evil(wolf_inds)

        assert result is True
