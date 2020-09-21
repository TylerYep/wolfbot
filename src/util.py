""" util.py """
import logging
import random
from typing import List, Optional, Sequence, Tuple

from src import const
from src.const import Role, logger


def verify_const() -> None:
    if const.USER_ROLE is not Role.NONE and const.USER_ROLE not in const.ROLE_SET:
        raise RuntimeError(f"USER_ROLE is invalid: {const.USER_ROLE}")
    if const.EXPECTIMAX_WOLF and const.RL_WOLF:
        raise RuntimeError("EXPECTIMAX_WOLF and RL_WOLF cannot both be enabled.")
    if Role.DRUNK in const.ROLE_SET and const.NUM_CENTER <= 0:
        raise RuntimeError("Drunk cannot be included when there are no center cards.")
    if Role.MASON in const.ROLE_SET and const.ROLE_COUNTS[Role.MASON] != 2:
        raise RuntimeError("Exactly 2 Masons must be included to play.")
    if const.NUM_PLAYERS <= 1 and (
        Role.ROBBER in const.ROLE_SET or Role.SEER in const.ROLE_SET
    ):
        raise RuntimeError("There are too few players to include Robber and Seer.")
    if const.NUM_PLAYERS <= 2 and Role.TROUBLEMAKER in const.ROLE_SET:
        raise RuntimeError("There are too few players to include Troublemaker.")


def print_roles(
    game_roles: Sequence[Role], tag: str, log_level: int = logging.DEBUG
) -> None:
    """ Formats hidden roles to console. """
    players = list(game_roles[: const.NUM_PLAYERS])
    centers = list(game_roles[const.NUM_PLAYERS :])
    role_output = (
        f"[{tag}] Player roles: {players}\n{' ' * (len(tag) + 3)}"
        f"Center cards: {centers}\n"
    )
    logger.log(log_level, role_output.replace("'", ""))


def swap_characters(game_roles: List[Role], ind1: int, ind2: int) -> None:
    """ Util function to swap two characters, updating game_roles. """
    if ind1 == ind2:
        raise RuntimeError("Cannot swap the same index.")
    if not (0 <= ind1 < const.NUM_ROLES and 0 <= ind2 < const.NUM_ROLES):
        raise RuntimeError(f"ind1 and/or ind2 is out of bounds: {ind1} {ind2}")
    game_roles[ind1], game_roles[ind2] = game_roles[ind2], game_roles[ind1]


def find_all_player_indices(
    game_roles: Sequence[Role], role: Role, exclude: Tuple[int, ...] = ()
) -> Tuple[int, ...]:
    """ Util function to find all indices of a given role. """
    return tuple(
        i
        for i in range(const.NUM_PLAYERS)
        if game_roles[i] is role and i not in exclude
    )


def get_player(is_user: bool, exclude: Tuple[int, ...] = ()) -> int:
    """ Gets a random player index (not in the center) or prompts the user. """
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


def get_center(is_user: bool, exclude: Tuple[int, ...] = ()) -> int:
    """ Gets a random index of a center card or prompts the user. """
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

    choices = [
        const.NUM_PLAYERS + i
        for i in range(const.NUM_CENTER)
        if const.NUM_PLAYERS + i not in exclude
    ]
    return random.choice(choices)


def get_numeric_input(end: int, start: Optional[int] = None) -> int:
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


def weighted_coin_flip(prob: float) -> bool:
    """ Flips a weighted coin with probability prob and 1 - prob. """
    return random.choices([True, False], [prob, 1 - prob])[0]
