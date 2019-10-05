''' stats_test.py '''
import pytest

from src import stats, const

class TestSavedGame:
    def test_constructor(self):
        ''' Should initialize correctly. '''
        pass
    #     result = stats.SavedGame()
    #
    #     assert isinstance(result, stats.GameResult)
    #
    # def test_json_repr(self, example_small_game_result):
    #     ''' Should convert a GameResult into a dict with all of its fields. '''
    #     result = example_small_game_result.json_repr()
    #
    #     assert result == {'actual': ['Villager', 'Seer', 'Robber'],
    #                       'guessed': ['Villager', 'Seer', 'Robber'],
    #                       'type': 'GameResult',
    #                       'winning_team': 'Villager',
    #                       'wolf_inds': []}
    #
    # def test_repr(self, example_small_game_result):
    #     ''' Should convert a GameResult into a string with all useful fields. '''
    #     expected = "GameResult(['Villager', 'Seer', 'Robber'], " \
    #              + "['Villager', 'Seer', 'Robber'], [], Villager)"
    #
    #     result = str(example_small_game_result)
    #
    #     assert result == expected
    #
    # def test_eq(self, example_small_game_result):
    #     ''' Should declare two Statements with identical fields to be equal. '''
    #     not_a_game_result = 'hello'
    #
    #     result = stats.GameResult(['Villager', 'Seer', 'Robber'],
    #                               ['Villager', 'Seer', 'Robber'],
    #                               [],
    #                               'Villager')
    #
    #     assert result == example_small_game_result
    #     with pytest.raises(AssertionError):
    #         if example_small_game_result != not_a_game_result:
    #             print("Should throw an exception if trying to compare GameResult to another type.")


class TestGameResult:
    def test_constructor(self):
        ''' Should initialize correctly. '''
        result = stats.GameResult(['Wolf'], ['Wolf'], [0], 'Werewolf')

        assert isinstance(result, stats.GameResult)

    def test_json_repr(self, example_small_game_result):
        ''' Should convert a GameResult into a dict with all of its fields. '''
        result = example_small_game_result.json_repr()

        assert result == {'actual': ['Villager', 'Seer', 'Robber'],
                          'guessed': ['Villager', 'Seer', 'Robber'],
                          'type': 'GameResult',
                          'winning_team': 'Villager',
                          'wolf_inds': []}

    def test_repr(self, example_small_game_result):
        ''' Should convert a GameResult into a string with all useful fields. '''
        expected = "GameResult(['Villager', 'Seer', 'Robber'], " \
                 + "['Villager', 'Seer', 'Robber'], [], Villager)"

        result = str(example_small_game_result)

        assert result == expected

    def test_eq(self, example_small_game_result):
        ''' Should declare two Statements with identical fields to be equal. '''
        not_a_game_result = 'hello'

        result = stats.GameResult(['Villager', 'Seer', 'Robber'],
                                  ['Villager', 'Seer', 'Robber'],
                                  [],
                                  'Villager')

        assert result == example_small_game_result
        with pytest.raises(AssertionError):
            if example_small_game_result != not_a_game_result:
                print("Should throw an exception if trying to compare GameResult to another type.")


class Statistics:
    def test_constructor(self):
        ''' Should initialize correctly. '''
        pass

    def test_add_result(self):
        ''' Should initialize correctly. '''
        pass

    def test_print_statistics(self):
        ''' Should initialize correctly. '''
        pass
