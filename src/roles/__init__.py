''' Imports all Player objects. '''
import sys
from typing import Any

from .player import Player
from .village.drunk import Drunk
from .village.hunter import Hunter
from .village.insomniac import Insomniac
from .village.mason import Mason
from .village.robber import Robber
from .village.seer import Seer
from .village.troublemaker import Troublemaker
from .village.villager import Villager
from .werewolf.minion import Minion
from .werewolf.tanner import Tanner
from .werewolf.wolf import Wolf


def get_role_obj(role_str: str) -> Any:
    ''' Retrieves class initializer from its string name. '''
    return getattr(sys.modules[__name__], role_str)
