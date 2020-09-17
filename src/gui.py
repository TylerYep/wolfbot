""" gui.py """
import os
from typing import Tuple

from src import const
from src.const import Role, logger
from src.statements import Statement


class GUIState:
    """ If INTERACTIVE_MODE is False, all actions are no-ops. """

    def __init__(self) -> None:
        self.disable_gui = not const.INTERACTIVE_MODE

    @staticmethod
    def print_cache() -> None:
        """ Clears console and then output all lines stored in the logging cache. """
        os.system("clear")
        for log_level, line in logger.output_cache:
            logger.log(log_level, line)

    def intro(self, original_roles: Tuple[Role, ...]) -> None:
        """ Tells the player what their assigned role is. """
        if self.disable_gui:
            return
        input("Press Enter to continue...")
        os.system("clear")
        logger.clear()

        user_index = const.IS_USER.index(True)
        logger.info(
            f"Player {user_index}, you are a {original_roles[user_index]}!", cache=True
        )
        self.print_cache()

    def night_falls(self) -> None:
        """ Clears the output except for the player's role. """
        if self.disable_gui:
            return
        input("Press Enter to continue...")
        self.print_cache()

    def print_statements(self, all_statements: Tuple[Statement, ...]) -> None:
        """ Prints all statements that have been said so far. """
        if self.disable_gui:
            return
        logger.info("\n-- GAME BEGINS --\n", cache=True)
        for j, statement in enumerate(all_statements):
            logger.info(f"Player {j}: {statement.sentence}", cache=True)
        self.print_cache()
