''' statements_test.py '''
import pytest

from src import statements, const
from src.const import Priority

class TestStatement:
    ''' Tests for the Statement class. '''

    @staticmethod
    def test_constructor():
        ''' Should initialize using the given sentence and knowledge. '''
        result = statements.Statement('test', [(1, {'Villager'})])

        assert isinstance(result, statements.Statement)
        assert result.sentence == 'test'
        assert result.knowledge == ((1, frozenset({'Villager'})),)
        assert result.switches == ()
        assert result.speaker == 'Villager'

    @staticmethod
    def test_negate(large_game_roles, example_statement):
        ''' Negated statements only contain the speaker and the opposite of the first clause. '''
        const.ROLES = large_game_roles
        expected = statements.Statement('NOT - test',
                                        [(2, const.ROLE_SET - {'Robber'})],
                                        speaker='Robber')

        result = example_statement.negate()

        assert isinstance(result, statements.Statement)
        assert str(result) == str(expected)

    @staticmethod
    def test_negate_all(large_game_roles, example_statement):
        ''' Negate-all statements contain the opposite of all clauses. '''
        const.ROLES = large_game_roles
        expected = statements.Statement('NOT - test',
                                        [(2, const.ROLE_SET - {'Robber'}),
                                         (0, const.ROLE_SET - {'Seer'})],
                                        speaker='Robber')

        result = example_statement.negate_all()

        assert isinstance(result, statements.Statement)
        assert str(result) == str(expected)

    @staticmethod
    def test_json_repr(example_statement):
        ''' Should convert a Statement into a dict with all of its fields. '''
        result = example_statement.json_repr()

        assert result == {'type': 'Statement',
                          'sentence': 'test',
                          'knowledge': ((2, {'Robber'}), (0, {'Seer'})),
                          'switches': ((Priority.ROBBER, 2, 0),),
                          'speaker': 'Robber'}

    @staticmethod
    def test_repr(example_statement):
        ''' Should convert a Statement into a string with all useful fields. '''
        expected = ("Statement(\"test\", [(2, {'Robber'}), (0, {'Seer'})], "
                    "[(<Priority.ROBBER: 1>, 2, 0)], 'Robber')")

        result = str(example_statement)

        assert result == expected

    @staticmethod
    def test_eq(example_statement):
        ''' Should declare two Statements with identical fields to be equal. '''
        not_a_statement = 'hello'

        result = statements.Statement('test',
                                      [(2, {'Robber'}), (0, {'Seer'})],
                                      [(Priority.ROBBER, 2, 0)])

        assert result == example_statement
        with pytest.raises(AssertionError):
            if example_statement != not_a_statement:
                print("Should throw an exception when trying to compare Statement to another type.")

    @staticmethod
    def test_hash(example_statement):
        ''' Should give two Statements with identical fields the same hash. '''
        identical_statement = statements.Statement('test',
                                                   [(2, {'Robber'}), (0, {'Seer'})],
                                                   [(Priority.ROBBER, 2, 0)])

        result = set([identical_statement, example_statement])

        assert result == set([example_statement])
