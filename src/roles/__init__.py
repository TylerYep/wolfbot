# Not used, but enables - from roles import * -
__all__ = ['player', 'villager', 'mason', 'seer', 'robber', 'troublemaker', 'drunk', 'insomniac', 'wolf', 'possible']

from .player import Player
from .villager import Villager
from .mason import Mason
from .seer import Seer
from .robber import Robber
from .troublemaker import Troublemaker
from .drunk import Drunk
from .insomniac import Insomniac
from .wolf import Wolf
from .possible import get_possible_statements
