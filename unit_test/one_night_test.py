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

    # @staticmethod
    # def test_one_night_medium(caplog, example_medium_game_result):
    #     ''' Correctly play one round of one night werewolf. '''
    #     const.REPLAY_FILE = 'unit_test/test_data/replay.json'
    #
    #     result = one_night.play_one_night_werewolf()
    #
    #     assert result == example_medium_game_result
    #     captured = tuple(map(lambda x: x.getMessage(), caplog.records))
    #     with open('unit_test/test_data/one_night_medium.out') as output_file:
    #         expected = output_file.read().split('\n')
    #         assert '\n'.join(captured) == '\n'.join(expected)

    # @staticmethod
    # def test_one_night_large(caplog, example_large_game_result):
    #     ''' Correctly play one round of one night werewolf. '''
    #     const.REPLAY_FILE = 'unit_test/test_data/replay.json'
    #
    #     result = one_night.play_one_night_werewolf()
    #
    #     assert result == example_large_game_result
    #     captured = list(map(lambda x: x.getMessage(), caplog.records))
    #     with open('unit_test/test_data/one_night_large.out') as output_file:
    #         expected = output_file.read().split('\n')
    #         assert '\n'.join(captured) == '\n'.join(expected)
