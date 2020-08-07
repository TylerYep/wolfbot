""" const_test.py """
from src import const
from src.const import Role, RoleBits
from src.roles import Mason, Seer


class TestRoleBits:
    """ Tests for the Bits class. """

def test_everything(medium_game_roles):
    # Role.DRUNK, Role.MINION, Role.ROBBER, Role.SEER, Role.TROUBLEMAKER, Role.WOLF
    x = RoleBits.from_num(5)

    y = RoleBits.from_roles(Role.MINION, Role.ROBBER, Role.WOLF)
    assert str(y) == "011001"
    assert y.is_solo is False

    assert str(~y) == "100110"

    y.set_bit(3, True)
    assert str(y) == "011101"
    y.set_bit(3, False)
    assert str(y) == "011001"
    y.set_bit(0, False)
    assert str(y) == "011001"
    y.set_bit(5, False)
    y.set_bit(1, False)
    assert str(y) == "001000"

    assert y.is_solo is True
    assert y.solo_role == Role.ROBBER


class TestLRUCache:
    """ Tests for the lru_cache function. """

    @staticmethod
    def test_lru_cache_hit() -> None:
        """ Correctly cache a function call cache hit. """
        result_1 = Seer.get_seer_statements(1, (6, Role.ROBBER))

        result_2 = Seer.get_seer_statements(1, (6, Role.ROBBER))
        info = Seer.get_seer_statements.cache_info()

        assert result_1 == result_2
        assert info.hits == 1
        assert info.misses == 1
        assert info.currsize == 1

    @staticmethod
    def test_lru_cache_miss() -> None:
        """ Correctly cache a function call cache miss. """
        result_1 = Seer.get_seer_statements(2, (6, Role.ROBBER))

        result_2 = Seer.get_seer_statements(2, (2, Role.ROBBER))
        info = Seer.get_seer_statements.cache_info()

        assert result_1 != result_2
        assert info.hits == 0
        assert info.misses == 2
        assert info.currsize == 2

    @staticmethod
    def test_lru_cache_side_effects() -> None:
        """ Showcase the problem with using a cache and changing internal constants. """
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
