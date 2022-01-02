from tests.conftest import set_roles
from wolfbot import const
from wolfbot.enums import Role, SwitchPriority
from wolfbot.game_utils import GameRoles
from wolfbot.roles import Troublemaker
from wolfbot.statements import Statement


class TestTroublemaker:
    """Tests for the Troublemaker player class."""

    @staticmethod
    def test_awake_init(large_game_roles: tuple[Role, ...]) -> None:
        """
        Should initialize a Troublemaker. Note that the player_index of the
        Troublemaker is not necessarily the index where the
        true Troublemaker is located.
        """
        player_index = 11
        game_roles = list(large_game_roles)
        expected = (
            Statement(
                "I am a Troublemaker and I swapped Player 6 and Player 7.",
                ((11, frozenset({Role.TROUBLEMAKER})),),
                ((SwitchPriority.TROUBLEMAKER, 6, 7),),
                Role.TROUBLEMAKER,
            ),
        )
        new_roles = list(large_game_roles)
        new_roles[6], new_roles[7] = new_roles[7], new_roles[6]

        tmkr = Troublemaker.awake_init(player_index, GameRoles(game_roles))

        assert tmkr.choice_ind1 == 6
        assert tmkr.choice_ind2 == 7
        assert game_roles == new_roles
        assert tmkr.statements == expected

    @staticmethod
    def test_get_troublemaker_statements() -> None:
        """Execute initialization actions and return the possible statements."""
        player_index = 1

        result = Troublemaker.get_troublemaker_statements(player_index, 6, 3)

        assert result == (
            Statement(
                "I am a Troublemaker and I swapped Player 6 and Player 3.",
                ((1, frozenset({Role.TROUBLEMAKER})),),
                ((SwitchPriority.TROUBLEMAKER, 6, 3),),
                Role.TROUBLEMAKER,
            ),
        )

    @staticmethod
    def test_get_all_statements() -> None:
        """Should return possible statements from all possible initializations."""
        player_index = 2
        set_roles(
            Role.WOLF,
            Role.SEER,
            Role.TROUBLEMAKER,
            Role.VILLAGER,
            Role.ROBBER,
            Role.WOLF,
        )
        const.NUM_PLAYERS = 3
        const.NUM_CENTER = 3
        expected_statements = (
            Statement(
                "I am a Troublemaker and I swapped Player 0 and Player 1.",
                ((2, frozenset({Role.TROUBLEMAKER})),),
                ((SwitchPriority.TROUBLEMAKER, 0, 1),),
                Role.TROUBLEMAKER,
            ),
        )

        result = Troublemaker.get_all_statements(player_index)

        assert result == expected_statements
