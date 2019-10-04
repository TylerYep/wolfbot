''' stats_test.py '''
from src import stats, const

class TestSavedGame:
    pass

class TestGameResult:
    def test_constructor(self):
        ''' Should initialize using the given sentence and knowledge. '''
        result = stats.GameResult(['Wolf'], ['Wolf'], [0], 'Werewolf')

        assert isinstance(result, stats.GameResult)

    # def test_json_repr(self, example_game_result):
    #     ''' Should convert a GameResult into a dict with all of its fields. '''
    #     result = example_game_result.json_repr()
    #
    #     assert result == {'type': 'GameResult',
    #                       'sentence': 'test',
    #                       'knowledge': ((2, {'Robber'}), (0, {'Seer'})),
    #                       'switches': ((const.ROBBER_PRIORITY, 2, 0),),
    #                       'speaker': 'Robber'}
    #
    # def test_repr(self, example_game_result):
    #     ''' Should convert a GameResult into a string with all useful fields. '''
    #     expected = "GameResult(\"test\", [(2, {'Robber'}), (0, {'Seer'})], [(1, 2, 0)], 'Robber')"
    #
    #     result = str(example_game_result)
    #
    #     assert result == expected
    #
    # def test_eq(self, example_statement):
    #     ''' Should declare two Statements with identical fields to be equal. '''
    #     not_a_statement = 'hello'
    #
    #     result = statements.Statement('test',
    #                                   [(2, {'Robber'}), (0, {'Seer'})],
    #                                   [(const.ROBBER_PRIORITY, 2, 0)])
    #
    #     assert result == example_statement
    #     with pytest.raises(AssertionError):
    #         if example_statement != not_a_statement:
    #             print("Should throw an exception when trying to compare Statement to another type.")
    #
    # def test_hash(self, example_statement):
    #     ''' Should give two Statements with identical fields the same hash. '''
    #     identical_statement = statements.Statement('test',
    #                                                [(2, {'Robber'}), (0, {'Seer'})],
    #                                                [(const.ROBBER_PRIORITY, 2, 0)])
    #
    #     result = set([identical_statement, example_statement])
    #
    #     assert result == set([example_statement])
