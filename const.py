from collections import Counter
import logging

ROLES = ('Villager', 'Villager', 'Villager', 'Wolf', 'Wolf', 'Mason', 'Mason', 'Seer')
ROLE_SET = set(ROLES)
NUM_ROLES = len(ROLES)
ROLE_COUNTS = dict(Counter(ROLES))

NUM_CENTER = 3
NUM_PLAYERS = NUM_ROLES - NUM_CENTER

NUM_GAMES = 2

logging.basicConfig(format='%(message)s', level=logging.INFO)
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
# Toggle between DEBUG and WARNING to see game output
