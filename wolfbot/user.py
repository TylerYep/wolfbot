from collections.abc import Sequence

from wolfbot import const
from wolfbot.enums import Role, Team
from wolfbot.log import logger
from wolfbot.statements import Statement

CLEAR_TERMINAL = "\033c"
DISABLE_USER_INPUT = not const.INTERACTIVE_MODE


class UserState:
    """
    Contains logic for all of the official game logging.

    If INTERACTIVE_MODE is False, all actions are no-ops.
    """

    @staticmethod
    def print_cache() -> None:
        """Clears console and then output all lines stored in the logging cache."""
        logger.info(CLEAR_TERMINAL)
        for log_level, line in logger.output_cache:
            logger.log(log_level, line)

    @staticmethod
    def intro(original_roles: Sequence[Role]) -> None:
        """Tells the player what their assigned role is."""
        if DISABLE_USER_INPUT:
            return
        input("Press Enter to continue...")
        logger.info(CLEAR_TERMINAL)
        logger.clear()

        user_index = const.IS_USER.index(True)
        logger.info(
            f"Player {user_index}, you are a {original_roles[user_index]}!", cache=True
        )
        UserState.print_cache()

    @staticmethod
    def night_falls() -> None:
        """Clears the output except for the player's role."""
        if DISABLE_USER_INPUT:
            return
        input("Press Enter to continue...")
        UserState.print_cache()

    @staticmethod
    def print_statements(all_statements: tuple[Statement, ...]) -> None:
        """Prints all statements that have been said so far."""
        if DISABLE_USER_INPUT:
            return
        logger.info("\n-- GAME BEGINS --\n", cache=True)
        for j, statement in enumerate(all_statements):
            logger.info(f"Player {j}: {statement.sentence}", cache=True)
        UserState.print_cache()

    @staticmethod
    def print_game_result(game_roles: tuple[Role, ...], winning_team: Team) -> None:
        if DISABLE_USER_INPUT:
            return

        user_index = const.IS_USER.index(True)
        player_role = game_roles[user_index]
        if (
            (winning_team == Team.VILLAGE and player_role in const.VILLAGE_ROLES)
            or (winning_team == Team.WEREWOLF and player_role in const.EVIL_ROLES)
            or (winning_team == Team.TANNER and player_role == Role.TANNER)
        ):
            outcome = "won"
        else:
            outcome = "lost"

        logger.info(
            f"You were a {player_role} at the end of the game, so you {outcome}!"
        )
