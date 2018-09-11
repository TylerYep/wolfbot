from roles import Player
from statements import Statement
import json
import pickle

class WolfBotEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Player) or isinstance(obj, Statement):
            return obj.json_repr()
        elif isinstance(obj, set):
            return {'type': 'Set', 'data': tuple(obj)}
        else:
            super().default(self, obj)

class WolfBotDecoder(json.JSONDecoder):
    def __init__(self):
        json.JSONDecoder.__init__(self, object_hook=self.json_to_objects)

    def json_to_objects(self, obj):
        if 'type' not in obj:
            return obj
        type = obj['type']
        if type == 'Set':
            return set(obj['data'])
        elif type == 'Statement':
            return Statement(obj['sentence'], obj['knowledge'], obj['switches'])
        # TODO Currently unused. Make a function mapping to solve this issue.
        elif type in ['Player', 'Villager', 'Mason', 'Seer', 'Robber', 'Troublemaker', 'Drunk', 'Insomniac', 'Wolf']:
            return Player(obj)
        return obj

def convert_dict_to_json(file_path):
    with open(file_path, 'rb') as fpkl, open('%s.json' % file_path[0:-4], 'w') as fjson:
        data = pickle.load(fpkl)
        json.dump(data, fjson, cls=WolfBotEncoder)
