''' statements_test.py '''
from src import statements, const
from fixtures import large_game_roles

class TestStatement:
    def test_constructor(self):
        result = statements.Statement('test', [(2, {'Robber'})], [(0, 2, const.ROBBER_PRIORITY)])

        assert isinstance(result, statements.Statement)
        assert str(result) == 'Statement("test", [(2, {\'Robber\'})], [(0, 2, 1)], Robber)'

    def test_negate(self):
        const.ROLES = large_game_roles()
        statement = statements.Statement('test', [(2, {'Robber'})], [(0, 2, const.ROBBER_PRIORITY)])
        expected = statements.Statement('NOT - test',
                                        [(2, set(const.ROLES) - {'Robber'})],
                                        None,
                                        'Robber')

        result = statement.negate()

        assert isinstance(result, statements.Statement)
        assert str(result) == str(expected)

