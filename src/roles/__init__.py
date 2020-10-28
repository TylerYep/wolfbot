""" Imports all Player objects. """
import sys
from typing import Type, cast

from src.const import Role
from src.roles.player import Player
from src.roles.village import (
    Drunk,
    Hunter,
    Insomniac,
    Mason,
    Robber,
    Seer,
    Troublemaker,
    Villager,
)
from src.roles.werewolf import Minion, Tanner, Wolf


def get_role_obj(role_str: Role) -> Type[Player]:
    """ Retrieves class initializer from its string name. """
    role_class_name = role_str.value
    if role_str is Role.NONE:
        role_class_name = "Player"
    return cast(Type[Player], getattr(sys.modules[__name__], role_class_name))


__all__ = (
    "Role",
    "Player",
    "Drunk",
    "Hunter",
    "Insomniac",
    "Mason",
    "Robber",
    "Seer",
    "Troublemaker",
    "Villager",
    "Minion",
    "Tanner",
    "Wolf",
    "get_role_obj",
)
