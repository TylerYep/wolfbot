from collections import Counter, defaultdict
import logging
def _get_int_dict(): return defaultdict(int)
logging.basicConfig(format='%(message)s', level=logging.INFO)
logger = logging.getLogger()

### Simulation Constants ###
NUM_GAMES = 50
FIXED_WOLF_INDEX = None

### Game Constants ###
ROLES = ('Villager', 'Villager', 'Villager', 'Wolf', 'Wolf', 'Seer',
      'Mason', 'Mason', 'Drunk', 'Troublemaker', 'Insomniac', 'Robber')
NUM_CENTER = 3
# ROLES = ('Villager', 'Villager', 'Villager', 'Seer', 'Wolf')
# NUM_CENTER = 0

ROLE_SET = set(ROLES)
NUM_ROLES = len(ROLES)
ROLE_COUNTS = dict(Counter(ROLES)) # Dict of {'Villager': 3, 'Wolf': 2, ... }

NUM_PLAYERS = NUM_ROLES - NUM_CENTER

ROBBER_PRIORITY = 1
TROUBLEMAKER_PRIORITY = 2
DRUNK_PRIORITY = 3
USE_AI_PLAYERS = False

''' Expectimax Wolf Player'''
USE_WOLF_AI = True
EXPECTIMAX_DEPTH = 3
EVAL_UNIT = 10
BRANCH_FACTOR = 3

''' Reinforcement Learning Wolf Player'''
USE_WOLF_RL = False
EXPERIENCE_PATH = 'wolf_player.pkl'

### Logging Constants ###
logger.setLevel(logging.DEBUG)
logger.setLevel(logging.WARNING)

''' DEBUG = Include all hidden messages '''
''' INFO = Regular gameplay '''
''' WARNING = Results only '''
