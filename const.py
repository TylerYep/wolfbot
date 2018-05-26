from collections import Counter
import logging

logging.basicConfig(format='%(message)s', level=logging.INFO)
logger = logging.getLogger()

### Simulation Constants ###
NUM_GAMES = 1
FIXED_WOLF_INDEX = None

### Game Constants ###

ROLES = ('Villager', 'Villager', 'Villager', 'Wolf', 'Wolf', 'Seer',
       'Mason', 'Mason', 'Drunk', 'Troublemaker', 'Insomniac', 'Robber')
# ROLES = ('Villager', 'Villager', 'Villager', 'Seer', 'Wolf')

ROLE_SET = set(ROLES)
NUM_ROLES = len(ROLES)
ROLE_COUNTS = dict(Counter(ROLES)) # Dict of {'Villager': 3, 'Wolf': 2, ... }

NUM_CENTER = 3
NUM_PLAYERS = NUM_ROLES - NUM_CENTER

ROBBER_PRIORITY = 1
TROUBLEMAKER_PRIORITY = 2
DRUNK_PRIORITY = 3

USE_WOLF_AI = False
USE_AI_PLAYERS = False

### Logging Constants ###
# logger.setLevel(logging.DEBUG)
logger.setLevel(logging.WARNING)

''' DEBUG = Include all hidden messages '''
''' INFO = Regular gameplay '''
''' WARNING = Results only '''
