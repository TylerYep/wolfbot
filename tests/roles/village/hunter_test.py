from wolfbot.enums import Role
from wolfbot.game_utils import GameRoles
from wolfbot.roles import Hunter
from wolfbot.statements import Statement


class TestHunter:
    """Tests for the Hunter player class."""

    @staticmethod
    def test_awake_init() -> None:
        """Should initialize a Hunter."""
        player_index = 5

        hunter = Hunter.awake_init(player_index, GameRoles([]))  # unused

        assert hunter.statements == (
            Statement("I am a Hunter.", ((5, frozenset({Role.HUNTER})),)),
        )

    @staticmethod
    def test_get_hunter_statements() -> None:
        """Execute initialization actions and return the possible statements."""
        player_index = 0

        result = Hunter.get_hunter_statements(player_index)

        assert result == (
            Statement("I am a Hunter.", ((0, frozenset({Role.HUNTER})),)),
        )

    @staticmethod
    def test_get_all_statements() -> None:
        """Should return possible statements from all possible initializations."""
        player_index = 2

        result = Hunter.get_all_statements(player_index)

        assert result == (
            Statement("I am a Hunter.", ((2, frozenset({Role.HUNTER})),)),
        )
