''' encoder_test.py '''
import json

from src import encoder
from src.encoder import WolfBotEncoder, WolfBotDecoder
from src.roles import Villager, Player
from src.statements import Statement
from src.stats import GameResult, SavedGame

class TestWolfBotEncoder:
    @staticmethod
    def test_default_list():
        ''' Should convert objects of different types to JSON. '''
        input_obj = ['Wolf', 'Villager']

        result = json.dumps(input_obj, cls=WolfBotEncoder)

        assert result == '["Wolf", "Villager"]'

    @staticmethod
    def test_default_set():
        ''' Should convert objects of different types to JSON. '''
        input_obj = set(['Wolf', 'Villager'])

        result = json.dumps(input_obj, cls=WolfBotEncoder)

        assert result == '{"type": "Set", "data": ["Villager", "Wolf"]}'

    @staticmethod
    def test_default_frozenset():
        ''' Should convert objects of different types to JSON. '''
        input_obj = frozenset(['Wolf', 'Villager'])

        result = json.dumps(input_obj, cls=WolfBotEncoder)

        assert result == '{"type": "FrozenSet", "data": ["Villager", "Wolf"]}'

    @staticmethod
    def test_default_statement(example_statement):
        ''' Should convert objects of different types to JSON. '''
        result = json.dumps(example_statement, cls=WolfBotEncoder)

        assert result == ('{"type": "Statement",'
                          ' "sentence": "test",'
                          ' "knowledge": [[2, {"type": "FrozenSet", "data": ["Robber"]}],'
                          ' [0, {"type": "FrozenSet", "data": ["Seer"]}]],'
                          ' "switches": [[1, 2, 0]], "speaker": "Robber"}')

    @staticmethod
    def test_default_player():
        ''' Should convert objects of different types to JSON. '''
        input_obj = Villager(0)

        result = json.dumps(input_obj, cls=WolfBotEncoder)

        assert result == '{"type": "Villager", "player_index": 0}'

    @staticmethod
    def test_default_game_result(example_small_game_result):
        ''' Should convert objects of different types to JSON. '''
        result = json.dumps(example_small_game_result, cls=WolfBotEncoder)

        assert result == ('{"type": "GameResult",'
                          ' "actual": ["Villager", "Seer", "Robber"],'
                          ' "guessed": ["Villager", "Seer", "Robber"],'
                          ' "wolf_inds": [],'
                          ' "winning_team": "Villager"}')

    # @staticmethod
    # def test_default_saved_game(example_saved_game):
    #     ''' Should convert objects of different types to JSON. '''
    #     result = json.dumps(example_saved_game, cls=WolfBotEncoder)
    #
    #     assert result == ''


class TestWolfBotDecoder:
    @staticmethod
    def test_json_to_list():
        ''' Should convert JSON to the correct objects. '''
        input_json = '["Wolf", "Villager"]'

        result = json.loads(input_json, cls=WolfBotDecoder)

        assert result == ['Wolf', 'Villager']

    @staticmethod
    def test_json_to_set():
        ''' Should convert JSON to the correct objects. '''
        input_json = '{"type": "Set", "data": ["Villager", "Wolf"]}'

        result = json.loads(input_json, cls=WolfBotDecoder)

        assert result == set(['Wolf', 'Villager'])

    @staticmethod
    def test_json_to_frozenset():
        ''' Should convert JSON to the correct objects. '''
        input_json = '{"type": "FrozenSet", "data": ["Villager", "Wolf"]}'

        result = json.loads(input_json, cls=WolfBotDecoder)

        assert result == frozenset(['Wolf', 'Villager'])

    @staticmethod
    def test_json_to_statement(example_statement):
        ''' Should convert JSON to the correct objects. '''
        input_json = ('{"type": "Statement",'
                      ' "sentence": "test",'
                      ' "knowledge": [[2, {"type": "FrozenSet", "data": ["Robber"]}],'
                      ' [0, {"type": "FrozenSet", "data": ["Seer"]}]],'
                      ' "switches": [[1, 2, 0]], "speaker": "Robber"}')

        result = json.loads(input_json, cls=WolfBotDecoder)

        assert result == example_statement

    @staticmethod
    def test_json_to_player():
        ''' Should convert JSON to the correct objects. '''
        input_json = '{"type": "Villager", "player_index": 0}'

        result = json.loads(input_json, cls=WolfBotDecoder)

        assert result == Villager(0)

    @staticmethod
    def test_json_to_game_result(example_small_game_result):
        ''' Should convert JSON to the correct objects. '''
        input_json = ('{"type": "GameResult",'
                      ' "actual": ["Villager", "Seer", "Robber"],'
                      ' "guessed": ["Villager", "Seer", "Robber"],'
                      ' "wolf_inds": [],'
                      ' "winning_team": "Villager"}')

        result = json.loads(input_json, cls=WolfBotDecoder)

        assert result == example_small_game_result

    # @staticmethod
    # def test_json_to_saved_game():
    #     ''' Should convert JSON to the correct objects. '''
    #     result = json.loads(input_json, cls=WolfBotDecoder)
    #
    #     assert result == ''


class TestGetObjectInitializer:
    @staticmethod
    def test_get_object_initializers():
        ''' Should return the correct object initializer. '''
        result = (encoder.get_object_initializer('Player'),
                  encoder.get_object_initializer('Statement'),
                  encoder.get_object_initializer('GameResult'),
                  encoder.get_object_initializer('SavedGame'))

        assert result == (Player, Statement, GameResult, SavedGame)


class TestConvertPklToJson:
    @staticmethod
    def test_convert_pkl_to_json():
        ''' Should convert pkl to JSON. '''
        pass
