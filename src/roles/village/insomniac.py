""" insomniac.py """
from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

from overrides import overrides

from src import const
from src.const import logger
from src.roles.player import Player
from src.statements import KnowledgeBase, Statement


class Insomniac(Player):
    """ Insomniac Player class. """

    def __init__(self, player_index: int, new_role: str):
        super().__init__(player_index)
        self.new_role = new_role
        self.statements += self.get_insomniac_statements(player_index, new_role)

    @classmethod
    @overrides
    def awake_init(
        cls, player_index: int, game_roles: List[str], original_roles: List[str]
    ) -> Insomniac:
        """ Initializes Insomniac - learns new role. """
        del original_roles
        is_user = const.IS_USER[player_index]
        insomniac_new_role = game_roles[player_index]
        logger.debug(f"[Hidden] Insomniac wakes up as a {insomniac_new_role}.")
        if is_user:
            logger.info(f"You woke up as a {insomniac_new_role}!", cache=True)
        return cls(player_index, insomniac_new_role)

    @staticmethod
    def get_insomniac_statements(
        player_index: int, insomniac_new_role: str, new_insomniac_index: Optional[int] = None
    ) -> Tuple[Statement, ...]:
        """ Gets Insomniac Statement. """
        knowledge = ((player_index, frozenset({"Insomniac"})),)
        sentence = f"I am a Insomniac and when I woke up I was a {insomniac_new_role}."
        if new_insomniac_index is None:
            if insomniac_new_role != "Insomniac":
                sentence += " I don't know who I switched with."
        else:
            sentence += f" I switched with Player {new_insomniac_index}."
        # switches = ((player_index, new_insomniac_index),)  # TODO
        return (Statement(sentence, knowledge),)

    @staticmethod
    @overrides
    def get_all_statements(player_index: int) -> Tuple[Statement, ...]:
        """ Required for all player types. Returns all possible role statements. """
        statements: List[Statement] = []
        for role in const.SORTED_ROLE_SET:
            statements += Insomniac.get_insomniac_statements(player_index, role)
        return tuple(statements)

    @overrides
    def analyze(self, knowledge_base: KnowledgeBase) -> None:
        """ Overrides analyze. """
        possible_switches: List[int] = []
        for i, stated_role in enumerate(knowledge_base.stated_roles):
            if stated_role == self.new_role:
                possible_switches.append(i)
        if len(possible_switches) == 1:  # TODO how to handle multiple possible switches
            self.statements += self.get_insomniac_statements(
                self.player_index, self.new_role, possible_switches[0]
            )

    @overrides
    def json_repr(self) -> Dict[str, Any]:
        """ Gets JSON representation of an Insomniac player. """
        json_dict = super().json_repr()
        json_dict.update({"new_role": self.new_role})
        return json_dict
