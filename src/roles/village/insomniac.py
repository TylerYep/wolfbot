""" insomniac.py """
from __future__ import annotations

from typing import Any, Dict, List, Optional

from src import const
from src.const import logger
from src.statements import Statement

from ..player import Player


class Insomniac(Player):
    """ Insomniac Player class. """

    def __init__(self, player_index: int, new_role: str):
        super().__init__(player_index)
        self.new_role = new_role
        self.statements += self.get_insomniac_statements(player_index, new_role)

    @classmethod
    def awake_init(
        cls, player_index: int, game_roles: List[str], original_roles: List[str]
    ) -> Insomniac:
        """ Initializes Insomniac - learns new role. """
        del original_roles
        is_user = const.IS_USER[player_index]
        insomniac_new_role = game_roles[player_index]
        logger.debug(f"[Hidden] Insomniac wakes up as a {insomniac_new_role}.")
        if is_user:
            logger.info(f"You woke up as a {insomniac_new_role}!")
        return cls(player_index, insomniac_new_role)

    @staticmethod
    def get_insomniac_statements(
        player_index: int, insomniac_new_role: str, new_insomniac_index: Optional[int] = None
    ) -> List[Statement]:
        """ Gets Insomniac Statement. """
        knowledge = ((player_index, {"Insomniac"}),)
        sentence = f"I am a Insomniac and when I woke up I was a {insomniac_new_role}."
        if new_insomniac_index is None:
            if insomniac_new_role != "Insomniac":
                sentence += " I don't know who I switched with."
        else:
            sentence += f" I switched with Player {new_insomniac_index}."
        # switches = ((player_index, new_insomniac_index),)  # TODO
        return [Statement(sentence, knowledge)]

    @staticmethod
    def get_all_statements(player_index: int) -> List[Statement]:
        """ Required for all player types. Returns all possible role statements. """
        statements: List[Statement] = []
        for role in const.SORTED_ROLE_SET:
            statements += Insomniac.get_insomniac_statements(player_index, role)
        return statements

    def get_statement(self, stated_roles: List[str], previous: List[Statement]) -> Statement:
        """ Overrides get_statement when the Insomniac becomes a Wolf. """
        if self.new_role != "Insomniac" and self.new_role in const.EVIL_ROLES:
            return self.transform(self.new_role).get_statement(stated_roles, previous)

        possible_switches: List[int] = []
        for i, stated_role in enumerate(stated_roles):
            if stated_role == self.new_role:
                possible_switches.append(i)
        if len(possible_switches) == 1:  # TODO how to handle multiple possible switches
            self.statements += self.get_insomniac_statements(
                self.player_index, self.new_role, possible_switches[0]
            )
        return super().get_statement(stated_roles, previous)

    def json_repr(self) -> Dict[str, Any]:
        """ Gets JSON representation of an Insomniac player. """
        return {"type": self.role, "player_index": self.player_index, "new_role": self.new_role}
