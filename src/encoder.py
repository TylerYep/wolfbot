''' encoder.py '''
import json
import pickle

from statistics import GameResult
from statements import Statement
from roles import Player #, get_role_obj
import const

class WolfBotEncoder(json.JSONEncoder):
    ''' Encoder for all WolfBot objects '''
    def default(self, obj):
        ''' Overrides encoding method. '''
        if isinstance(obj, (Player, Statement, GameResult)):
            return obj.json_repr()
        if isinstance(obj, set):
            return {'type': 'Set', 'data': tuple(obj)}
        return json.JSONEncoder.default(self, obj)


class WolfBotDecoder(json.JSONDecoder):
    ''' Decoder for all WolfBot objects '''
    def __init__(self):
        json.JSONDecoder.__init__(self, object_hook=self.json_to_objects)

    @staticmethod
    def json_to_objects(obj):
        ''' Implements decoding method. '''
        if 'type' not in obj:
            return obj
        obj_type = obj['type']
        del obj['type']

        if obj_type == 'Set':
            return set(obj['data'])
        if obj_type == 'Statement':
            return Statement(**obj)
        if obj_type == 'GameResult':
            return GameResult(**obj)
        if obj_type in const.ROLE_SET:
            return Player(obj['player_index'], obj['new_role'])
            # For recreating the entire player object:
            # return get_role_obj(obj_type)(player_index, game_roles, original_roles)
        return obj


def convert_dict_to_json(file_path):
    ''' Backwards compatibility with pkl. '''
    with open(file_path, 'rb') as fpkl, open(f'{file_path[0:-4]}.json', 'w') as fjson:
        data = pickle.load(fpkl)
        json.dump(data, fjson, cls=WolfBotEncoder)
