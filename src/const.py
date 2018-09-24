''' const.py '''
from collections import Counter, defaultdict
import logging
logging.basicConfig(format='%(message)s', level=logging.INFO)
logger = logging.getLogger()
def _get_int_dict(): return defaultdict(int) # TODO Delete this when wolf_player.pkl is obsolete

''' Game Constants '''
ROLES = ('Villager', 'Villager', 'Villager', 'Wolf', 'Wolf', 'Seer',
         'Mason', 'Mason', 'Drunk', 'Troublemaker', 'Insomniac', 'Robber')
NUM_CENTER = 3
USE_VOTING = True

''' Util Constants '''
ROLE_SET = set(ROLES)
NUM_ROLES = len(ROLES)
ROLE_COUNTS = dict(Counter(ROLES)) # Dict of {'Villager': 3, 'Wolf': 2, ... }
NUM_PLAYERS = NUM_ROLES - NUM_CENTER
ROBBER_PRIORITY, TROUBLEMAKER_PRIORITY, DRUNK_PRIORITY = 1, 2, 3

''' Expectimax Wolf Player'''
USE_EXPECTIMAX_WOLF = False
EXPECTIMAX_DEPTH = 1
BRANCH_FACTOR = 5

''' Reinforcement Learning Wolf Player'''
USE_RL_WOLF = False
EXPERIENCE_PATH = 'data/wolf_player.json'

''' Simulation Constants '''
NUM_GAMES = 1
SHOW_PROGRESS = False or NUM_GAMES >= 10
FIXED_WOLF_INDEX = None

''' Logging Constants '''
logging.TRACE = 5
logger.setLevel(logging.TRACE)
if NUM_GAMES >= 10: logger.setLevel(logging.WARNING)
'''
TRACE = Debugging mode for development
DEBUG = Include all hidden messages
INFO = Regular gameplay
WARNING = Results only
'''
