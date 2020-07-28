""" minion_test.py """
from src import const
from src.roles import Minion
from src.statements import Statement


class TestMinion:
    """ Tests for the Minion player class. """

    @staticmethod
    def test_get_random_statement_medium(medium_game_roles, medium_knowledge_base) -> None:
        """ Should execute initialization actions and return the possible statements. """
        player_index = 4
        minion = Minion(player_index, [1, 5])

        minion.analyze(medium_knowledge_base)
        result = minion.get_statement(medium_knowledge_base)

        assert len(minion.statements) == 61
        assert result == Statement(
            "I am a Seer and I saw that Player 1 was a Seer.",
            ((4, frozenset({"Seer"})), (1, frozenset({"Seer"})),),
        )

    @staticmethod
    def test_get_reg_wolf_statement_medium(medium_game_roles, medium_knowledge_base) -> None:
        """ Should execute initialization actions and return the possible statements. """
        const.USE_REG_WOLF = True
        player_index = 4
        minion = Minion(player_index, [1, 5])

        minion.analyze(medium_knowledge_base)
        _ = minion.get_statement(medium_knowledge_base)

        assert len(minion.statements) == 16

    @staticmethod
    def test_get_random_statement_large(large_game_roles, large_knowledge_base) -> None:
        """ Should execute initialization actions and return the possible statements. """
        player_index = 4
        minion = Minion(player_index, [1, 5])

        minion.analyze(large_knowledge_base)
        _ = minion.get_statement(large_knowledge_base)

        assert len(minion.statements) == 615

    @staticmethod
    def test_get_reg_wolf_statement_large(large_game_roles, large_knowledge_base) -> None:
        """ Should execute initialization actions and return the possible statements. """
        const.USE_REG_WOLF = True
        player_index = 4
        minion = Minion(player_index, [1, 5])

        minion.analyze(large_knowledge_base)
        _ = minion.get_statement(large_knowledge_base)

        assert len(minion.statements) == 76
