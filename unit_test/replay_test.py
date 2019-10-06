''' replay_test.py '''
from src import replay, const, one_night

class TestReplay:
    @staticmethod
    def test_replay_game_small(example_small_game_result):
        const.REPLAY_FILE = 'unit_test/test_data/replay.json'
        one_night.play_one_night_werewolf()

        replay.replay_game()

        assert example_small_game_result # TODO

    @staticmethod
    def test_replay_game_medium(example_medium_game_result):
        const.REPLAY_FILE = 'unit_test/test_data/replay.json'
        one_night.play_one_night_werewolf()

        replay.replay_game()

        assert example_medium_game_result # TODO

    # @staticmethod
    # def test_replay_game_large(example_large_game_result):
    #     const.REPLAY_FILE = 'unit_test/test_data/replay.json'
    #     one_night.play_one_night_werewolf()
    #
    #     replay.replay_game()
    #
    #     assert example_large_game_result # TODO
