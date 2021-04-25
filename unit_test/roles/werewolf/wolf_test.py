""" wolf_test.py """
from conftest import set_roles
from src import const
from src.const import Role
from src.roles import Wolf
from src.statements import KnowledgeBase


class TestWolf:
    """Tests for the Wolf player class."""

    @staticmethod
    def test_awake_init_medium(medium_game_roles: tuple[Role, ...]) -> None:
        """
        Should initialize a Wolf. Note that the player_index of the Wolf is
        not necessarily the index where the true Wolf is located.
        """
        set_roles(Role.WOLF, *medium_game_roles[1:])
        player_index = 2

        wolf = Wolf.awake_init(player_index, list(const.ROLES), const.ROLES)
        assert wolf.wolf_indices == (0, 2)
        assert wolf.center_index is None
        assert wolf.center_role is None

    @staticmethod
    def test_awake_init_large(large_game_roles: tuple[Role, ...]) -> None:
        """
        Should initialize a Wolf. Note that the player_index of the Wolf is
        not necessarily the index where the true Wolf is located.
        """
        player_index = 7

        wolf = Wolf.awake_init(player_index, list(const.ROLES), const.ROLES)

        assert wolf.wolf_indices == (0, 7)
        assert wolf.center_index is None
        assert wolf.center_role is None

    @staticmethod
    def test_awake_init_center(large_game_roles: tuple[Role, ...]) -> None:
        """
        Should initialize a Center Wolf. Note that the player_index of the Wolf is
        not necessarily the index where the true Wolf is located.
        """
        set_roles(Role.VILLAGER, *large_game_roles[1:])
        player_index = 7

        wolf = Wolf.awake_init(player_index, list(const.ROLES), const.ROLES)

        assert wolf.wolf_indices == (7,)
        assert wolf.center_index == 13
        assert wolf.center_role is Role.INSOMNIAC

    @staticmethod
    def test_get_random_statement_medium(
        medium_game_roles: tuple[Role, ...], medium_knowledge_base: KnowledgeBase
    ) -> None:
        """Execute initialization actions and return the possible statements."""
        player_index = 4
        wolf = Wolf(player_index, (1, player_index))

        wolf.analyze(medium_knowledge_base)
        _ = wolf.get_statement(medium_knowledge_base)

        assert len(wolf.statements) == 61

    @staticmethod
    def test_get_reg_wolf_statement_medium(
        medium_game_roles: tuple[Role, ...], medium_knowledge_base: KnowledgeBase
    ) -> None:
        """Execute initialization actions and return the possible statements."""
        const.USE_REG_WOLF = True
        player_index = 4
        wolf = Wolf(player_index, (1, player_index))

        wolf.analyze(medium_knowledge_base)
        _ = wolf.get_statement(medium_knowledge_base)

        assert len(wolf.statements) == 7

    @staticmethod
    def test_get_center_statement_medium(
        medium_game_roles: tuple[Role, ...], medium_knowledge_base: KnowledgeBase
    ) -> None:
        """Execute initialization actions and return the possible statements."""
        const.USE_REG_WOLF = True
        player_index = 2
        wolf = Wolf(player_index, (1, player_index), 5, Role.ROBBER)

        wolf.analyze(medium_knowledge_base)
        _ = wolf.get_statement(medium_knowledge_base)

        assert len(wolf.statements) == 4

    @staticmethod
    def test_get_random_statement_large(
        large_game_roles: tuple[Role, ...], large_knowledge_base: KnowledgeBase
    ) -> None:
        """Execute initialization actions and return the possible statements."""
        player_index = 4
        wolf = Wolf(player_index, (1, player_index))

        wolf.analyze(large_knowledge_base)
        _ = wolf.get_statement(large_knowledge_base)

        assert len(wolf.statements) == 615

    @staticmethod
    def test_get_reg_wolf_statement_large(
        large_game_roles: tuple[Role, ...], large_knowledge_base: KnowledgeBase
    ) -> None:
        """Execute initialization actions and return the possible statements."""
        const.USE_REG_WOLF = True
        player_index = 4
        wolf = Wolf(player_index, (1, player_index))

        wolf.analyze(large_knowledge_base)
        _ = wolf.get_statement(large_knowledge_base)

        assert len(wolf.statements) == 74

    # @staticmethod
    # def test_eval_fn() -> None:
    #     """ Should return the value from the chosen statement action. """
    #     pass
