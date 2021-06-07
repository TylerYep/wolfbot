""" mason_test.py """
from conftest import set_roles
from wolfbot import const
from wolfbot.const import Role
from wolfbot.roles import Mason
from wolfbot.statements import Statement


class TestMason:
    """Tests for the Mason player class."""

    @staticmethod
    def test_awake_init(large_game_roles: tuple[Role, ...]) -> None:
        """Should initialize a Mason."""
        player_index = 6

        mason = Mason.awake_init(player_index, [], large_game_roles)

        assert mason.mason_indices == (6, 9)
        assert mason.statements == (
            Statement(
                "I am a Mason. The other Mason is Player 9.",
                ((6, frozenset({Role.MASON})), (9, frozenset({Role.MASON}))),
            ),
        )

    @staticmethod
    def test_get_mason_statements() -> None:
        """Execute initialization actions and return the possible statements."""
        player_index = 9

        result = Mason.get_mason_statements(player_index, (6, 9))

        assert result == (
            Statement(
                "I am a Mason. The other Mason is Player 6.",
                ((9, frozenset({Role.MASON})), (6, frozenset({Role.MASON}))),
            ),
        )

    @staticmethod
    def test_get_single_mason_statement() -> None:
        """Should give the proper statement when only one Mason is present."""
        player_index = 2
        set_roles(Role.WOLF, Role.SEER, Role.MASON, Role.VILLAGER)
        const.NUM_PLAYERS = 3
        result = Mason.get_mason_statements(player_index, (2,))

        assert result == (
            Statement(
                "I am a Mason. The other Mason is not present.",
                (
                    (2, frozenset({Role.MASON})),
                    (0, frozenset({Role.WOLF, Role.SEER, Role.VILLAGER})),
                    (1, frozenset({Role.WOLF, Role.SEER, Role.VILLAGER})),
                ),
            ),
        )

    @staticmethod
    def test_get_all_statements() -> None:
        """Should return possible statements from all possible initializations."""
        player_index = 2
        set_roles(Role.WOLF, Role.SEER, Role.MASON, Role.VILLAGER)
        const.NUM_PLAYERS = 3
        expected_statements = (
            Statement(
                "I am a Mason. The other Mason is not present.",
                (
                    (2, frozenset({Role.MASON})),
                    (0, frozenset({Role.WOLF, Role.SEER, Role.VILLAGER})),
                    (1, frozenset({Role.WOLF, Role.SEER, Role.VILLAGER})),
                ),
            ),
            Statement(
                "I am a Mason. The other Mason is Player 0.",
                ((2, frozenset({Role.MASON})), (0, frozenset({Role.MASON}))),
            ),
            Statement(
                "I am a Mason. The other Mason is Player 1.",
                ((2, frozenset({Role.MASON})), (1, frozenset({Role.MASON}))),
            ),
        )

        result = Mason.get_all_statements(player_index)

        assert result == expected_statements
