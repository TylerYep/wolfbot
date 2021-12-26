from tests.conftest import set_roles
from wolfbot import const
from wolfbot.enums import Role, SwitchPriority
from wolfbot.roles import Drunk
from wolfbot.statements import Statement


class TestDrunk:
    """Tests for the Drunk player class."""

    @staticmethod
    def test_awake_init(large_game_roles: tuple[Role, ...]) -> None:
        """
        Should initialize a Drunk. Note that the player_index of the Drunk
        is not necessarily the index where the true Drunk is located.
        """
        player_index = 6
        game_roles = list(large_game_roles)
        new_roles = list(large_game_roles)
        new_roles[13], new_roles[6] = new_roles[6], new_roles[13]

        drunk = Drunk.awake_init(player_index, game_roles, large_game_roles)

        assert drunk.choice_ind == 13
        assert game_roles == new_roles
        assert drunk.statements == (
            Statement(
                "I am a Drunk and I swapped with Center 1.",
                ((6, frozenset({Role.DRUNK})),),
                ((SwitchPriority.DRUNK, 6, 13),),
                Role.DRUNK,
            ),
        )

    @staticmethod
    def test_get_drunk_statements() -> None:
        """Execute initialization actions and return the possible statements."""
        player_index = 4

        result = Drunk.get_drunk_statements(player_index, 12)

        assert result == (
            Statement(
                "I am a Drunk and I swapped with Center 0.",
                ((4, frozenset({Role.DRUNK})),),
                ((SwitchPriority.DRUNK, 4, 12),),
                Role.DRUNK,
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
                "I am a Drunk and I swapped with Center 0.",
                ((2, frozenset({Role.DRUNK})),),
                ((SwitchPriority.DRUNK, 2, 3),),
                Role.DRUNK,
            ),
            Statement(
                "I am a Drunk and I swapped with Center 1.",
                ((2, frozenset({Role.DRUNK})),),
                ((SwitchPriority.DRUNK, 2, 4),),
                Role.DRUNK,
            ),
            Statement(
                "I am a Drunk and I swapped with Center 2.",
                ((2, frozenset({Role.DRUNK})),),
                ((SwitchPriority.DRUNK, 2, 5),),
                Role.DRUNK,
            ),
        )

        result = Drunk.get_all_statements(player_index)

        assert result == expected_statements
