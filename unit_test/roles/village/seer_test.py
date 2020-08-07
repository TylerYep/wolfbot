""" seer_test.py """
from typing import Tuple

from conftest import set_roles
from src import const
from src.const import Role, RoleBits
from src.roles import Seer
from src.statements import Statement


class TestSeer:
    """ Tests for the Seer player class. """

    @staticmethod
    def test_awake_init_center_choice(large_game_roles: Tuple[Role, ...]) -> None:
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
                    (11, RoleBits.from_roles(Role.SEER)),
                    (13, RoleBits.from_roles(Role.INSOMNIAC)),
                    (12, RoleBits.from_roles(Role.TROUBLEMAKER)),
                ),
            ),
        )

        seer = Seer.awake_init(player_index, game_roles, ())

        assert seer.choice_1 == (13, Role.INSOMNIAC)
        assert seer.choice_2 == (12, Role.TROUBLEMAKER)
        assert seer.statements == expected

    @staticmethod
    def test_awake_init_player_choice(large_game_roles: Tuple[Role, ...]) -> None:
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
                ((11, RoleBits.from_roles(Role.SEER)), (6, RoleBits.from_roles(Role.MASON))),
            ),
        )

        seer = Seer.awake_init(player_index, game_roles, ())

        assert seer.choice_1 == (6, Role.MASON)
        assert seer.choice_2 == (None, None)
        assert seer.statements == expected

    @staticmethod
    def test_get_seer_statements() -> None:
        """ Should execute initialization actions and return the possible statements. """
        player_index = 1

        result = Seer.get_seer_statements(player_index, (6, Role.ROBBER))

        assert result == (
            Statement(
                "I am a Seer and I saw that Player 6 was a Robber.",
                ((1, RoleBits.from_roles(Role.SEER)), (6, RoleBits.from_roles(Role.ROBBER))),
            ),
        )

    @staticmethod
    def test_get_all_statements() -> None:
        """ Should return the possible statements from all possible initialization actions. """
        player_index = 1
        set_roles(Role.WOLF, Role.SEER, Role.VILLAGER, Role.WOLF)
        const.NUM_PLAYERS = 2
        const.NUM_CENTER = 2
        expected = (
            Statement(
                "I am a Seer and I saw that Player 0 was a Villager.",
                ((1, RoleBits.from_roles(Role.SEER)), (0, RoleBits.from_roles(Role.VILLAGER))),
            ),
            Statement(
                "I am a Seer and I saw that Player 1 was a Villager.",
                ((1, RoleBits.from_roles(Role.SEER)), (1, RoleBits.from_roles(Role.VILLAGER))),
            ),
            Statement(
                "I am a Seer and I saw that Player 0 was a Wolf.",
                ((1, RoleBits.from_roles(Role.SEER)), (0, RoleBits.from_roles(Role.WOLF))),
            ),
            Statement(
                "I am a Seer and I saw that Player 1 was a Wolf.",
                ((1, RoleBits.from_roles(Role.SEER)), (1, RoleBits.from_roles(Role.WOLF))),
            ),
            Statement(
                "I am a Seer and I saw that Player 0 was a Seer.",
                ((1, RoleBits.from_roles(Role.SEER)), (0, RoleBits.from_roles(Role.SEER))),
            ),
            Statement(
                "I am a Seer and I saw that Player 1 was a Seer.",
                ((1, RoleBits.from_roles(Role.SEER)), (1, RoleBits.from_roles(Role.SEER))),
            ),
            Statement(
                (
                    "I am a Seer and I saw that Center 0 was a Villager and "
                    "that Center 1 was a Wolf."
                ),
                (
                    (1, RoleBits.from_roles(Role.SEER)),
                    (2, RoleBits.from_roles(Role.VILLAGER)),
                    (3, RoleBits.from_roles(Role.WOLF)),
                ),
            ),
            Statement(
                (
                    "I am a Seer and I saw that Center 0 was a Wolf and "
                    "that Center 1 was a Villager."
                ),
                (
                    (1, RoleBits.from_roles(Role.SEER)),
                    (2, RoleBits.from_roles(Role.WOLF)),
                    (3, RoleBits.from_roles(Role.VILLAGER)),
                ),
            ),
            Statement(
                ("I am a Seer and I saw that Center 0 was a Wolf and that Center 1 was a Wolf."),
                (
                    (1, RoleBits.from_roles(Role.SEER)),
                    (2, RoleBits.from_roles(Role.WOLF)),
                    (3, RoleBits.from_roles(Role.WOLF)),
                ),
            ),
        )

        result = Seer.get_all_statements(player_index)

        assert set(result) == set(expected)
