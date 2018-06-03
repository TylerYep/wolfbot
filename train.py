import pickle
import os
import collections
import const
import main

def evaluate(game):
    val = 5
    for wolfi in game.wolf_inds:
        if game.guessed[wolfi] == 'Wolf':
            val = -5
    return val

def get_wolf_state(game):
    states, statements = [], []
    for wolf_ind in game.wolf_inds:
        states.append((tuple(game.wolf_inds), tuple([s.sentence for s in game.statements[:wolf_ind]])))
        statements.append(game.statements[wolf_ind].sentence)
    return states, statements

def train(folder, eta=0.01):
    counter = 0
    experience_dict = collections.defaultdict(const._get_int_dict)
    count_dict = collections.defaultdict(int) # NOTE: For testing purposes
    for f in os.listdir(folder):
        #print(f)
        file_path = os.path.join(folder, f)
        with open(file_path, 'rb') as data_file:
            for game in pickle.load(data_file):
                if counter %100 == 0:
                    test(experience_dict)
                val = evaluate(game)
                states, statements = get_wolf_state(game)
                for state, statement in zip(states, statements):
                    experience_dict[state][statement] = (1-eta)*experience_dict[state][statement] + eta*val
                    count_dict[(state)] += 1
                counter += 1
    with open('wolf_player.pkl', 'wb') as f: pickle.dump(experience_dict, f)

def test(experience_dict):
    main.main()

if __name__ == '__main__':
    folder = 'data' #TODO make this changeable
    train(folder)
