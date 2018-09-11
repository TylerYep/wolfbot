from collections import Counter
import logging
logging.basicConfig(format='%(message)s', level=logging.INFO)
logger = logging.getLogger()

''' Simulation Constants '''
NUM_GAMES = 1
SHOW_PROGRESS = False
FIXED_WOLF_INDEX = None

''' Game Constants '''
ROLES = ('Villager', 'Villager', 'Villager', 'Wolf', 'Wolf', 'Seer',
        'Mason', 'Mason', 'Drunk', 'Troublemaker', 'Insomniac', 'Robber')
NUM_CENTER = 3
USE_VOTING = False

''' Util Constants '''
ROLE_SET = set(ROLES)
NUM_ROLES = len(ROLES)
ROLE_COUNTS = dict(Counter(ROLES)) # Dict of {'Villager': 3, 'Wolf': 2, ... }
NUM_PLAYERS = NUM_ROLES - NUM_CENTER
ROBBER_PRIORITY, TROUBLEMAKER_PRIORITY, DRUNK_PRIORITY = 1, 2, 3

''' Expectimax Wolf Player'''
USE_EXPECTIMAX_WOLF = False
EXPECTIMAX_DEPTH = 1
BRANCH_FACTOR = 5

''' Reinforcement Learning Wolf Player'''
USE_WOLF_RL = False
EXPERIENCE_PATH = 'data/wolf_player.pkl'

''' Logging Constants '''
logger.setLevel(logging.DEBUG)
#logger.setLevel(logging.WARNING)

''' DEBUG = Include all hidden messages '''
''' INFO = Regular gameplay '''
''' WARNING = Results only '''
