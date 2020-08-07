""" insomniac_test.py """
from conftest import set_roles
from src.const import Role, RoleBits
from src.roles import Insomniac
from src.statements import Statement


class TestInsomniac:
    """ Tests for the Insomniac player class. """

    @staticmethod
    def test_awake_init() -> None:
        """ Should initialize a Insomniac. """
        player_index = 1
        game_roles = [Role.INSOMNIAC, Role.ROBBER, Role.VILLAGER]
        expected = (
            Statement(
                (
                    "I am a Insomniac and when I woke up I was a Robber. "
                    "I don't know who I switched with."
                ),
                ((1, RoleBits.from_roles(Role.INSOMNIAC)),),
            ),
        )

        insomniac = Insomniac.awake_init(player_index, game_roles, ())

        assert insomniac.new_role is Role.ROBBER
        assert insomniac.statements == expected

    @staticmethod
    def test_get_insomniac_statements() -> None:
        """ Should execute initialization actions and return the possible statements. """
        player_index = 0
        expected = (
            Statement(
                (
                    "I am a Insomniac and when I woke up I was a Hunter. "
                    "I don't know who I switched with."
                ),
                ((0, RoleBits.from_roles(Role.INSOMNIAC)),),
            ),
        )

        result = Insomniac.get_insomniac_statements(player_index, Role.HUNTER)

        assert result == expected

    @staticmethod
    def test_get_all_statements() -> None:
        """ Should return the possible statements from all possible initialization actions. """
        player_index = 2
        set_roles(Role.WOLF, Role.INSOMNIAC, Role.SEER)
        expected = (
            Statement(
                (
                    "I am a Insomniac and when I woke up I was a Wolf. I don't know "
                    "who I switched with."
                ),
                ((2, RoleBits.from_roles(Role.INSOMNIAC)),),
            ),
            Statement(
                "I am a Insomniac and when I woke up I was a Insomniac.",
                ((2, RoleBits.from_roles(Role.INSOMNIAC)),),
            ),
            Statement(
                (
                    "I am a Insomniac and when I woke up I was a Seer. I don't know "
                    "who I switched with."
                ),
                ((2, RoleBits.from_roles(Role.INSOMNIAC)),),
            ),
        )

        result = Insomniac.get_all_statements(player_index)

        assert set(result) == set(expected)
