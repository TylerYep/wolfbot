""" insomniac_test.py """
from src import const
from src.roles.village import Insomniac
from src.statements import Statement


class TestInsomniac:
    """ Tests for the Insomniac player class. """

    @staticmethod
    def test_awake_init():
        """ Should initialize a Insomniac. """
        player_index = 1
        game_roles = ["Insomniac", "Robber", "Villager"]
        expected = [
            Statement(
                (
                    "I am a Insomniac and when I woke up I was a Robber. "
                    "I don't know who I switched with."
                ),
                [(1, {"Insomniac"})],
                [],
                "Insomniac",
            )
        ]

        insomniac = Insomniac.awake_init(player_index, game_roles, [])

        assert insomniac.new_role == "Robber"
        assert insomniac.statements == expected

    @staticmethod
    def test_get_insomniac_statements():
        """ Should execute initialization actions and return the possible statements. """
        player_index = 0
        expected = [
            Statement(
                (
                    "I am a Insomniac and when I woke up I was a Hunter. "
                    "I don't know who I switched with."
                ),
                [(0, {"Insomniac"})],
                [],
                "Insomniac",
            )
        ]

        result = Insomniac.get_insomniac_statements(player_index, "Hunter")

        assert result == expected

    @staticmethod
    def test_get_all_statements():
        """ Should return the possible statements from all possible initialization actions. """
        player_index = 2
        const.ROLE_SET = frozenset(["Wolf", "Insomniac", "Seer"])
        const.SORTED_ROLE_SET = sorted(const.ROLE_SET)
        expected = [
            Statement(
                (
                    "I am a Insomniac and when I woke up I was a Wolf. I don't know "
                    "who I switched with."
                ),
                [(2, {"Insomniac"})],
                [],
                "Insomniac",
            ),
            Statement(
                "I am a Insomniac and when I woke up I was a Insomniac.",
                [(2, {"Insomniac"})],
                [],
                "Insomniac",
            ),
            Statement(
                (
                    "I am a Insomniac and when I woke up I was a Seer. I don't know "
                    "who I switched with."
                ),
                [(2, {"Insomniac"})],
                [],
                "Insomniac",
            ),
        ]

        result = Insomniac.get_all_statements(player_index)

        assert set(result) == set(expected)
