from collections import Counter
import logging

logging.basicConfig(format='%(message)s', level=logging.INFO)
logger = logging.getLogger()

### Simulation Constants ###
NUM_GAMES = 10000

### Game Constants ###

#ROLES = ('Villager', 'Villager', 'Villager', 'Wolf', 'Wolf', 'Seer',
#        'Mason', 'Mason', 'Robber', 'Drunk', 'Troublemaker', 'Insomniac')
ROLES = ('Villager', 'Villager', 'Villager', 'Seer', 'Wolf')

ROLE_SET = set(ROLES)
NUM_ROLES = len(ROLES)
ROLE_COUNTS = dict(Counter(ROLES)) # Dict of {'Villager': 3, 'Wolf': 2, ... }

NUM_CENTER = 0
NUM_PLAYERS = NUM_ROLES - NUM_CENTER

ROBBER_PRIORITY = 1
TROUBLEMAKER_PRIORITY = 2
DRUNK_PRIORITY = 3

USE_AI_PLAYERS = False

### Logging Constants ###
logger.setLevel(logging.WARNING)

''' DEBUG = Include all hidden messages '''
''' INFO = Regular gameplay '''
''' WARNING = Results only '''
