""" villager_test.py """
from wolfbot.const import Role
from wolfbot.roles import Villager
from wolfbot.statements import Statement


class TestVillager:
    """Tests for the Villager player class."""

    @staticmethod
    def test_awake_init() -> None:
        """Should initialize a Villager."""
        player_index = 5

        villager = Villager.awake_init(player_index, [], ())  # Other params are unused.

        assert villager.statements == (
            Statement("I am a Villager.", ((5, frozenset({Role.VILLAGER})),)),
        )

    @staticmethod
    def test_get_villager_statements() -> None:
        """Execute initialization actions and return the possible statements."""
        player_index = 0

        result = Villager.get_villager_statements(player_index)

        assert result == (
            Statement("I am a Villager.", ((0, frozenset({Role.VILLAGER})),)),
        )

    @staticmethod
    def test_get_all_statements() -> None:
        """Should return possible statements from all possible initializations."""
        player_index = 2

        result = Villager.get_all_statements(player_index)

        assert result == (
            Statement("I am a Villager.", ((2, frozenset({Role.VILLAGER})),)),
        )
