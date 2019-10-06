''' stats_test.py '''
import pytest

from src import stats, const
from src.statements import Statement
from src.roles import Villager, Robber, Seer

class TestSavedGame:
    @staticmethod
    def test_constructor():
        ''' Should initialize correctly. '''
        villager_statement = Statement("I am a Villager.", [(0, {'Villager'})], [], 'Villager')

        result = stats.SavedGame(('Villager'), ['Villager'], [villager_statement], [Villager(0)])

        assert isinstance(result, stats.SavedGame)

    @staticmethod
    def test_json_repr(example_small_saved_game):
        ''' Should convert a SavedGame into a dict with all of its fields. '''
        result = example_small_saved_game.json_repr()

        assert result == {'all_statements':
                          [Statement("I am a Villager.", [(0, {'Villager'})], [], 'Villager'),
                           Statement("I am a Robber and I swapped with Player 2. I am now a Seer.",
                                     [(1, {'Robber'}), (2, {'Seer'})], [(1, 1, 2)], 'Robber'),
                           Statement("I am a Seer and I saw that Player 1 was a Robber.",
                                     [(2, {'Seer'}), (1, {'Robber'})], [], 'Seer')],
                          'game_roles': ['Villager', 'Seer', 'Robber'],
                          'original_roles': ('Villager', 'Robber', 'Seer'),
                          'player_objs': [Villager(0), Robber(1, 2, 'Seer'),
                                          Seer(2, (1, 'Robber'), (None, None))],
                          'type': 'SavedGame'}

    @staticmethod
    def test_repr(example_small_saved_game):
        ''' Should convert a SavedGame into a string with all useful fields. '''
        expected = ("SavedGame(('Villager', 'Robber', 'Seer'), ['Villager', 'Seer', 'Robber'], "
                    "[Statement(\"I am a Villager.\", [(0, {'Villager'})], [], 'Villager'), "
                    "Statement(\"I am a Robber and I swapped with Player 2. I am now a Seer.\", "
                    "[(1, {'Robber'}), (2, {'Seer'})], [(1, 1, 2)], 'Robber'), Statement(\"I am a "
                    "Seer and I saw that Player 1 was a Robber.\", [(2, {'Seer'}), (1, {'Robber'})]"
                    ", [], 'Seer')], [Villager(0), Robber(1, 2, Seer), Seer(2, (1, 'Robber'), "
                    "(None, None))])")

        result = str(example_small_saved_game)

        assert result == expected

    @staticmethod
    def test_eq(example_small_saved_game):
        ''' Should declare two SavedGames with identical fields to be equal. '''
        not_a_saved_game = 'hello'

        result = stats.SavedGame(
            ('Villager', 'Robber', 'Seer'),
            ['Villager', 'Seer', 'Robber'],
            [Statement("I am a Villager.", [(0, {'Villager'})], [], 'Villager'),
             Statement("I am a Robber and I swapped with Player 2. I am now a Seer.",
                       [(1, {'Robber'}), (2, {'Seer'})], [(1, 1, 2)], 'Robber'),
             Statement("I am a Seer and I saw that Player 1 was a Robber.",
                       [(2, {'Seer'}), (1, {'Robber'})], [], 'Seer')],
            [Villager(0), Robber(1, 2, 'Seer'), Seer(2, (1, 'Robber'), (None, None))])

        assert result == example_small_saved_game
        with pytest.raises(AssertionError):
            if example_small_saved_game != not_a_saved_game:
                print("Should throw an exception if trying to compare SavedGame to another type.")


class TestGameResult:
    @staticmethod
    def test_constructor():
        ''' Should initialize correctly. '''
        result = stats.GameResult(['Wolf'], ['Wolf'], [0], 'Werewolf')

        assert isinstance(result, stats.GameResult)

    @staticmethod
    def test_json_repr(example_small_game_result):
        ''' Should convert a GameResult into a dict with all of its fields. '''
        result = example_small_game_result.json_repr()

        assert result == {'actual': ['Villager', 'Seer', 'Robber'],
                          'guessed': ['Villager', 'Seer', 'Robber'],
                          'type': 'GameResult',
                          'winning_team': 'Villager',
                          'wolf_inds': []}

    @staticmethod
    def test_repr(example_small_game_result):
        ''' Should convert a GameResult into a string with all useful fields. '''
        expected = "GameResult(['Villager', 'Seer', 'Robber'], " \
                 + "['Villager', 'Seer', 'Robber'], [], Villager)"

        result = str(example_small_game_result)

        assert result == expected

    @staticmethod
    def test_eq(example_small_game_result):
        ''' Should declare two GameResults with identical fields to be equal. '''
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
    @staticmethod
    def test_constructor():
        ''' Should initialize correctly. '''
        pass

    @staticmethod
    def test_add_result():
        ''' Should initialize correctly. '''
        pass

    @staticmethod
    def test_print_statistics():
        ''' Should initialize correctly. '''
        pass
