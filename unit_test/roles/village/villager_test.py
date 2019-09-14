''' villager_test.py '''
from src.statements import Statement
from src.roles.village import Villager

class TestVillager:
    def test_constructor(self):
        player_index = 5

        villager = Villager(player_index, [], [])  # Other params are unused.

        assert villager.statements == [Statement('I am a Villager.', [(5, {'Villager'})])]

    def test_get_villager_statements(self):
        player_index = 0

        result = Villager.get_villager_statements(player_index)

        assert result == [Statement('I am a Villager.', [(0, {'Villager'})])]

    def test_get_all_statements(self):
        player_index = 2

        result = Villager.get_all_statements(player_index)

        assert result == [Statement('I am a Villager.', [(2, {'Villager'})])]
