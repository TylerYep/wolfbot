""" Imports all Player objects. """
import sys
from typing import Any

from src.const import Role
from src.roles.player import Player
from src.roles.village import Drunk, Hunter, Insomniac, Mason, Robber, Seer, Troublemaker, Villager
from src.roles.werewolf import Minion, Tanner, Wolf


def get_role_obj(role_str: Role) -> Any:
    """ Retrieves class initializer from its string name. """
    role_class_name = role_str.value
    if role_str == Role.NONE:
        role_class_name = "Player"
    return getattr(sys.modules[__name__], role_class_name)
