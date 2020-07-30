""" mason.py """
from __future__ import annotations

from typing import Any, Dict, List, Tuple

from src import const, util
from src.const import logger, lru_cache
from src.roles.player import Player
from src.statements import Statement


class Mason(Player):
    """ Mason Player class. """

    def __init__(self, player_index: int, mason_indices: Tuple[int, ...]):
        super().__init__(player_index)
        self.mason_indices = mason_indices
        self.statements += self.get_mason_statements(player_index, mason_indices)

    @classmethod
    def awake_init(
        cls, player_index: int, game_roles: List[str], original_roles: Tuple[str, ...]
    ) -> Mason:
        """ Initializes Mason - sees all other Masons. """
        del game_roles
        is_user = const.IS_USER[player_index]
        mason_indices = util.find_all_player_indices(original_roles, "Mason")
        assert player_index in mason_indices
        assert len(mason_indices) <= 2
        logger.debug(f"[Hidden] Masons are at indices: {list(mason_indices)}")
        if is_user:
            logger.info(
                f"Masons are players: {list(mason_indices)} (You are player {player_index})",
                cache=True,
            )
        return cls(player_index, mason_indices)

    @staticmethod
    @lru_cache
    def get_mason_statements(
        player_index: int, mason_indices: Tuple[int, ...]
    ) -> Tuple[Statement, ...]:
        """ Gets Mason Statement. """
        assert player_index in mason_indices
        if len(mason_indices) == 1:
            sentence = "I am a Mason. The other Mason is not present."
            knowledge = [(player_index, frozenset({"Mason"}))]
            for ind in range(const.NUM_PLAYERS):
                if ind != player_index:
                    knowledge.append((ind, const.ROLE_SET - frozenset({"Mason"})))
        else:
            other_mason = mason_indices[0] if mason_indices[0] != player_index else mason_indices[1]
            sentence = f"I am a Mason. The other Mason is Player {other_mason}."
            knowledge = [(player_index, frozenset({"Mason"})), (other_mason, frozenset({"Mason"}))]
        return (Statement(sentence, tuple(knowledge)),)

    @staticmethod
    @lru_cache
    def get_all_statements(player_index: int) -> Tuple[Statement, ...]:
        """ Required for all player types. Returns all possible role statements. """
        statements = Mason.get_mason_statements(player_index, (player_index,))
        for i in range(const.NUM_PLAYERS):
            if player_index != i:
                mason_indices = (player_index, i)
                statements += Mason.get_mason_statements(player_index, mason_indices)
        return statements

    def json_repr(self) -> Dict[str, Any]:
        """ Gets JSON representation of a Mason player. """
        json_dict = super().json_repr()
        json_dict.update({"mason_indices": self.mason_indices})
        return json_dict
