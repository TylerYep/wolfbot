from roles import Wolf, Player, Villager, Mason, Seer, Robber, Troublemaker, Drunk, Insomniac
from statements import Statement
from statistics import GameResult
import json
import pickle
import const

class WolfBotEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Player) or isinstance(obj, Statement) or isinstance(obj, GameResult):
            return obj.json_repr()
        elif isinstance(obj, set):
            return {'type': 'Set', 'data': tuple(obj)}
        else:
            super().default(self, obj)


class WolfBotDecoder(json.JSONDecoder):
    def __init__(self):
        json.JSONDecoder.__init__(self, object_hook=self.json_to_objects)
        self.str_to_obj = {}
        for role in (Wolf, Villager, Mason, Seer, Robber, Troublemaker, Drunk, Insomniac):
            self.str_to_obj[role.__name__] = role

    def json_to_objects(self, obj):
        if 'type' not in obj: return obj

        type = obj['type']
        if type == 'Set':
            return set(obj['data'])
        elif type == 'Statement':
            return Statement(obj['sentence'], obj['knowledge'], obj['switches'])
        elif type == 'GameResult':
            return GameResult(obj['actual'], obj['guessed'], obj['statements'],
                            obj['wolf_inds'], obj['found_single_vote_wolf'])
        elif type in const.ROLE_SET:
            return self.str_to_obj[type](obj) # TODO
        return obj


def convert_dict_to_json(file_path):
    with open(file_path, 'rb') as fpkl, open('%s.json' % file_path[0:-4], 'w') as fjson:
        data = pickle.load(fpkl)
        json.dump(data, fjson, cls=WolfBotEncoder)
