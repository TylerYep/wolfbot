''' seer_test.py '''
from collections import Counter

from src import const
from src.roles.village import Seer
from src.statements import Statement


class TestSeer:
    ''' Tests for the Seer player class. '''

    @staticmethod
    def test_awake_init_center_choice(large_game_roles):
        '''
        Should initialize a Seer. Note that the player_index of the Seer is
        not necessarily the index where the true Seer is located.
        '''
        player_index = 11
        const.CENTER_SEER_PROB = 1
        orig_roles, game_roles = [], list(large_game_roles)
        expected = [Statement(("I am a Seer and I saw that Center 1 was a Insomniac "
                               "and that Center 0 was a Troublemaker."),
                              [(11, {'Seer'}), (13, {'Insomniac'}), (12, {'Troublemaker'})],
                              [], 'Seer')]

        seer = Seer.awake_init(player_index, game_roles, orig_roles)

        assert seer.choice_1 == (13, 'Insomniac')
        assert seer.choice_2 == (12, 'Troublemaker')
        assert seer.statements == expected

    @staticmethod
    def test_awake_init_player_choice(large_game_roles):
        '''
        Should initialize a Seer. Note that the player_index of the Seer is
        not necessarily the index where the true Seer is located.
        '''
        player_index = 11
        const.CENTER_SEER_PROB = 0
        orig_roles, game_roles = [], list(large_game_roles)
        expected = [Statement("I am a Seer and I saw that Player 6 was a Mason.",
                              [(11, {'Seer'}), (6, {'Mason'})], [], 'Seer')]

        seer = Seer.awake_init(player_index, game_roles, orig_roles)

        assert seer.choice_1 == (6, 'Mason')
        assert seer.choice_2 == (None, None)
        assert seer.statements == expected

    @staticmethod
    def test_get_seer_statements():
        ''' Should execute initialization actions and return the possible statements. '''
        player_index = 1

        result = Seer.get_seer_statements(player_index, (6, 'Robber'))

        assert result == [Statement("I am a Seer and I saw that Player 6 was a Robber.",
                                    [(1, {'Seer'}), (6, {'Robber'})], [], 'Seer')]

    @staticmethod
    def test_get_all_statements():
        ''' Should return the possible statements from all possible initialization actions. '''
        player_index = 1
        const.ROLES = ['Wolf', 'Seer', 'Villager', 'Wolf']
        const.ROLE_SET = set(const.ROLES)
        const.ROLE_COUNTS = dict(Counter(const.ROLES))
        const.NUM_PLAYERS = 2
        const.NUM_CENTER = 2
        expected = [Statement("I am a Seer and I saw that Player 0 was a Villager.",
                              [(1, {'Seer'}), (0, {'Villager'})], [], 'Seer'),
                    Statement("I am a Seer and I saw that Player 1 was a Villager.",
                              [(1, {'Seer'}), (1, {'Villager'})], [], 'Seer'),
                    Statement("I am a Seer and I saw that Player 0 was a Wolf.",
                              [(1, {'Seer'}), (0, {'Wolf'})], [], 'Seer'),
                    Statement("I am a Seer and I saw that Player 1 was a Wolf.",
                              [(1, {'Seer'}), (1, {'Wolf'})], [], 'Seer'),
                    Statement("I am a Seer and I saw that Player 0 was a Seer.",
                              [(1, {'Seer'}), (0, {'Seer'})], [], 'Seer'),
                    Statement("I am a Seer and I saw that Player 1 was a Seer.",
                              [(1, {'Seer'}), (1, {'Seer'})], [], 'Seer'),
                    Statement(("I am a Seer and I saw that Center 0 was a Villager and "
                               "that Center 1 was a Wolf."),
                              [(1, {'Seer'}), (2, {'Villager'}), (3, {'Wolf'})], [], 'Seer'),
                    Statement(("I am a Seer and I saw that Center 0 was a Wolf and "
                               "that Center 1 was a Villager."),
                              [(1, {'Seer'}), (2, {'Wolf'}), (3, {'Villager'})], [], 'Seer'),
                    Statement(("I am a Seer and I saw that Center 0 was a Wolf and "
                               "that Center 1 was a Wolf."),
                              [(1, {'Seer'}), (2, {'Wolf'}), (3, {'Wolf'})], [], 'Seer')]

        result = Seer.get_all_statements(player_index)

        assert set(result) == set(expected)
