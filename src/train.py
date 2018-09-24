''' train.py '''
import os
import json

from collections import defaultdict
from encoder import WolfBotEncoder, WolfBotDecoder
from main import main

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


# TODO: Figure out a way to map state to JSON. There should be a better way to do this.
def remap_keys(mapping):
    ''' Remaps keys for jsonifying. '''
    return [{'wolf_inds': k, 'statements': v} for k, v in mapping.items()]


def train(folder, eta=0.01):
    ''' Trains Wolf using games stored in simulations. '''
    counter = 0
    experience_dict = defaultdict(lambda: defaultdict(int))
    count_dict = defaultdict(int) # NOTE: For testing purposes
    for file in os.listdir(folder):
        file_path = os.path.join(folder, file)
        if file_path.lower().endswith('.json'):
            with open(file_path, 'r') as data_file:
                json_obj = json.load(data_file, cls=WolfBotDecoder)
                for game in json_obj:
                    if counter % 100 == 0:
                        test(experience_dict)
                    val = evaluate(game)
                    states, statements = get_wolf_state(game)
                    for state, statement in zip(states, statements):
                        experience_dict[state][statement] = (1-eta)*experience_dict[state][statement] + eta*val
                        count_dict[(state)] += 1
                    counter += 1

    exp_dict = remap_keys(experience_dict)
    with open('data/wolf_player.json', 'w') as wolf_file:
        json.dump(exp_dict, wolf_file, cls=WolfBotEncoder)


def test(experience_dict):
    ''' Run main with a specific experience_dict. '''
    main()


if __name__ == '__main__':
    train('data/simulations')
