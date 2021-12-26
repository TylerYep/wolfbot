""" util.py """
from __future__ import annotations

import logging
import random
from collections.abc import Sequence

from wolfbot import const
from wolfbot.const import logger
from wolfbot.enums import Role


def verify_valid_const_config() -> None:
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
    """Formats hidden roles to console."""
    players = list(game_roles[: const.NUM_PLAYERS])
    centers = list(game_roles[const.NUM_PLAYERS :])
    role_output = (
        f"[{tag}] Player roles: {players}\n{' ' * (len(tag) + 3)}"
        f"Center cards: {centers}\n"
    )
    logger.log(log_level, role_output.replace("'", ""))


def swap_characters(game_roles: list[Role], ind1: int, ind2: int) -> None:
    """Util function to swap two characters, updating game_roles."""
    if ind1 == ind2:
        raise RuntimeError("Cannot swap the same index.")
    if not (0 <= ind1 < const.NUM_ROLES and 0 <= ind2 < const.NUM_ROLES):
        raise RuntimeError(f"ind1 and/or ind2 is out of bounds: {ind1} {ind2}")
    game_roles[ind1], game_roles[ind2] = game_roles[ind2], game_roles[ind1]


def find_all_player_indices(
    game_roles: Sequence[Role], role: Role, exclude: tuple[int, ...] = ()
) -> tuple[int, ...]:
    """Util function to find all indices of a given role."""
    return tuple(
        i
        for i in range(const.NUM_PLAYERS)
        if game_roles[i] is role and i not in exclude
    )


def weighted_coin_flip(prob: float) -> bool:
    """Flips a weighted coin with probability prob and 1 - prob."""
    return random.choices([True, False], [prob, 1 - prob])[0]
