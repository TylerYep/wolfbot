""" util.py """
import logging
import random
from typing import List, Optional, Sequence, Tuple

from src import const
from src.const import logger


def print_roles(game_roles: Sequence[str], tag: str, log_level: int = logging.DEBUG) -> None:
    """ Formats hidden roles to console. """
    role_output = (
        f"[{tag}] Player roles: {game_roles[:const.NUM_PLAYERS]}\n{' ' * (len(tag) + 3)}"
        f"Center cards: {game_roles[const.NUM_PLAYERS:]}\n"
    )
    logger.log(log_level, role_output.replace("'", ""))


def swap_characters(game_roles: List[str], ind1: int, ind2: int) -> None:
    """ Util function to swap two characters, updating game_roles. """
    assert ind1 != ind2
    assert 0 <= ind1 < const.NUM_ROLES and 0 <= ind2 < const.NUM_ROLES
    game_roles[ind1], game_roles[ind2] = game_roles[ind2], game_roles[ind1]


def find_all_player_indices(
    game_roles: Sequence[str], role: str, exclude: Tuple[int, ...] = ()
) -> List[int]:
    """ Util function to find all indices of a given role. """
    return [i for i in range(const.NUM_PLAYERS) if game_roles[i] == role and i not in exclude]


def get_player(is_user: bool, exclude: Tuple[int, ...] = ()) -> int:
    """ Gets a random player index (not in the center) or prompts the user. """
    if is_user:
        choice_ind = -1
        while choice_ind < 0 or choice_ind >= const.NUM_PLAYERS:
            user_input = ""
            while not user_input.isdigit():
                user_input = input(f"Which player index (0 - {const.NUM_PLAYERS - 1})? ")
            choice_ind = int(user_input)

            if choice_ind in exclude:
                logger.info("You cannot choose yourself or an index twice.")
                choice_ind = -1
        return choice_ind

    choice_ind = -1
    while choice_ind == -1 or choice_ind in exclude:
        choice_ind = random.randrange(const.NUM_PLAYERS)
    return choice_ind


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

    choice_ind = -1
    while choice_ind == -1 or choice_ind in exclude:
        choice_ind = const.NUM_PLAYERS + random.randrange(const.NUM_CENTER)
    return choice_ind


def get_numeric_input(end: int, start: Optional[int] = None) -> int:
    """
    Prompts the user for an index between [start, end). Note that if two parameters are supplied,
    the order of the parameters flips in order to achieve a Pythonic range() function.
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
