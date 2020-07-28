""" tanner_test.py """
from src.roles import Tanner
from src.statements import Statement


class TestTanner:
    """ Tests for the Tanner player class. """

    # @staticmethod
    # def test_awake_init(large_game_roles) -> None:
    #     '''
    #     Should initialize a Tanner. Note that the player_index of the Tanner is
    #     not necessarily the index where the true Tanner is located.
    #     '''
    #     player_index = 3
    #     expected = None

    # tanner = Tanner.awake_init(player_index, [], [])

    # assert tanner.statements == expected

    @staticmethod
    def test_get_random_statement(large_game_roles, large_knowledge_base) -> None:
        """ Should execute initialization actions and return the possible statements. """
        player_index = 1
        tanner = Tanner(player_index)

        tanner.analyze(large_knowledge_base)
        result = tanner.get_statement(large_knowledge_base)

        assert len(tanner.statements) == 615
        assert result == Statement(
            "I am a Seer and I saw that Center 0 was a Troublemaker and that Center 2 was a Mason.",
            (
                (1, frozenset({"Seer"})),
                (12, frozenset({"Troublemaker"})),
                (14, frozenset({"Mason"})),
            ),
        )
