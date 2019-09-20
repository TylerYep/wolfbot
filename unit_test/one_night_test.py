''' one_night_test.py '''
from src import one_night, const

class TestPlayOneNightWerewolf:
    def test_play_one_night_werewolf_result(self, medium_game_roles):
        ''' Correctly swap two players. '''
        const.ROLES = medium_game_roles
        const.REPLAY_FILE = 'unit_test/test_data/replay.json'

        result = one_night.play_one_night_werewolf()

        assert result.actual == ['Seer', 'Wolf', 'Troublemaker', 'Drunk', 'Minion', 'Robber']
        # TODO make this deterministic.
        assert result.guessed == ['Robber', 'Seer', 'Troublemaker', 'Minion', 'Wolf', 'Drunk'] or \
               result.guessed == ['Robber', 'Seer', 'Troublemaker', 'Wolf', 'Minion', 'Drunk']
        assert result.wolf_inds

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
