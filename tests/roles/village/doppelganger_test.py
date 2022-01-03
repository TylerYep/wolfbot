from tests.conftest import set_roles
from wolfbot import const
from wolfbot.enums import Role
from wolfbot.roles import Doppelganger
from wolfbot.statements import Statement


class TestDoppelganger:
    """Tests for the Doppelganger player class."""

    @staticmethod
    def test_awake_init(large_game_roles: tuple[Role, ...]) -> None:
        """
        Initialize a Doppelganger. Note that the player_index of the Doppelganger
        is not necessarily the index where the true Doppelganger is located.
        """
        player_index = 6
        game_roles = list(large_game_roles)
        game_roles[5] = Role.DOPPELGANGER

        doppelganger = Doppelganger.awake_init(player_index, game_roles)

        assert doppelganger.statements == (
            Statement(
                "I am a Doppelganger and when I woke up I was a Wolf.",
                ((6, frozenset({Role.DOPPELGANGER})),),
            ),
        )

    @staticmethod
    def test_get_doppelganger_statements() -> None:
        """Execute initialization actions and return the possible statements."""
        player_index = 4

        result = Doppelganger.get_doppelganger_statements(player_index, Role.ROBBER)

        assert result == (
            Statement(
                "I am a Doppelganger and when I woke up I was a Robber.",
                ((4, frozenset({Role.DOPPELGANGER})),),
            ),
        )

    @staticmethod
    def test_get_all_statements() -> None:
        """Should return possible statements from all possible initializations."""
        player_index = 2
        set_roles(
            Role.WOLF, Role.SEER, Role.DRUNK, Role.VILLAGER, Role.ROBBER, Role.WOLF
        )
        const.NUM_PLAYERS = 3
        const.NUM_CENTER = 3
        expected_statements = (
            Statement(
                "I am a Doppelganger and when I woke up I was a Drunk.",
                ((2, frozenset({Role.DOPPELGANGER})),),
            ),
            Statement(
                "I am a Doppelganger and when I woke up I was a Robber.",
                ((2, frozenset({Role.DOPPELGANGER})),),
            ),
            Statement(
                "I am a Doppelganger and when I woke up I was a Seer.",
                ((2, frozenset({Role.DOPPELGANGER})),),
            ),
            Statement(
                "I am a Doppelganger and when I woke up I was a Villager.",
                ((2, frozenset({Role.DOPPELGANGER})),),
            ),
            Statement(
                "I am a Doppelganger and when I woke up I was a Wolf.",
                ((2, frozenset({Role.DOPPELGANGER})),),
            ),
        )

        result = Doppelganger.get_all_statements(player_index)

        assert result == expected_statements
