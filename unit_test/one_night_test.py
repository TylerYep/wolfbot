''' one_night_test.py '''
from src import one_night, const
from src.stats import GameResult

class TestPlayOneNightWerewolf:
    def test_play_one_night_werewolf(self, medium_game_roles):
        ''' Correctly swap two players. '''
        const.ROLES = medium_game_roles
        const.REPLAY_FILE = 'unit_test/test_data/replay.json'

        result = one_night.play_one_night_werewolf()

        assert result.actual == ['Seer', 'Wolf', 'Troublemaker', 'Drunk', 'Minion', 'Robber']
        assert result.guessed == ['Robber', 'Seer', 'Troublemaker', 'Minion', 'Wolf', 'Drunk'] or \
               result.guessed == ['Robber', 'Seer', 'Troublemaker', 'Wolf', 'Minion', 'Drunk']