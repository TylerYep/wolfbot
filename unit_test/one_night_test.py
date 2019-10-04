''' one_night_test.py '''
from src import one_night, const

class TestPlayOneNightWerewolf:
    def test_play_one_night_werewolf_small(self, example_small_game_result):
        ''' Correctly play one round of one night werewolf. '''
        const.REPLAY_FILE = 'unit_test/test_data/replay.json'

        result = one_night.play_one_night_werewolf()

        assert result == example_small_game_result

    def test_play_one_night_werewolf_medium(self, example_medium_game_result):
        ''' Correctly play one round of one night werewolf. '''
        const.REPLAY_FILE = 'unit_test/test_data/replay.json'

        result = one_night.play_one_night_werewolf()

        assert result == example_medium_game_result

    # def test_play_one_night_werewolf_large(self, example_large_game_result):
    #     ''' Correctly play one round of one night werewolf. '''
    #     const.REPLAY_FILE = 'unit_test/test_data/replay.json'
    #
    #     result = one_night.play_one_night_werewolf()
    #
    #     assert result == example_large_game_result

    # def test_play_one_night_werewolf_output(self, caplog, medium_game_roles):
    #     ''' Correctly swap two players. '''
    #     const.ROLES = medium_game_roles
    #     const.REPLAY_FILE = 'unit_test/test_data/replay.json'
    #
    #     one_night.play_one_night_werewolf()
    #
    #     captured = list(map(lambda x: x.getMessage(), caplog.records))
    #     with open('unit_test/test_data/one_night.out') as output_file:
    #         expected = output_file.read().split('\n')
    #         assert '\n'.join(captured) == '\n'.join(expected)
