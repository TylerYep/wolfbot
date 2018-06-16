from collections import Counter, defaultdict
import logging
def _get_int_dict(): return defaultdict(int)
logging.basicConfig(format='%(message)s', level=logging.INFO)
logger = logging.getLogger()

### Simulation Constants ###
NUM_GAMES = 10
FIXED_WOLF_INDEX = None

### Game Constants ###
ROLES = ('Villager', 'Villager', 'Villager', 'Wolf', 'Wolf', 'Seer',
        'Mason', 'Mason', 'Drunk', 'Troublemaker', 'Insomniac', 'Robber')
NUM_CENTER = 3
# ROLES, NUM_CENTER = ('Villager', 'Villager', 'Villager', 'Seer', 'Wolf'), 0

ROLE_SET = set(ROLES)
NUM_ROLES = len(ROLES)
ROLE_COUNTS = dict(Counter(ROLES)) # Dict of {'Villager': 3, 'Wolf': 2, ... }

NUM_PLAYERS = NUM_ROLES - NUM_CENTER

ROBBER_PRIORITY, TROUBLEMAKER_PRIORITY, DRUNK_PRIORITY = 1, 2, 3
USE_VOTING = False

''' Expectimax Wolf Player'''
USE_EXPECTIMAX_WOLF = True
EXPECTIMAX_DEPTH = 1
BRANCH_FACTOR = 5

''' Reinforcement Learning Wolf Player'''
USE_WOLF_RL = False
EXPERIENCE_PATH = 'wolf_player.pkl'

### Logging Constants ###
logger.setLevel(logging.DEBUG)
#logger.setLevel(logging.WARNING)

''' DEBUG = Include all hidden messages '''
''' INFO = Regular gameplay '''
''' WARNING = Results only '''
