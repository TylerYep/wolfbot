'''
train.py
To run, cd to src/ and run python -m learning.train
'''
import json
import os
import time
from collections import defaultdict

from src import const
from src.const import logger
from src.encoder import WolfBotDecoder, WolfBotEncoder
from src.one_night import play_one_night_werewolf
from src.stats import Statistics


def evaluate(game):
    ''' Evaluation function. '''
    val = 5
    for wolf_ind in game.wolf_inds:
        if game.guessed[wolf_ind] == 'Wolf':
            val = -5
    return val


def get_wolf_state(game):
    ''' Fetches Wolf statement from Game. '''
    states, statements = [], []
    for wolf_ind in game.wolf_inds:
        state = (tuple(game.wolf_inds), tuple([s.sentence for s in game.statements[:wolf_ind]]))
        states.append(state)
        statements.append(game.statements[wolf_ind].sentence)
    return states, statements


def remap_keys(mapping):
    ''' Remaps keys for jsonifying. '''
    exp_dict = defaultdict(lambda: defaultdict(int))
    for k, val in mapping.items():
        exp_dict[str(k)] = val
    return exp_dict


def train(folder, eta=0.01):
    ''' Trains Wolf using games stored in simulations. '''
    counter = 0
    experience_dict = defaultdict(lambda: defaultdict(int))
    count_dict = defaultdict(int)  # NOTE: For testing purposes
    for file in os.listdir(folder):
        file_path = os.path.join(folder, file)
        if file_path.lower().endswith('.json'):
            with open(file_path, 'r') as data_file:
                for game in json.load(data_file, cls=WolfBotDecoder):
                    # See how training improves over time
                    if counter % 100 == 0:
                        test()
                    states, statements = get_wolf_state(game)
                    for state, statement in zip(states, statements):
                        experience_dict[state][statement] \
                            = (1 - eta) * experience_dict[state][statement] + eta * evaluate(game)
                        count_dict[(state)] += 1
                    counter += 1

    exp_dict = remap_keys(experience_dict)
    with open(f'learning/simulations/wolf_{time.strftime("%Y%m%d_%H%M%S")}.json', 'w') as wolf_file:
        json.dump(exp_dict, wolf_file, cls=WolfBotEncoder)


def test():  # experience_dict as param
    ''' Run play_one_night_werewolf with a specific experience_dict. '''
    assert const.USE_RL_WOLF is False
    start_time = time.time()
    stats = Statistics()
    for num in range(const.NUM_GAMES):
        if const.SHOW_PROGRESS and num % 10 == 0:
            logger.warning(f'Currently on Game: {num}')
        game_result = play_one_night_werewolf(False)
        stats.add_result(game_result)
    stats.print_statistics()
    logger.warning(f'\nTime taken: {time.time() - start_time}')


if __name__ == '__main__':
    train('learning/simulations')
