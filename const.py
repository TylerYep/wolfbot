from collections import Counter
import logging

ROLES = ('Villager', 'Villager', 'Villager', 'Wolf', 'Wolf', 'Seer')
ROLE_SET = set(ROLES)
NUM_PLAYERS = len(ROLES)
ROLE_COUNTS = dict(Counter(ROLES))
NUM_GAMES = 1

logging.basicConfig(format='%(message)s', level=logging.INFO)
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
# Toggle between DEBUG and WARNING to see game output
