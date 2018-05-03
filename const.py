from collections import Counter

ROLES = ('Villager', 'Villager', 'Villager', 'Wolf', 'Wolf', 'Seer')
ROLE_SET = set(ROLES)
NUM_PLAYERS = len(ROLES)
ROLE_COUNTS = dict(Counter(ROLES))
