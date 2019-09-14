''' player_test.py '''
import logging

from src import const
from src.statements import Statement
from src.roles.village import Player, Robber, Villager

class TestPlayer:
    def test_constructor(self):
        player_index = 5

        empty_player = Player(player_index)

        assert empty_player.role == 'Player'
        assert empty_player.statements == []

    def test_inheritance(self):
        const.logger.setLevel(logging.WARNING)
        const.ROLES = ('Wolf', 'Villager', 'Robber', 'Villager', 'Wolf')
        roles = list(const.ROLES)

        robber = Robber(2, roles, roles)

        assert robber.new_role == 'Villager'
        assert not robber.is_user

    def test_get_statement_inheritance(self):
        villager = Villager(0, [], [])

        statement = villager.get_statement([], [])

        assert statement == Statement('I am a Villager.', [(0, {'Villager'})])

    def test_json_repr(self):
        pass

    def test_repr(self):
        pass
