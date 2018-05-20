from collections import Counter
import logging

logging.basicConfig(format='%(message)s', level=logging.INFO)
logger = logging.getLogger()

### Simulation Constants ###
NUM_GAMES = 1

### Game Constants ###
ROLES = ('Villager', 'Villager', 'Villager', 'Wolf', 'Wolf', 'Seer',
        'Mason', 'Mason', 'Robber', 'Drunk', 'Troublemaker')
# ROLES = ('Villager', 'Villager', 'Villager', 'Wolf', 'Seer')
ROLE_SET = set(ROLES)
NUM_ROLES = len(ROLES)
ROLE_COUNTS = dict(Counter(ROLES)) # Dict of {'Villager': 3, 'Wolf': 2, ... }

NUM_CENTER = 3
NUM_PLAYERS = NUM_ROLES - NUM_CENTER

ROBBER_PRIORITY = 1
TRBLMKR_PRIORITY = 2
DRUNK_PRIORITY = 3

### Logging Constants ###
logger.setLevel(logging.DEBUG)

''' DEBUG = Include all hidden messages '''
''' INFO = Regular gameplay '''
''' WARNING = Results only '''
