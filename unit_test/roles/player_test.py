""" player_test.py """
import pytest

from wolfbot import const
from wolfbot.const import Role
from wolfbot.roles import Drunk, Hunter, Minion, Player, Robber, Seer, Villager, Wolf
from wolfbot.statements import KnowledgeBase, Statement


class TestPlayer:
    """Tests for the Player class."""

    @staticmethod
    def test_constructor() -> None:
        """Should initialize a Player."""
        player_index = 5

        empty_player = Player(player_index)

        assert empty_player.role is Role.NONE
        assert empty_player.statements == ()

    @staticmethod
    def test_inheritance() -> None:
        """Classes extending Player should be able to access Player fields."""
        robber = Robber(2, 3, Role.VILLAGER)

        assert robber.choice_ind == 3
        assert robber.new_role is Role.VILLAGER

    @staticmethod
    def test_get_statement_inheritance() -> None:
        """Classes extending Player should contain a get_statement method."""
        villager = Villager(0)
        knowledge_base = KnowledgeBase()

        statement = villager.get_statement(knowledge_base)

        assert statement == Statement(
            "I am a Villager.", ((0, frozenset({Role.VILLAGER})),)
        )

    @staticmethod
    def test_json_repr() -> None:
        """Should convert a Player into a dict with all of its fields."""
        villager = Villager(0)

        result = villager.json_repr()

        assert result == {"type": "Villager", "player_index": 0}

    @staticmethod
    def test_repr() -> None:
        """Should convert a Player into a representative string."""
        villager = Villager(3)

        result = str(villager)

        assert result == "Villager(3)"

    @staticmethod
    def test_eq() -> None:
        """Should convert a Player into a representative string."""
        villager = Villager(3)
        hunter = Hunter(3)
        drunk_1 = Drunk(4, 5)
        drunk_2 = Drunk(4, 5)
        drunk_3 = Drunk(4, 7)

        assert villager != hunter
        assert drunk_1 == drunk_2
        assert drunk_1 != drunk_3


class TestIsEvil:
    """Tests for the is_evil function."""

    @staticmethod
    def test_no_evil_player(small_game_roles: tuple[str, ...]) -> None:
        """Should determine if a player has turned evil after night falls."""
        villager = Villager(0)

        result = villager.is_evil()

        assert result is False

    @staticmethod
    def test_find_evil_players(medium_game_roles: tuple[str, ...]) -> None:
        """Should determine if a player has turned evil after night falls."""
        player_list: tuple[Player, ...] = (
            Seer(0, (2, Role.DRUNK)),
            Wolf(1, (1,), 5, Role.TROUBLEMAKER),
            Drunk(2, 5),
            Robber(3, 2, Role.DRUNK),
            Minion(4, (1,)),
        )

        result = [player.is_evil() for player in player_list]

        assert result == [False, True, False, False, True]

    @staticmethod
    def test_turned_evil_player(medium_game_roles: tuple[str, ...]) -> None:
        """Should determine if a player has turned evil after night falls."""
        robber = Robber(3, 1, Role.WOLF)

        result = robber.is_evil()

        assert result is True


class TestGetVote:
    """
    Tests for the vote function.
    IMPORTANT: As written, the voter's role does not matter in their decision.
    If it becomes important, then use the player_list from test_find_evil_players.
    """

    @staticmethod
    def test_vote_for_wolf(medium_game_roles: tuple[str, ...]) -> None:
        """If a player suspects a Wolf, they should vote for that player."""
        prediction = (
            Role.SEER,
            Role.WOLF,
            Role.TROUBLEMAKER,
            Role.DRUNK,
            Role.MINION,
            Role.ROBBER,
        )

        result = Player(2).vote(prediction)

        assert result == 1

    @staticmethod
    def test_no_vote_for_center_wolf(medium_game_roles: tuple[str, ...]) -> None:
        """
        If a player suspects a Wolf in the center, they should not vote for that player.
        """
        prediction = (
            Role.SEER,
            Role.TROUBLEMAKER,
            Role.DRUNK,
            Role.MINION,
            Role.ROBBER,
            Role.WOLF,
        )

        result = Player(2).vote(prediction)

        assert result == 3

    @staticmethod
    def test_vote_right(small_game_roles: tuple[str, ...]) -> None:
        """
        If no Wolves are found, players should vote for the person to their right.
        """
        prediction = (Role.VILLAGER, Role.SEER, Role.ROBBER)

        result = [Player(i).vote(prediction) for i in range(const.NUM_PLAYERS)]

        assert result == [1, 2, 0]

    @staticmethod
    def test_interactive_vote(
        monkeypatch: pytest.MonkeyPatch, medium_game_roles: tuple[str, ...]
    ) -> None:
        """Prompt the user for their vote."""
        player_index = 2
        const.IS_USER[player_index] = True
        prediction = (
            Role.SEER,
            Role.TROUBLEMAKER,
            Role.DRUNK,
            Role.MINION,
            Role.ROBBER,
            Role.WOLF,
        )
        monkeypatch.setattr("builtins.input", lambda x: "4")

        result = Player(player_index).vote(prediction)

        assert result == 4
