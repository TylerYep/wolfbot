''' const.py '''
import sys
import random
import logging
from collections import Counter

''' Game Constants '''
ROLES = ('Insomniac', 'Villager', 'Villager', 'Villager', 'Wolf', 'Wolf', 'Seer', 'Tanner',
         'Mason', 'Mason', 'Drunk', 'Troublemaker', 'Robber', 'Minion', 'Hunter')
# ROLES = ('Drunk', 'Insomniac', 'Hunter', 'Mason', 'Mason', 'Minion', 'Robber', 'Seer', 'Tanner',
#          'Troublemaker', 'Wolf', 'Wolf', 'Villager', 'Villager', 'Villager')
NUM_CENTER = 3
USE_VOTING = True
RANDOMIZE_ROLES = True

''' Simulation Constants '''
NUM_GAMES = 1
FIXED_WOLF_INDEX = -1
SHOW_PROGRESS = False or NUM_GAMES >= 10
SAVE_REPLAY = NUM_GAMES < 10
UNIT_TEST = 'pytest' in sys.modules
if UNIT_TEST: random.seed(0)

''' Util Constants '''
ROLE_SET = set(ROLES)
NUM_ROLES = len(ROLES)
ROLE_COUNTS = dict(Counter(ROLES))  # Dict of {'Villager': 3, 'Wolf': 2, ... }
NUM_PLAYERS = NUM_ROLES - NUM_CENTER

''' Game Rules '''
ROBBER_PRIORITY, TROUBLEMAKER_PRIORITY, DRUNK_PRIORITY = 1, 2, 3
AWAKE_ORDER = ('Wolf', 'Minion', 'Mason', 'Seer', 'Robber', 'Troublemaker', 'Drunk', 'Insomniac')
VILLAGE_ROLES = {'Villager', 'Mason', 'Seer', 'Robber', 'Troublemaker', 'Drunk',
                 'Insomniac', 'Hunter'} & ROLE_SET
EVIL_ROLES = {'Tanner', 'Wolf', 'Minion'} & ROLE_SET

''' Basic Wolf Player (Pruned statement set) '''
USE_REG_WOLF = True

''' Expectimax Wolf Player '''
USE_EXPECTIMAX_WOLF = False
EXPECTIMAX_DEPTH = 1
BRANCH_FACTOR = 5

''' Reinforcement Learning Wolf Player '''
USE_RL_WOLF = False
EXPERIENCE_PATH = 'src/learning/simulations/wolf_player.json'

''' Interactive Game Constants '''
INTERACTIVE_MODE_ON = False
IS_USER = [False for _ in range(NUM_ROLES)]
if INTERACTIVE_MODE_ON:
    IS_USER[random.randint(0, NUM_PLAYERS - 1)] = True

''' Logging Constants
TRACE = Debugging mode for development
DEBUG = Include all hidden messages
INFO = Regular gameplay
WARNING = Results only '''
TRACE = 5
logging.basicConfig(format='%(message)s', level=TRACE)#, filename='test1.txt', filemode='a')
logger = logging.getLogger()

if NUM_GAMES >= 10 and not UNIT_TEST: logger.setLevel(logging.WARNING)
if INTERACTIVE_MODE_ON: logger.setLevel(logging.INFO)

''' Ensure only one Wolf version is active '''
assert sum([USE_EXPECTIMAX_WOLF, USE_RL_WOLF]) <= 1

if sys.version_info < (3, 0):
    sys.stdout.write('Requires Python 3, not Python 2!\n')
    sys.exit()
