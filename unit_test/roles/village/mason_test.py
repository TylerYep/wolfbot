''' mason_test.py '''
from src import const
from src.statements import Statement
from src.roles.village import Mason


class TestMason:
    ''' Tests for the Mason player class. '''

    @staticmethod
    def test_awake_init(large_game_roles):
        ''' Should initialize a Mason. '''
        player_index = 6
        orig_roles, game_roles = list(large_game_roles), []

        mason = Mason.awake_init(player_index, game_roles, orig_roles)

        assert mason.mason_indices == [6, 9]
        assert mason.statements == [Statement("I am a Mason. The other Mason is Player 9.",
                                              [(6, {'Mason'}), (9, {'Mason'})], [], 'Mason')]

    @staticmethod
    def test_get_mason_statements():
        ''' Should execute initialization actions and return the possible statements. '''
        player_index = 9

        result = Mason.get_mason_statements(player_index, [6, 9])

        assert result == [Statement("I am a Mason. The other Mason is Player 6.",
                                    [(9, {'Mason'}), (6, {'Mason'})], [], 'Mason')]

    @staticmethod
    def test_get_single_mason_statement():
        ''' Should give the proper statement when only one Mason is present. '''
        player_index = 2
        const.ROLES = ('Wolf', 'Seer', 'Mason', 'Villager')
        const.ROLE_SET = set(const.ROLES)
        const.NUM_PLAYERS = 3
        result = Mason.get_mason_statements(player_index, [2])

        assert result == [Statement("I am a Mason. The other Mason is not present.",
                                    [(2, {'Mason'}),
                                     (0, {'Wolf', 'Seer', 'Villager'}),
                                     (1, {'Wolf', 'Seer', 'Villager'})],
                                    [], 'Mason')]

    @staticmethod
    def test_get_all_statements():
        ''' Should return the possible statements from all possible initialization actions. '''
        player_index = 2
        const.ROLES = ['Wolf', 'Seer', 'Mason', 'Villager']
        const.ROLE_SET = set(const.ROLES)
        const.NUM_PLAYERS = 3
        expected_statements = [Statement("I am a Mason. The other Mason is not present.",
                                         [(2, {'Mason'}),
                                          (0, {'Wolf', 'Seer', 'Villager'}),
                                          (1, {'Wolf', 'Seer', 'Villager'})],
                                         [], 'Mason'),
                               Statement("I am a Mason. The other Mason is Player 0.",
                                         [(2, {'Mason'}), (0, {'Mason'})], [], 'Mason'),
                               Statement("I am a Mason. The other Mason is Player 1.",
                                         [(2, {'Mason'}), (1, {'Mason'})], [], 'Mason')]

        result = Mason.get_all_statements(player_index)

        assert result == expected_statements
