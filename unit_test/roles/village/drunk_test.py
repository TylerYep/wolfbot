''' drunk_test.py '''
from src import const
from src.statements import Statement
from src.roles.village import Drunk

class TestDrunk:
    def test_constructor_init(self, large_game_roles):
        '''
        Should initialize a Drunk. Note that the player_index of the Drunk is not necessarily
        the index where the true Drunk is located.
        '''
        player_index = 6
        orig_roles, game_roles = list(large_game_roles), list(large_game_roles)
        new_roles = ['Wolf', 'Villager', 'Robber', 'Seer', 'Villager', 'Tanner', 'Insomniac',
                     'Wolf', 'Minion', 'Mason', 'Drunk', 'Villager', 'Troublemaker', 'Mason',
                     'Hunter']

        drunk = Drunk(player_index, game_roles, orig_roles)

        assert game_roles == new_roles
        assert drunk.choice_ind == 13
        assert drunk.statements == [Statement("I am a Drunk and I swapped with Center 1.",
                                              [(6, {'Drunk'})], [(3, 6, 13)], 'Drunk')]

    def test_get_drunk_statements(self):
        ''' Should execute initialization actions and return the possible statements. '''
        player_index = 4

        result = Drunk.get_drunk_statements(player_index, 12)

        assert result == [Statement("I am a Drunk and I swapped with Center 0.",
                                    [(4, {'Drunk'})], [(3, 4, 12)], 'Drunk')]

    def test_get_all_statements(self):
        ''' Should return the possible statements from all possible initialization actions. '''
        player_index = 2
        const.ROLES = ['Wolf', 'Seer', 'Drunk', 'Villager', 'Robber', 'Wolf']
        const.ROLE_SET = set(const.ROLES)
        const.NUM_PLAYERS = 3
        const.NUM_CENTER = 3
        expected_statements = [Statement("I am a Drunk and I swapped with Center 0.",
                                         [(2, {'Drunk'})], [(3, 2, 3)], 'Drunk'),
                               Statement("I am a Drunk and I swapped with Center 1.",
                                         [(2, {'Drunk'})], [(3, 2, 4)], 'Drunk'),
                               Statement("I am a Drunk and I swapped with Center 2.",
                                         [(2, {'Drunk'})], [(3, 2, 5)], 'Drunk')]

        result = Drunk.get_all_statements(player_index)

        assert result == expected_statements
