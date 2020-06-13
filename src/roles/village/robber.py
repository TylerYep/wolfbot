""" robber.py """
from __future__ import annotations

from typing import Any, Dict, List

from src import const, util
from src.const import SwitchPriority, logger
from src.statements import Statement

from ..player import Player


class Robber(Player):
    """ Robber Player class. """

    def __init__(self, player_index: int, choice_ind: int, new_role: str):
        super().__init__(player_index)
        self.choice_ind = choice_ind
        self.new_role = new_role
        self.statements += self.get_robber_statements(player_index, choice_ind, new_role)

    @classmethod
    def awake_init(
        cls, player_index: int, game_roles: List[str], original_roles: List[str]
    ) -> Robber:
        """ Initializes Robber - switches roles with another player. """
        del original_roles
        assert const.NUM_PLAYERS > 1
        is_user = const.IS_USER[player_index]
        choice_ind = util.get_player(is_user, (player_index,))
        choice_char = game_roles[choice_ind]
        logger.debug(
            f"[Hidden] Robber switches with Player {choice_ind} and becomes a {choice_char}."
        )
        if is_user:
            logger.info(
                f"You switched with Player {choice_ind} and are now a {choice_char}!", cache=True
            )
        util.swap_characters(game_roles, player_index, choice_ind)
        return cls(player_index, choice_ind, choice_char)

    @staticmethod
    def get_robber_statements(
        player_index: int, choice_ind: int, choice_char: str
    ) -> List[Statement]:
        """ Gets Robber Statement. """
        sentence = (
            f"I am a Robber and I swapped with Player {choice_ind}. I am now a {choice_char}."
        )
        knowledge = ((player_index, frozenset({"Robber"})), (choice_ind, frozenset({choice_char})))
        switches = ((SwitchPriority.ROBBER, player_index, choice_ind),)
        return [Statement(sentence, knowledge, switches)]

    @staticmethod
    def get_all_statements(player_index: int) -> List[Statement]:
        """ Required for all player types. Returns all possible role statements. """
        statements: List[Statement] = []
        for i in range(const.NUM_PLAYERS):
            for role in const.SORTED_ROLE_SET:
                if player_index != i:  # OK: 'I robbed Player 0 and now I'm a Wolf... ;)'
                    statements += Robber.get_robber_statements(player_index, i, role)
        return statements

    def get_statement(self, stated_roles: List[str], previous: List[Statement]) -> Statement:
        """ Overrides get_statement when the Robber becomes a Wolf. """
        if self.new_role != "" and self.new_role in const.EVIL_ROLES:
            return self.transform(self.new_role).get_statement(stated_roles, previous)

        return super().get_statement(stated_roles, previous)

    def json_repr(self) -> Dict[str, Any]:
        """ Gets JSON representation of a Robber player. """
        json_dict = super().json_repr()
        json_dict.update({"choice_ind": self.choice_ind, "new_role": self.new_role})
        return json_dict
