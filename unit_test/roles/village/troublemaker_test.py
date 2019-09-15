''' troublemaker_test.py '''
from src import const
from src.statements import Statement
from src.roles.village import Troublemaker

class TestTroublemaker:
    def test_constructor(self, large_game_roles):
        ''' Should initialize a Troublemaker. '''
        player_index = 11
        orig_roles, game_roles = [], list(large_game_roles)
        expected = [Statement("I am a Troublemaker and I swapped Player 5 and Player 1.",
                              [(11, {'Troublemaker'})], [(2, 5, 1)], 'Troublemaker')]

        tmkr = Troublemaker(player_index, game_roles, orig_roles)

        assert tmkr.statements == expected

    def test_get_troublemaker_statements(self):
        ''' Should execute initialization actions and return the possible statements. '''
        player_index = 1

        result = Troublemaker.get_troublemaker_statements(player_index, 6, 3)

        assert result == [Statement("I am a Troublemaker and I swapped Player 6 and Player 3.",
                                    [(1, {'Troublemaker'})], [(2, 6, 3)], 'Troublemaker')]

    def test_get_all_statements(self):
        ''' Should return the possible statements from all possible initialization actions. '''
        player_index = 2
        const.ROLES = ['Wolf', 'Seer', 'Troublemaker', 'Villager', 'Robber', 'Wolf']
        const.ROLE_SET = set(const.ROLES)
        const.NUM_PLAYERS = 3
        const.NUM_CENTER = 3
        expected_statements = [Statement("I am a Troublemaker and I swapped Player 0 and Player 1.",
                                         [(2, {'Troublemaker'})], [(2, 0, 1)], 'Troublemaker')]

        result = Troublemaker.get_all_statements(player_index)

        assert result == expected_statements
