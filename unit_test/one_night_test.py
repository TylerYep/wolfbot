''' one_night_test.py '''
from src import one_night, const

class TestPlayOneNightWerewolf:
    def test_play_one_night_werewolf_result(self, medium_game_roles):
        ''' Correctly play one round of one night werewolf. '''
        const.ROLES = medium_game_roles
        const.REPLAY_FILE = 'unit_test/test_data/replay.json'

        result = one_night.play_one_night_werewolf()

        assert result.actual == ['Seer', 'Wolf', 'Troublemaker', 'Drunk', 'Minion', 'Robber']
        assert result.guessed == ['Robber', 'Seer', 'Minion', 'Troublemaker', 'Wolf', 'Drunk']
        assert result.wolf_inds == [1]
        # TODO compare the entire object instead?

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
