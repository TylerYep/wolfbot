''' Imports all Player objects. '''
from typing import Any
import sys
from .player import Player
from .village.villager import Villager
from .village.mason import Mason
from .village.seer import Seer
from .village.robber import Robber
from .village.troublemaker import Troublemaker
from .village.drunk import Drunk
from .village.insomniac import Insomniac
from .village.hunter import Hunter
from .werewolf.wolf import Wolf
from .werewolf.minion import Minion
from .werewolf.tanner import Tanner


def get_role_obj(role_str: str) -> Any:
    ''' Retrieves class initializer from its string name. '''
    return getattr(sys.modules[__name__], role_str)
