''' hunter_test.py '''
from src import const
from src.statements import Statement
from src.roles.village import Hunter

class TestHunter:
    def test_constructor(self):
        player_index = 5

        hunter = Hunter(player_index, [], [])  # Other params are unused.

        assert hunter.statements == [Statement('I am a Hunter.', [(5, {'Hunter'})])]

    def test_get_hunter_statements(self):
        player_index = 0

        result = Hunter.get_hunter_statements(0)

        assert result == [Statement('I am a Hunter.', [(0, {'Hunter'})])]

    def test_get_all_statements(self):
        player_index = 2

        result = Hunter.get_all_statements(2)

        assert result == [Statement('I am a Hunter.', [(2, {'Hunter'})])]