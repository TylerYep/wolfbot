import pickle
from main import GameResult
import os
import collections
import const
#self.actual = actual
#self.guessed = guessed
#self.statements = statements

#self.sentence = sentence
#self.knowledge = knowledge
#self.switches = switches
#self.speaker = next(iter(knowledge[0][1])) if len(self.knowledge) != 0 else None

def evaluate(game):
    val = 5 
    for wolfi in game.wolf_inds:
        if game.guessed[wolfi] == 'Wolf':
            val -= 10 
    return val

def get_wolf_state(game):
    states, statements = [], []
    for wolf_ind in game.wolf_inds:
        #TODO account for the other wolf
        states.append((tuple(game.wolf_inds), tuple([s.sentence for s in game.statements[:wolf_ind]])))
        statements.append(game.statements[wolf_ind].sentence) 
    return states, statements

def _get_int_dict():
    return collections.defaultdict(int)

def train(folder, a=0.1):
    experience_dict = collections.defaultdict(const._get_int_dict)
    count_dict = collections.defaultdict(int) #NOTE: For testing purposes
    for f in os.listdir(folder):
        file_path = os.path.join(folder, f)
        with open(file_path, 'rb') as data_file:
            for game in pickle.load(data_file):
                val = evaluate(game)
                states, statements = get_wolf_state(game)
                for state, statement in zip(states, statements):
                    experience_dict[state][statement] = (1-a)*experience_dict[state][statement] + a*val
                    count_dict[(state, statement)] += 1 
                # TODO test while training to see improvement :)
    
    with open('wolf_player_simple.pkl', 'wb') as f: pickle.dump(experience_dict, f)

def test(experience_dict):
    pass

if __name__ == '__main__':
    folder = 'data' #TODO make this changeable
    train(folder)
