""" tanner_test.py """
from typing import Tuple

from src.roles import Tanner
from src.statements import KnowledgeBase


class TestTanner:
    """ Tests for the Tanner player class. """

    @staticmethod
    def test_awake_init(large_game_roles: Tuple[str, ...]) -> None:
        """
        Should initialize a Tanner. Note that the player_index of the Tanner is
        not necessarily the index where the true Tanner is located.
        """
        player_index = 3
        expected = ()

        tanner = Tanner.awake_init(player_index, [], ())

        assert tanner.statements == expected

    @staticmethod
    def test_get_random_statement(
        large_game_roles: Tuple[str, ...], large_knowledge_base: KnowledgeBase
    ) -> None:
        """ Should execute initialization actions and return the possible statements. """
        player_index = 1
        tanner = Tanner(player_index)

        tanner.analyze(large_knowledge_base)
        _ = tanner.get_statement(large_knowledge_base)

        assert len(tanner.statements) == 615
