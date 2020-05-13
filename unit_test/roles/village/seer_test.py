""" seer_test.py """
from collections import Counter

from src import const
from src.roles.village import Seer
from src.statements import Statement


class TestSeer:
    """ Tests for the Seer player class. """

    @staticmethod
    def test_awake_init_center_choice(large_game_roles):
        """
        Should initialize a Seer. Note that the player_index of the Seer is
        not necessarily the index where the true Seer is located.
        """
        player_index = 11
        const.CENTER_SEER_PROB = 1
        orig_roles, game_roles = [], list(large_game_roles)
        expected = [
            Statement(
                (
                    "I am a Seer and I saw that Center 1 was a Insomniac "
                    "and that Center 0 was a Troublemaker."
                ),
                (
                    (11, frozenset({"Seer"})),
                    (13, frozenset({"Insomniac"})),
                    (12, frozenset({"Troublemaker"})),
                ),
                (),
                "Seer",
            )
        ]

        seer = Seer.awake_init(player_index, game_roles, orig_roles)

        assert seer.choice_1 == (13, "Insomniac")
        assert seer.choice_2 == (12, "Troublemaker")
        assert seer.statements == expected

    @staticmethod
    def test_awake_init_player_choice(large_game_roles):
        """
        Should initialize a Seer. Note that the player_index of the Seer is
        not necessarily the index where the true Seer is located.
        """
        player_index = 11
        const.CENTER_SEER_PROB = 0
        orig_roles, game_roles = [], list(large_game_roles)
        expected = [
            Statement(
                "I am a Seer and I saw that Player 6 was a Mason.",
                ((11, frozenset({"Seer"})), (6, frozenset({"Mason"})),),
                (),
                "Seer",
            )
        ]

        seer = Seer.awake_init(player_index, game_roles, orig_roles)

        assert seer.choice_1 == (6, "Mason")
        assert seer.choice_2 == (None, None)
        assert seer.statements == expected

    @staticmethod
    def test_get_seer_statements():
        """ Should execute initialization actions and return the possible statements. """
        player_index = 1

        result = Seer.get_seer_statements(player_index, (6, "Robber"))

        assert result == [
            Statement(
                "I am a Seer and I saw that Player 6 was a Robber.",
                ((1, frozenset({"Seer"})), (6, frozenset({"Robber"})),),
                (),
                "Seer",
            )
        ]

    @staticmethod
    def test_get_all_statements():
        """ Should return the possible statements from all possible initialization actions. """
        player_index = 1
        const.ROLES = ["Wolf", "Seer", "Villager", "Wolf"]
        const.ROLE_SET = frozenset(const.ROLES)
        const.SORTED_ROLE_SET = sorted(const.ROLE_SET)
        const.ROLE_COUNTS = dict(Counter(const.ROLES))
        const.NUM_PLAYERS = 2
        const.NUM_CENTER = 2
        expected = [
            Statement(
                "I am a Seer and I saw that Player 0 was a Villager.",
                ((1, frozenset({"Seer"})), (0, frozenset({"Villager"})),),
                (),
                "Seer",
            ),
            Statement(
                "I am a Seer and I saw that Player 1 was a Villager.",
                ((1, frozenset({"Seer"})), (1, frozenset({"Villager"})),),
                (),
                "Seer",
            ),
            Statement(
                "I am a Seer and I saw that Player 0 was a Wolf.",
                ((1, frozenset({"Seer"})), (0, frozenset({"Wolf"})),),
                (),
                "Seer",
            ),
            Statement(
                "I am a Seer and I saw that Player 1 was a Wolf.",
                ((1, frozenset({"Seer"})), (1, frozenset({"Wolf"})),),
                (),
                "Seer",
            ),
            Statement(
                "I am a Seer and I saw that Player 0 was a Seer.",
                ((1, frozenset({"Seer"})), (0, frozenset({"Seer"})),),
                (),
                "Seer",
            ),
            Statement(
                "I am a Seer and I saw that Player 1 was a Seer.",
                ((1, frozenset({"Seer"})), (1, frozenset({"Seer"})),),
                (),
                "Seer",
            ),
            Statement(
                (
                    "I am a Seer and I saw that Center 0 was a Villager and "
                    "that Center 1 was a Wolf."
                ),
                ((1, frozenset({"Seer"})), (2, frozenset({"Villager"})), (3, frozenset({"Wolf"})),),
                (),
                "Seer",
            ),
            Statement(
                (
                    "I am a Seer and I saw that Center 0 was a Wolf and "
                    "that Center 1 was a Villager."
                ),
                ((1, frozenset({"Seer"})), (2, frozenset({"Wolf"})), (3, frozenset({"Villager"})),),
                (),
                "Seer",
            ),
            Statement(
                ("I am a Seer and I saw that Center 0 was a Wolf and that Center 1 was a Wolf."),
                ((1, frozenset({"Seer"})), (2, frozenset({"Wolf"})), (3, frozenset({"Wolf"})),),
                (),
                "Seer",
            ),
        ]

        result = Seer.get_all_statements(player_index)

        assert set(result) == set(expected)
