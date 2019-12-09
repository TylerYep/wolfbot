''' const.py '''
import sys
import random
import logging
from enum import IntEnum, unique
from collections import Counter
import argparse

UNIT_TEST = 'pytest' in sys.modules
if UNIT_TEST: random.seed(0)

''' Command Line Arguments '''
PARSER = argparse.ArgumentParser(description='config constants for main.py')
PARSER.add_argument('--interactive', '-u', help='enable interactive mode', action='store_true')
PARSER.add_argument('--num_games', '-n', help='specify number of games')
PARSER.add_argument('--info', '-i', help='enable logging.INFO', action='store_true')
PARSER.add_argument('--replay', '-r', help='replay previous game', action='store_true')
ARGS = PARSER.parse_args('' if UNIT_TEST else sys.argv[1:])

''' Game Constants '''
ROLES = ('Drunk', 'Insomniac', 'Hunter', 'Mason', 'Mason', 'Minion', 'Robber', 'Seer', 'Tanner',
         'Troublemaker', 'Wolf', 'Wolf', 'Villager', 'Villager', 'Villager')
NUM_CENTER = 3
USE_VOTING = True
RANDOMIZE_ROLES = True

''' Simulation Constants '''
NUM_GAMES = 1 if ARGS.num_games is None else int(ARGS.num_games)
MAX_LOG_GAMES = 10
FIXED_WOLF_INDEX = -1
SHOW_PROGRESS = False or NUM_GAMES >= MAX_LOG_GAMES
SAVE_REPLAY = NUM_GAMES < MAX_LOG_GAMES
REPLAY_FILE = 'data/replay.json'
REPLAY = ARGS.replay

''' Util Constants '''
ROLE_SET = set(ROLES)
NUM_ROLES = len(ROLES)
ROLE_COUNTS = dict(Counter(ROLES))  # Dict of {'Villager': 3, 'Wolf': 2, ... }
NUM_PLAYERS = NUM_ROLES - NUM_CENTER

@unique
class Priority(IntEnum):
    ''' Priorities for Statement order. '''
    ROBBER = 1; TROUBLEMAKER = 2; DRUNK = 3

''' Game Rules '''
AWAKE_ORDER = ('Wolf', 'Minion', 'Mason', 'Seer', 'Robber', 'Troublemaker', 'Drunk', 'Insomniac')
VILLAGE_ROLES = {'Villager', 'Mason', 'Seer', 'Robber', 'Troublemaker', 'Drunk',
                 'Insomniac', 'Hunter'} & ROLE_SET
EVIL_ROLES = {'Tanner', 'Wolf', 'Minion'} & ROLE_SET

''' Basic Wolf Player (Pruned statement set) '''
USE_REG_WOLF = False
CENTER_SEER_PROB = 0.9

''' Expectimax Wolf Player '''
USE_EXPECTIMAX_WOLF = False
EXPECTIMAX_DEPTH = 1
BRANCH_FACTOR = 5

''' Reinforcement Learning Wolf Player '''
USE_RL_WOLF = False
EXPERIENCE_PATH = 'src/learning/simulations/wolf_player.json'

''' Interactive Game Constants '''
INTERACTIVE_MODE_ON = ARGS.interactive
IS_USER = [False] * NUM_ROLES
if INTERACTIVE_MODE_ON:
    IS_USER[random.randint(0, NUM_PLAYERS - 1)] = True

''' Logging Constants
TRACE = Debugging mode for development
DEBUG = Include all hidden messages
INFO = Regular gameplay
WARNING = Results only '''
TRACE = 5
logging.basicConfig(format='%(message)s', level=TRACE)  # , filename='test1.txt', filemode='a')
logger = logging.getLogger()  # pylint: disable=invalid-name

if ARGS.info: logger.setLevel(logging.INFO)
if NUM_GAMES >= 10 and not UNIT_TEST: logger.setLevel(logging.WARNING)
if INTERACTIVE_MODE_ON: logger.setLevel(logging.INFO)

''' Ensure only one Wolf version is active '''
assert sum([USE_EXPECTIMAX_WOLF, USE_RL_WOLF]) <= 1

if sys.version_info < (3, 0):
    sys.stdout.write('Requires Python 3, not Python 2!\n')
    sys.exit()
