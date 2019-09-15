''' mason_test.py '''
from src import const
from src.statements import Statement
from src.roles.village import Mason

class TestMason:
    def test_constructor(self, large_game_roles):
        ''' Should initialize a Mason. '''
        player_index = 5
        orig_roles, game_roles = large_game_roles, []

        mason = Mason(player_index, game_roles, orig_roles)

        assert mason.mason_indices == [6, 9]
        assert mason.statements == [Statement("I am a Mason. The other Mason is Player 6.",
                                              [(5, {'Mason'}), (6, {'Mason'})], [], 'Mason')]

    def test_get_mason_statements(self):
        ''' Should execute initialization actions and return the possible statements. '''
        player_index = 0

        result = Mason.get_mason_statements(player_index, [6, 9])

        assert result == [Statement("I am a Mason. The other Mason is Player 6.",
                                    [(0, {'Mason'}), (6, {'Mason'})], [], 'Mason')]

    def test_get_all_statements(self):
        ''' Should return the possible statements from all possible initialization actions. '''
        player_index = 2
        const.ROLES = ['Wolf', 'Seer', 'Robber', 'Villager']
        const.NUM_PLAYERS = 3
        expected_statements = [Statement("I am a Mason. The other Mason is not present.",
                                         [(2, {'Mason'}),
                                          (0, {'Wolf', 'Seer', 'Robber', 'Villager'}),
                                          (1, {'Wolf', 'Seer', 'Robber', 'Villager'})],
                                         [], 'Mason'),
                               Statement("I am a Mason. The other Mason is Player 0.",
                                         [(2, {'Mason'}), (0, {'Mason'})], [], 'Mason'),
                               Statement("I am a Mason. The other Mason is Player 1.",
                                         [(2, {'Mason'}), (1, {'Mason'})], [], 'Mason')]

        result = Mason.get_all_statements(player_index)

        assert result == expected_statements
