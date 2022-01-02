from tests.conftest import set_roles
from wolfbot import const
from wolfbot.enums import Role
from wolfbot.roles import Seer
from wolfbot.statements import Statement


class TestSeer:
    """Tests for the Seer player class."""

    @staticmethod
    def test_awake_init_center_choice(large_game_roles: tuple[Role, ...]) -> None:
        """
        Should initialize a Seer. Note that the player_index of the Seer is
        not necessarily the index where the true Seer is located.
        """
        player_index = 11
        const.CENTER_SEER_PROB = 1
        game_roles = list(large_game_roles)
        expected = (
            Statement(
                (
                    "I am a Seer and I saw that Center 1 was a Insomniac "
                    "and that Center 0 was a Troublemaker."
                ),
                (
                    (11, frozenset({Role.SEER})),
                    (13, frozenset({Role.INSOMNIAC})),
                    (12, frozenset({Role.TROUBLEMAKER})),
                ),
            ),
        )

        seer = Seer.awake_init(player_index, game_roles)

        assert seer.choice_1 == (13, Role.INSOMNIAC)
        assert seer.choice_2 == (12, Role.TROUBLEMAKER)
        assert seer.statements == expected

    @staticmethod
    def test_awake_init_player_choice(large_game_roles: tuple[Role, ...]) -> None:
        """
        Should initialize a Seer. Note that the player_index of the Seer is
        not necessarily the index where the true Seer is located.
        """
        player_index = 11
        const.CENTER_SEER_PROB = 0
        game_roles = list(large_game_roles)
        expected = (
            Statement(
                "I am a Seer and I saw that Player 6 was a Mason.",
                ((11, frozenset({Role.SEER})), (6, frozenset({Role.MASON}))),
            ),
        )

        seer = Seer.awake_init(player_index, game_roles)

        assert seer.choice_1 == (6, Role.MASON)
        assert seer.choice_2 == (None, None)
        assert seer.statements == expected

    @staticmethod
    def test_get_seer_statements() -> None:
        """Execute initialization actions and return the possible statements."""
        player_index = 1

        result = Seer.get_seer_statements(player_index, (6, Role.ROBBER))

        assert result == (
            Statement(
                "I am a Seer and I saw that Player 6 was a Robber.",
                ((1, frozenset({Role.SEER})), (6, frozenset({Role.ROBBER}))),
            ),
        )

    @staticmethod
    def test_get_all_statements() -> None:
        """Should return possible statements from all possible initializations."""
        player_index = 1
        set_roles(Role.WOLF, Role.SEER, Role.VILLAGER, Role.WOLF)
        const.NUM_PLAYERS = 2
        const.NUM_CENTER = 2
        expected = (
            Statement(
                "I am a Seer and I saw that Player 0 was a Villager.",
                ((1, frozenset({Role.SEER})), (0, frozenset({Role.VILLAGER}))),
            ),
            Statement(
                "I am a Seer and I saw that Player 1 was a Villager.",
                ((1, frozenset({Role.SEER})), (1, frozenset({Role.VILLAGER}))),
            ),
            Statement(
                "I am a Seer and I saw that Player 0 was a Wolf.",
                ((1, frozenset({Role.SEER})), (0, frozenset({Role.WOLF}))),
            ),
            Statement(
                "I am a Seer and I saw that Player 1 was a Wolf.",
                ((1, frozenset({Role.SEER})), (1, frozenset({Role.WOLF}))),
            ),
            Statement(
                "I am a Seer and I saw that Player 0 was a Seer.",
                ((1, frozenset({Role.SEER})), (0, frozenset({Role.SEER}))),
            ),
            Statement(
                "I am a Seer and I saw that Player 1 was a Seer.",
                ((1, frozenset({Role.SEER})), (1, frozenset({Role.SEER}))),
            ),
            Statement(
                (
                    "I am a Seer and I saw that Center 0 was a Villager and "
                    "that Center 1 was a Wolf."
                ),
                (
                    (1, frozenset({Role.SEER})),
                    (2, frozenset({Role.VILLAGER})),
                    (3, frozenset({Role.WOLF})),
                ),
            ),
            Statement(
                (
                    "I am a Seer and I saw that Center 0 was a Wolf and "
                    "that Center 1 was a Villager."
                ),
                (
                    (1, frozenset({Role.SEER})),
                    (2, frozenset({Role.WOLF})),
                    (3, frozenset({Role.VILLAGER})),
                ),
            ),
            Statement(
                (
                    "I am a Seer and I saw that Center 0 was a Wolf "
                    "and that Center 1 was a Wolf."
                ),
                (
                    (1, frozenset({Role.SEER})),
                    (2, frozenset({Role.WOLF})),
                    (3, frozenset({Role.WOLF})),
                ),
            ),
        )

        result = Seer.get_all_statements(player_index)

        assert set(result) == set(expected)
