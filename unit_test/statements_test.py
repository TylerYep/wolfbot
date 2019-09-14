''' statements_test.py '''
import pytest

from src import statements, const
from fixtures import large_game_roles

STATEMENT = statements.Statement('test',
                                 [(2, {'Robber'}), (0, {'Seer'})],
                                 [(0, 2, const.ROBBER_PRIORITY)])

class TestStatement:
    def test_constructor(self):
        statement = statements.Statement('test', [(1, {'Villager'})])
        assert isinstance(statement, statements.Statement)

    def test_negate(self):
        const.ROLES = large_game_roles()
        expected = statements.Statement('NOT - test',
                                        [(2, set(const.ROLES) - {'Robber'})],
                                        speaker='Robber')

        result = STATEMENT.negate()

        assert isinstance(result, statements.Statement)
        assert str(result) == str(expected)

    def test_negate_all(self):
        const.ROLES = large_game_roles()
        expected = statements.Statement('NOT - test',
                                        [(2, set(const.ROLES) - {'Robber'}),
                                         (0, set(const.ROLES) - {'Seer'})],
                                        speaker='Robber')

        result = STATEMENT.negate_all()

        assert isinstance(result, statements.Statement)
        assert str(result) == str(expected)

    def test_json_repr(self):
        result = STATEMENT.json_repr()

        assert result == {'type': 'Statement',
                          'sentence': 'test',
                          'knowledge': [(2, {'Robber'}), (0, {'Seer'})],
                          'switches': [(0, 2, const.ROBBER_PRIORITY)],
                          'speaker': 'Robber'}

    def test_repr(self):
        result = str(STATEMENT)
        expected = 'Statement("test", [(2, {\'Robber\'}), (0, {\'Seer\'})], [(0, 2, 1)], Robber)'

        assert result == expected

    def test_eq(self):
        not_a_statement = 'hello'
        identical_statement = statements.Statement('test',
                                                   [(2, {'Robber'}), (0, {'Seer'})],
                                                   [(0, 2, const.ROBBER_PRIORITY)])
        with pytest.raises(AssertionError):
            should_fail = STATEMENT == not_a_statement
        assert STATEMENT == identical_statement

    # def test_hash(self):
    #     identical_statement = statements.Statement('test',
    #                                                [(2, {'Robber'}), (0, {'Seer'})],
    #                                                [(0, 2, const.ROBBER_PRIORITY)])
    #
    #     statement_set = set([identical_statement, STATEMENT])
    #
    #     assert statement_set == set([STATEMENT])


