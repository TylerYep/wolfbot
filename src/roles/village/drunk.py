""" drunk.py """
from __future__ import annotations

from typing import Any, Dict, List, Tuple

from overrides import overrides

from src import const, util
from src.const import SwitchPriority, logger, lru_cache
from src.roles.player import Player
from src.statements import Statement


class Drunk(Player):
    """ Drunk Player class. """

    def __init__(self, player_index: int, choice_ind: int):
        super().__init__(player_index)
        self.choice_ind = choice_ind
        self.statements += self.get_drunk_statements(player_index, choice_ind)

    @classmethod
    @overrides
    def awake_init(
        cls, player_index: int, game_roles: List[str], original_roles: List[str]
    ) -> Drunk:
        """ Initializes Drunk - switches with a card in the center. """
        del original_roles
        assert const.NUM_CENTER > 0
        is_user = const.IS_USER[player_index]
        choice_ind = util.get_center(is_user)
        logger.debug(
            f"[Hidden] Drunk switches with Center Card {choice_ind - const.NUM_PLAYERS}"
            f" and unknowingly becomes a {game_roles[choice_ind]}."
        )
        if is_user:
            logger.info("You do not know your new role.", cache=True)
        util.swap_characters(game_roles, player_index, choice_ind)
        return cls(player_index, choice_ind)

    @staticmethod
    @lru_cache
    def get_drunk_statements(player_index: int, choice_ind: int) -> Tuple[Statement, ...]:
        """ Gets Drunk Statement. """
        sentence = f"I am a Drunk and I swapped with Center {choice_ind - const.NUM_PLAYERS}."
        knowledge = ((player_index, frozenset({"Drunk"})),)
        switches = ((SwitchPriority.DRUNK, player_index, choice_ind),)
        return (Statement(sentence, knowledge, switches),)

    @staticmethod
    @lru_cache
    @overrides
    def get_all_statements(player_index: int) -> Tuple[Statement, ...]:
        """ Required for all player types. Returns all possible role statements. """
        statements: Tuple[Statement, ...] = ()
        for k in range(const.NUM_CENTER):
            statements += Drunk.get_drunk_statements(player_index, const.NUM_PLAYERS + k)
        return statements

    @overrides
    def json_repr(self) -> Dict[str, Any]:
        """ Gets JSON representation of a Drunk player. """
        json_dict = super().json_repr()
        json_dict.update({"choice_ind": self.choice_ind})
        return json_dict
