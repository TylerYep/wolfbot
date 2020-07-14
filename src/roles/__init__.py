""" Imports all Player objects. """
import sys
from typing import Any

from src.roles.player import Player
from src.roles.village.drunk import Drunk
from src.roles.village.hunter import Hunter
from src.roles.village.insomniac import Insomniac
from src.roles.village.mason import Mason
from src.roles.village.robber import Robber
from src.roles.village.seer import Seer
from src.roles.village.troublemaker import Troublemaker
from src.roles.village.villager import Villager
from src.roles.werewolf.minion import Minion
from src.roles.werewolf.tanner import Tanner
from src.roles.werewolf.wolf import Wolf


def get_role_obj(role_str: str) -> Any:
    """ Retrieves class initializer from its string name. """
    return getattr(sys.modules[__name__], role_str)
