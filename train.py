import pickle
from main import GameResult
import os
import collections

#self.actual = actual
#self.guessed = guessed
#self.statements = statements

if __name__ == '__main__':
    folder = 'data' #TODO make this changeable
    
    #TODO Load in a master dict 
    experience_dict = collections.defaultdict(list)
    for f in os.listdir(folder):
        file_path = os.path.join(folder, f)
        with open(file_path, 'rb') as data_file:
            for game in pickle.load(data_file):
                print(game)
                # TODO some sort of evaluation
                #val = evaluate(game)
                # TODO How do we want to model the state?
                #state, statement = wolf_state(game)
                # TODO Use straight average instead of weighted average?
                #experience_dict[state][statement] = (1-a)*experience_dict[state][statement] + a*val
                
                # TODO test while training to see improvement :)
