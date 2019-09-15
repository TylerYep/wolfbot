''' drunk_test.py '''
from src import const
from src.statements import Statement
from src.roles.village import Drunk

class TestDrunk:
    def test_constructor(self, large_game_roles):
        ''' Should initialize a Drunk. '''
        player_index = 6
        orig_roles, game_roles = list(large_game_roles), list(large_game_roles)

        drunk = Drunk(player_index, game_roles, orig_roles)

        assert drunk.statements == [Statement("I am a Drunk and I swapped with Center 1.",
                                              [(6, {'Drunk'})], [(3, 13, 6)], 'Drunk')]

    def test_get_drunk_statements(self):
        ''' Should execute initialization actions and return the possible statements. '''
        player_index = 4

        result = Drunk.get_drunk_statements(player_index, 12)

        assert result == [Statement("I am a Drunk and I swapped with Center 0.",
                                    [(4, {'Drunk'})], [(3, 12, 4)], 'Drunk')]

    def test_get_all_statements(self):
        ''' Should return the possible statements from all possible initialization actions. '''
        player_index = 2
        const.ROLES = ['Wolf', 'Seer', 'Drunk', 'Villager', 'Robber', 'Wolf']
        const.ROLE_SET = set(const.ROLES)
        const.NUM_PLAYERS = 3
        const.NUM_CENTER = 3
        expected_statements = [Statement("I am a Drunk and I swapped with Center 0.",
                                         [(2, {'Drunk'})], [(3, 3, 2)], 'Drunk'),
                               Statement("I am a Drunk and I swapped with Center 1.",
                                         [(2, {'Drunk'})], [(3, 4, 2)], 'Drunk'),
                               Statement("I am a Drunk and I swapped with Center 2.",
                                         [(2, {'Drunk'})], [(3, 5, 2)], 'Drunk')]

        result = Drunk.get_all_statements(player_index)

        assert result == expected_statements
