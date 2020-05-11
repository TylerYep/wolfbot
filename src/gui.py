""" gui.py """
import os
import random
from typing import List, Tuple

from src import const
from src.const import logger
from src.statements import Statement


class GUIState:
    """ If INTERACTIVE_MODE_ON is False, all actions are no-ops. """

    def __init__(self) -> None:
        self.disable_gui = not const.INTERACTIVE_MODE_ON
        self.output_cache: List[str] = []

    def print_cache(self) -> None:
        """ Clears console and then output all lines stored in the logging cache. """
        os.system("clear")
        for line in self.output_cache:
            logger.info(line)

    def intro(self, original_roles: Tuple[str, ...]) -> None:
        """ Tells the player what their assigned role is. """
        if self.disable_gui:
            return
        user_index = random.randint(0, const.NUM_PLAYERS - 1)
        const.IS_USER[user_index] = True
        first_line = f"Player {user_index}, you are a {original_roles[user_index]}!"
        self.output_cache.append(first_line)
        self.print_cache()

    def night_falls(self) -> None:
        """ Clears the output except for the player's role. """
        if self.disable_gui:
            return
        self.print_cache()

    def print_statements(self, all_statements: List[Statement]) -> None:
        """ Prints all statements that have been said so far. """
        if self.disable_gui:
            return
        self.output_cache.append("\n-- GAME BEGINS --\n")
        for j, statement in enumerate(all_statements):
            self.output_cache.append(f"Player {j}: {statement.sentence}")
        self.print_cache()
