""" Imports all Player objects. """
import sys
from typing import Any

from src.roles.player import Player
from src.roles.village import Drunk, Hunter, Insomniac, Mason, Robber, Seer, Troublemaker, Villager
from src.roles.werewolf import Minion, Tanner, Wolf


def get_role_obj(role_str: str) -> Any:
    """ Retrieves class initializer from its string name. """
    return getattr(sys.modules[__name__], role_str)
