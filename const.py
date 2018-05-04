from collections import Counter
import logging

### Simulation Constants ###
NUM_GAMES = 1

### Game Constants ###
ROLES = ('Villager', 'Villager', 'Villager', 'Wolf', 'Wolf', 'Mason', 'Mason', 'Seer')
ROLE_SET = set(ROLES)
NUM_ROLES = len(ROLES)
ROLE_COUNTS = dict(Counter(ROLES))

NUM_CENTER = 3
NUM_PLAYERS = NUM_ROLES - NUM_CENTER

### Logging Constants ###
logging.basicConfig(format='%(message)s', level=logging.INFO)
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

''' DEBUG = Include all hidden messages '''
''' INFO = Regular gameplay '''
''' WARNING = Results only '''
