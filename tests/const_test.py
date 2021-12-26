""" const_test.py """
from wolfbot import const
from wolfbot.enums import Role
from wolfbot.roles import Mason, Seer


class TestLRUCache:
    """Tests for the lru_cache function."""

    @staticmethod
    def test_lru_cache_hit() -> None:
        """Correctly cache a function call cache hit."""
        result_1 = Seer.get_seer_statements(1, (6, Role.ROBBER))

        result_2 = Seer.get_seer_statements(1, (6, Role.ROBBER))
        info = Seer.get_seer_statements.cache_info()

        assert result_1 == result_2
        assert info.hits == 1
        assert info.misses == 1
        assert info.currsize == 1

    @staticmethod
    def test_lru_cache_miss() -> None:
        """Correctly cache a function call cache miss."""
        result_1 = Seer.get_seer_statements(2, (6, Role.ROBBER))

        result_2 = Seer.get_seer_statements(2, (2, Role.ROBBER))
        info = Seer.get_seer_statements.cache_info()

        assert result_1 != result_2
        assert info.hits == 0
        assert info.misses == 2
        assert info.currsize == 2

    @staticmethod
    def test_lru_cache_side_effects() -> None:
        """Showcase the problem with using a cache and changing internal constants."""
        result_1 = Mason.get_mason_statements(6, (6,))
        const.NUM_PLAYERS = 3

        result_2 = Mason.get_mason_statements(6, (6,))
        info = Mason.get_mason_statements.cache_info()

        # This following assert is true, which is incorrect.
        # It is unclear how to fix this problem.
        assert result_1 == result_2
        assert info.hits == 1
        assert info.misses == 1
        assert info.currsize == 1
