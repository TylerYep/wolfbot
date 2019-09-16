''' insomniac_test.py '''
from src import const
from src.statements import Statement
from src.roles.village import Insomniac

class TestInsomniac:
    def test_constructor(self):
        ''' Should initialize a Insomniac. '''
        player_index = 1
        game_roles = ['Insomniac', 'Robber', 'Villager']
        expected = [Statement("I am a Insomniac and when I woke up I was a Robber. " + \
                              "I don't know who I switched with.", [(1, {'Insomniac'})],
                              [], 'Insomniac')]

        insomniac = Insomniac(player_index, game_roles, [])

        assert insomniac.new_role == 'Robber'
        assert insomniac.statements == expected

    def test_get_insomniac_statements(self):
        ''' Should execute initialization actions and return the possible statements. '''
        player_index = 0
        expected = [Statement("I am a Insomniac and when I woke up I was a Hunter. " + \
                              "I don't know who I switched with.", [(0, {'Insomniac'})],
                              [], 'Insomniac')]

        result = Insomniac.get_insomniac_statements(player_index, 'Hunter')

        assert result == expected

    def test_get_all_statements(self):
        ''' Should return the possible statements from all possible initialization actions. '''
        player_index = 2
        const.ROLE_SET = set(['Wolf', 'Insomniac', 'Seer'])
        expected = [Statement("I am a Insomniac and when I woke up I was a Wolf. I don't know " + \
                              "who I switched with.", [(2, {'Insomniac'})], [], 'Insomniac'),
                    Statement("I am a Insomniac and when I woke up I was a Insomniac.",
                              [(2, {'Insomniac'})], [], 'Insomniac'),
                    Statement("I am a Insomniac and when I woke up I was a Seer. I don't know " + \
                              "who I switched with.", [(2, {'Insomniac'})], [], 'Insomniac')]

        result = Insomniac.get_all_statements(player_index)

        assert set(result) == set(expected)