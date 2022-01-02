from __future__ import annotations

import logging
import random
from collections.abc import Iterator, Sequence
from dataclasses import dataclass, field

from wolfbot import const
from wolfbot.enums import Role
from wolfbot.log import logger

Switch = tuple[int, int]


@dataclass(slots=True)
class GameRoles:
    """Wrapper for the game_roles list."""

    roles: list[Role]
    changelog: list[int] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.changelog = [0] * len(const.ROLES)

    def __len__(self) -> int:
        return len(self.roles)

    def __iter__(self) -> Iterator[Role]:
        yield from self.roles

    def __bool__(self) -> bool:
        return bool(self.roles)

    def __contains__(self, role: Role) -> bool:
        return role in self.roles

    def __getitem__(self, index: int) -> Role:
        return self.roles[index]

    def __setitem__(self, index: int, new_role: Role) -> None:
        self.roles[index] = new_role

    def swap_characters(self, ind1: int, ind2: int) -> None:
        swap_characters(self.roles, ind1, ind2)
        self.changelog[ind1], self.changelog[ind2] = ind2, ind1


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
