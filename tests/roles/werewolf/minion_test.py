from wolfbot import const
from wolfbot.enums import Role
from wolfbot.roles import Minion
from wolfbot.statements import KnowledgeBase


class TestMinion:
    """Tests for the Minion player class."""

    @staticmethod
    def test_get_random_statement_medium(
        medium_game_roles: tuple[Role, ...], medium_knowledge_base: KnowledgeBase
    ) -> None:
        """Execute initialization actions and return the possible statements."""
        player_index = 4
        minion = Minion(player_index, (1, 5))

        minion.analyze(medium_knowledge_base)
        _ = minion.get_statement(medium_knowledge_base)

        assert len(minion.statements) == 61

    @staticmethod
    def test_get_reg_wolf_statement_medium(
        medium_game_roles: tuple[Role, ...], medium_knowledge_base: KnowledgeBase
    ) -> None:
        """Execute initialization actions and return the possible statements."""
        const.USE_REG_WOLF = True
        player_index = 4
        minion = Minion(player_index, (1, 5))

        minion.analyze(medium_knowledge_base)
        _ = minion.get_statement(medium_knowledge_base)

        assert len(minion.statements) == 11

    @staticmethod
    def test_get_random_statement_large(
        large_game_roles: tuple[Role, ...], large_knowledge_base: KnowledgeBase
    ) -> None:
        """Execute initialization actions and return the possible statements."""
        player_index = 4
        minion = Minion(player_index, (1, 5))

        minion.analyze(large_knowledge_base)
        _ = minion.get_statement(large_knowledge_base)

        assert len(minion.statements) == 615

    @staticmethod
    def test_get_reg_wolf_statement_large(
        large_game_roles: tuple[Role, ...], large_knowledge_base: KnowledgeBase
    ) -> None:
        """Execute initialization actions and return the possible statements."""
        const.USE_REG_WOLF = True
        player_index = 4
        minion = Minion(player_index, (1, 5))

        minion.analyze(large_knowledge_base)
        _ = minion.get_statement(large_knowledge_base)

        assert len(minion.statements) == 73
