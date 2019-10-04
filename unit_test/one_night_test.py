''' one_night_test.py '''
from src import one_night, const
from src.stats import GameResult

class TestPlayOneNightWerewolf:
    def test_play_one_night_werewolf_result(self, medium_game_roles):
        ''' Correctly play one round of one night werewolf. '''
        const.ROLES = medium_game_roles
        const.REPLAY_FILE = 'unit_test/test_data/replay.json'
        expected = GameResult(['Seer', 'Wolf', 'Troublemaker', 'Drunk', 'Minion', 'Robber'],
                              ['Robber', 'Seer', 'Minion', 'Troublemaker', 'Wolf', 'Drunk'],
                              [1],
                              'Werewolf')

        result = one_night.play_one_night_werewolf()

        assert result == expected

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
