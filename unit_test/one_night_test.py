''' one_night_test.py '''
from src import one_night, const

class TestPlayOneNightWerewolf:
    ''' Tests for the play_one_night_werewolf function. '''

    @staticmethod
    def test_one_night_small(caplog, example_small_game_result):
        ''' Correctly play one round of one night werewolf. '''
        const.REPLAY_FILE = 'unit_test/test_data/replay.json'

        result = one_night.play_one_night_werewolf()

        assert result == example_small_game_result
        captured = tuple(map(lambda x: x.getMessage(), caplog.records))
        with open('unit_test/test_data/one_night_small.out') as output_file:
            expected = output_file.read().split('\n')
            assert '\n'.join(captured) == '\n'.join(expected)

    @staticmethod
    def test_one_night_medium(caplog, example_medium_game_result):
        ''' Correctly play one round of one night werewolf. '''
        const.REPLAY_FILE = 'unit_test/test_data/replay.json'

        result = one_night.play_one_night_werewolf()

        assert result == example_medium_game_result
        captured = tuple(map(lambda x: x.getMessage(), caplog.records))
        with open('unit_test/test_data/one_night_medium.out') as output_file:
            expected = output_file.read().split('\n')
            assert '\n'.join(captured) == '\n'.join(expected)

    @staticmethod
    def test_one_night_large(caplog, example_large_game_result):
        ''' Correctly play one round of one night werewolf. '''
        const.REPLAY_FILE = 'unit_test/test_data/replay.json'

        result = one_night.play_one_night_werewolf()

        assert result == example_large_game_result
        captured = list(map(lambda x: x.getMessage(), caplog.records))
        with open('unit_test/test_data/one_night_large.out') as output_file:
            expected = output_file.read().split('\n')
            assert '\n'.join(captured) == '\n'.join(expected)


class TestPrintRoles:
    ''' Tests for the print_roles function. '''

    @staticmethod
    def test_print_roles(caplog, small_game_roles):
        ''' Correctly print and format roles. '''
        const.ROLES = small_game_roles
        shuffled_roles = ['Seer', 'Villager', 'Wolf', 'Robber']

        one_night.print_roles(shuffled_roles, 'Hidden')

        captured = caplog.records[0].getMessage()
        expected = ('[Hidden] Current roles: [Seer, Villager, Wolf]\n'
                    '          Center cards: [Robber]\n')
        assert captured == expected
