import random

from wolfbot import const
from wolfbot.const import logger
from wolfbot.enums import Role
from wolfbot.statements import Statement

CLEAR_TERMINAL = "\033c"


class UserState:
    """If INTERACTIVE_MODE is False, all actions are no-ops."""

    def __init__(self) -> None:
        self.disable_user_input = not const.INTERACTIVE_MODE

    @staticmethod
    def print_cache() -> None:
        """Clears console and then output all lines stored in the logging cache."""
        logger.info(CLEAR_TERMINAL)
        for log_level, line in logger.output_cache:
            logger.log(log_level, line)

    def intro(self, original_roles: tuple[Role, ...]) -> None:
        """Tells the player what their assigned role is."""
        if self.disable_user_input:
            return
        input("Press Enter to continue...")
        logger.info(CLEAR_TERMINAL)
        logger.clear()

        user_index = const.IS_USER.index(True)
        logger.info(
            f"Player {user_index}, you are a {original_roles[user_index]}!", cache=True
        )
        self.print_cache()

    def night_falls(self) -> None:
        """Clears the output except for the player's role."""
        if self.disable_user_input:
            return
        input("Press Enter to continue...")
        self.print_cache()

    def print_statements(self, all_statements: tuple[Statement, ...]) -> None:
        """Prints all statements that have been said so far."""
        if self.disable_user_input:
            return
        logger.info("\n-- GAME BEGINS --\n", cache=True)
        for j, statement in enumerate(all_statements):
            logger.info(f"Player {j}: {statement.sentence}", cache=True)
        self.print_cache()


def get_player(is_user: bool, exclude: tuple[int, ...] = ()) -> int:
    """Gets a random player index (not in the center) or prompts the user."""
    if is_user:
        choice_ind = -1
        while choice_ind < 0 or choice_ind >= const.NUM_PLAYERS:
            user_input = ""
            while not user_input.isdigit():
                user_input = input(
                    f"Which player index (0 - {const.NUM_PLAYERS - 1})? "
                )
            choice_ind = int(user_input)

            if choice_ind in exclude:
                logger.info("You cannot choose yourself or an index twice.")
                choice_ind = -1
        return choice_ind

    return random.choice([i for i in range(const.NUM_PLAYERS) if i not in exclude])


def get_center(is_user: bool, exclude: tuple[int, ...] = ()) -> int:
    """Gets a random index of a center card or prompts the user."""
    if is_user:
        choice_ind = -1
        while choice_ind < 0 or choice_ind >= const.NUM_CENTER:
            user_input = ""
            while not user_input.isdigit():
                user_input = input(f"Which center card (0 - {const.NUM_CENTER - 1})? ")
            choice_ind = int(user_input)

            if choice_ind + const.NUM_PLAYERS in exclude:
                logger.info("You cannot choose an index twice.")
                choice_ind = -1
        return choice_ind + const.NUM_PLAYERS

    return random.choice(
        [
            const.NUM_PLAYERS + i
            for i in range(const.NUM_CENTER)
            if const.NUM_PLAYERS + i not in exclude
        ]
    )


def get_numeric_input(end: int, start: int | None = None) -> int:
    """
    Prompts the user for an index between [start, end). Note that
    if two parameters are supplied, the order of the parameters flips
    in order to achieve a Pythonic range() function.
    """
    if start is None:
        start = 0
    else:
        start, end = end, start

    choice_ind = -1
    while choice_ind < start or end <= choice_ind:
        user_input = ""
        while not user_input.isdigit():
            user_input = input(f"Enter a number from {start} - {end - 1}: ")
        choice_ind = int(user_input)
    return choice_ind
