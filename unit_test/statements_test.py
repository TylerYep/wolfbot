''' statements_test.py '''
import pytest

from src import statements, const

class TestStatement:
    def test_constructor(self):
        ''' Should initialize using the given sentence and knowledge. '''
        result = statements.Statement('test', [(1, {'Villager'})])

        assert isinstance(result, statements.Statement)
        assert result.sentence == 'test'

    def test_negate(self, large_game_roles, example_statement):
        ''' Negated statements only contain the speaker and the opposite of the first clause. '''
        const.ROLES = large_game_roles
        expected = statements.Statement('NOT - test',
                                        [(2, set(const.ROLES) - {'Robber'})],
                                        speaker='Robber')

        result = example_statement.negate()

        assert isinstance(result, statements.Statement)
        assert str(result) == str(expected)

    def test_negate_all(self, large_game_roles, example_statement):
        ''' Negate-all statements contain the opposite of all clauses. '''
        const.ROLES = large_game_roles
        expected = statements.Statement('NOT - test',
                                        [(2, set(const.ROLES) - {'Robber'}),
                                         (0, set(const.ROLES) - {'Seer'})],
                                        speaker='Robber')

        result = example_statement.negate_all()

        assert isinstance(result, statements.Statement)
        assert str(result) == str(expected)

    def test_json_repr(self, example_statement):
        ''' Should convert a Statement into a dict with all of its fields. '''
        result = example_statement.json_repr()

        assert result == {'type': 'Statement',
                          'sentence': 'test',
                          'knowledge': ((2, {'Robber'}), (0, {'Seer'})),
                          'switches': ((const.ROBBER_PRIORITY, 2, 0),),
                          'speaker': 'Robber'}

    def test_repr(self, example_statement):
        ''' Should convert a Statement into a string with all useful fields. '''
        expected = "Statement(\"test\", [(2, {'Robber'}), (0, {'Seer'})], [(1, 2, 0)], 'Robber')"

        result = str(example_statement)

        assert result == expected

    def test_eq(self, example_statement):
        ''' Should declare two Statements with identical fields to be equal. '''
        not_a_statement = 'hello'

        result = statements.Statement('test',
                                      [(2, {'Robber'}), (0, {'Seer'})],
                                      [(const.ROBBER_PRIORITY, 2, 0)])

        assert result == example_statement
        with pytest.raises(AssertionError):
            if example_statement != not_a_statement:
                print("Should throw an exception when trying to compare Statement to another type.")

    def test_hash(self, example_statement):
        ''' Should give two Statements with identical fields the same hash. '''
        identical_statement = statements.Statement('test',
                                                   [(2, {'Robber'}), (0, {'Seer'})],
                                                   [(const.ROBBER_PRIORITY, 2, 0)])

        result = set([identical_statement, example_statement])

        assert result == set([example_statement])
