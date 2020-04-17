""" mason.py """
from typing import Dict, List

from src import const, util
from src.const import logger
from src.statements import Statement

from ..player import Player


class Mason(Player):
    """ Mason Player class. """

    def __init__(self, player_index: int, mason_indices: List[int]):
        super().__init__(player_index)
        self.mason_indices = mason_indices
        self.statements = self.get_mason_statements(player_index, mason_indices)

    @classmethod
    def awake_init(cls, player_index: int, game_roles: List[str], original_roles: List[str]):
        """ Initializes Mason - sees all other Masons. """
        del game_roles
        is_user = const.IS_USER[player_index]
        mason_indices = util.find_all_player_indices(original_roles, "Mason")
        assert player_index in mason_indices
        logger.debug(f"[Hidden] Masons are at indices: {mason_indices}")
        if is_user:
            logger.info(f"Masons are players: {mason_indices} (You are player {player_index})")
        return cls(player_index, mason_indices)

    @staticmethod
    def get_mason_statements(player_index: int, mason_indices: List[int]) -> List[Statement]:
        """ Gets Mason Statement. """
        assert player_index in mason_indices
        if len(mason_indices) == 1:
            sentence = "I am a Mason. The other Mason is not present."
            knowledge = [(player_index, {"Mason"})]
            for ind in range(const.NUM_PLAYERS):
                if ind != player_index:
                    knowledge.append((ind, set(const.ROLE_SET) - {"Mason"}))
        else:
            other_mason = mason_indices[0] if mason_indices[0] != player_index else mason_indices[1]
            sentence = f"I am a Mason. The other Mason is Player {other_mason}."
            knowledge = [(player_index, {"Mason"}), (other_mason, {"Mason"})]
        return [Statement(sentence, knowledge)]

    @staticmethod
    def get_all_statements(player_index: int) -> List[Statement]:
        """ Required for all player types. Returns all possible role statements. """
        statements = Mason.get_mason_statements(player_index, [player_index])
        for i in range(const.NUM_PLAYERS):
            if player_index != i:
                mason_indices = [player_index, i]
                statements += Mason.get_mason_statements(player_index, mason_indices)
        return statements

    def json_repr(self) -> Dict:
        """ Gets JSON representation of a Mason player. """
        return {
            "type": self.role,
            "player_index": self.player_index,
            "mason_indices": self.mason_indices,
        }
