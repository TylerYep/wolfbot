import sys
from typing import cast

from wolfbot.enums import Role
from wolfbot.roles.player import Player
from wolfbot.roles.village import (
    Drunk,
    Hunter,
    Insomniac,
    Mason,
    Robber,
    Seer,
    Troublemaker,
    Villager,
)
from wolfbot.roles.werewolf import Minion, Tanner, Wolf


def get_role_obj(role_str: Role) -> type[Player]:
    """Retrieves class initializer from its string name."""
    role_class_name = role_str.value
    if role_str is Role.NONE:
        role_class_name = "Player"
    return cast(type[Player], getattr(sys.modules[__name__], role_class_name))


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
