''' robber_test.py '''
from src import const
from src.statements import Statement
from src.roles.village import Robber

class TestRobber:
    def test_constructor_init(self, large_game_roles):
        '''
        Should initialize a Robber. Note that the player_index of the Robber is not necessarily
        the index where the true Robber is located.
        '''
        player_index = 2
        orig_roles, game_roles = [], list(large_game_roles)
        new_roles = ['Wolf', 'Villager', 'Mason', 'Seer', 'Villager', 'Tanner', 'Robber', 'Wolf',
                     'Minion', 'Mason', 'Drunk', 'Villager', 'Troublemaker', 'Insomniac', 'Hunter']
        expected = [Statement("I am a Robber and I swapped with Player 6. I am now a Mason.",
                              [(2, {'Robber'}), (6, {'Mason'})], [(1, 6, 2)], 'Robber')]

        robber = Robber(player_index, game_roles, orig_roles)

        assert game_roles == new_roles
        assert robber.choice_ind == 6
        assert robber.new_role == 'Mason'
        assert robber.statements == expected

    def test_get_robber_statements(self):
        ''' Should execute initialization actions and return the possible statements. '''
        player_index = 4

        result = Robber.get_robber_statements(player_index, 3, 'Seer')

        assert result == [Statement("I am a Robber and I swapped with Player 3. I am now a Seer.",
                                    [(4, {'Robber'}), (3, {'Seer'})], [(1, 3, 4)], 'Robber')]

    def test_get_all_statements(self):
        ''' Should return the possible statements from all possible initialization actions. '''
        player_index = 1
        const.ROLE_SET = set(['Wolf', 'Robber', 'Villager'])
        const.NUM_PLAYERS = 2
        expected = [Statement("I am a Robber and I swapped with Player 0. I am now a Villager.",
                              [(1, {'Robber'}), (0, {'Villager'})], [(1, 0, 1)], 'Robber'),
                    Statement("I am a Robber and I swapped with Player 0. I am now a Wolf.",
                              [(1, {'Robber'}), (0, {'Wolf'})], [(1, 0, 1)], 'Robber'),
                    Statement("I am a Robber and I swapped with Player 0. I am now a Robber.",
                              [(1, {'Robber'}), (0, {'Robber'})], [(1, 0, 1)], 'Robber')]

        result = Robber.get_all_statements(player_index)

        assert set(result) == set(expected)