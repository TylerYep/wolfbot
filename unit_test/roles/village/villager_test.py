''' villager_test.py '''
from src.statements import Statement
from src.roles.village import Villager

class TestVillager:
    def test_awake_init(self):
        ''' Should initialize a Villager. '''
        player_index = 5

        villager = Villager.awake_init(player_index, [], [])  # Other params are unused.

        assert villager.statements == [Statement('I am a Villager.', [(5, {'Villager'})])]

    def test_get_villager_statements(self):
        ''' Should execute initialization actions and return the possible statements. '''
        player_index = 0

        result = Villager.get_villager_statements(player_index)

        assert result == [Statement('I am a Villager.', [(0, {'Villager'})])]

    def test_get_all_statements(self):
        ''' Should return the possible statements from all possible initialization actions. '''
        player_index = 2

        result = Villager.get_all_statements(player_index)

        assert result == [Statement('I am a Villager.', [(2, {'Villager'})])]
