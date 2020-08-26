""" encoder_test.py """
import json

from src import encoder
from src.const import Role, SwitchPriority, Team
from src.encoder import WolfBotDecoder, WolfBotEncoder
from src.roles import Player, Robber, Seer, Villager
from src.statements import Statement
from src.stats import GameResult, SavedGame


class TestWolfBotEncoderDecoder:
    """
    Tests for the WolfBotEncoder and WolfBotDecoder class.
    These tests break the arrange-act-assert paradigm to keep them symmetric.
    """

    @staticmethod
    def test_default_list() -> None:
        """ Should convert objects of different types to JSON. """
        input_obj = [Role.WOLF, Role.VILLAGER]

        result = json.dumps(input_obj, cls=WolfBotEncoder)
        assert result == '[{"type": "Role", "data": "Wolf"}, {"type": "Role", "data": "Villager"}]'

        reverted_result = json.loads(result, cls=WolfBotDecoder)
        assert reverted_result == input_obj

    @staticmethod
    def test_default_set() -> None:
        """ Should convert objects of different types to JSON. """
        input_obj = {Role.WOLF, Role.VILLAGER}

        result = json.dumps(input_obj, cls=WolfBotEncoder)
        assert result == (
            '{"type": "Set",'
            ' "data": [{"type": "Role", "data": "Villager"}, {"type": "Role", "data": "Wolf"}]}'
        )

        reverted_result = json.loads(result, cls=WolfBotDecoder)
        assert reverted_result == input_obj

    @staticmethod
    def test_default_frozenset() -> None:
        """ Should convert objects of different types to JSON. """
        input_obj = frozenset([Role.WOLF, Role.VILLAGER])

        result = json.dumps(input_obj, cls=WolfBotEncoder)
        assert result == (
            '{"type": "FrozenSet",'
            ' "data": [{"type": "Role", "data": "Villager"}, {"type": "Role", "data": "Wolf"}]}'
        )

        reverted_result = json.loads(result, cls=WolfBotDecoder)
        assert reverted_result == input_obj

    @staticmethod
    def test_default_statement(example_statement: Statement) -> None:
        """ Should convert objects of different types to JSON. """
        result = json.dumps(example_statement, cls=WolfBotEncoder)
        assert result == (
            '{"type": "Statement",'
            ' "sentence": "test",'
            ' "knowledge": [[2, {"type": "FrozenSet",'
            ' "data": [{"type": "Role", "data": "Robber"}]}],'
            ' [0, {"type": "FrozenSet", "data": [{"type": "Role", "data": "Seer"}]}]],'
            ' "switches": [[1, 2, 0]], "speaker": {"type": "Role", "data": "Robber"}}'
        )

        reverted_result = json.loads(result, cls=WolfBotDecoder)
        assert reverted_result == example_statement

    @staticmethod
    def test_default_player() -> None:
        """ Should convert objects of different types to JSON. """
        input_obj = Villager(0)

        result = json.dumps(input_obj, cls=WolfBotEncoder)
        assert result == '{"type": "Villager", "player_index": 0}'

        reverted_result = json.loads(result, cls=WolfBotDecoder)
        assert reverted_result == input_obj

    @staticmethod
    def test_default_role() -> None:
        """ Should convert objects of different types to JSON. """
        input_obj = Role.VILLAGER

        result = json.dumps(input_obj, cls=WolfBotEncoder)
        assert result == '{"type": "Role", "data": "Villager"}'

        reverted_result = json.loads(result, cls=WolfBotDecoder)
        assert reverted_result == input_obj

    @staticmethod
    def test_default_team() -> None:
        """ Should convert objects of different types to JSON. """
        input_obj = Team.WEREWOLF

        result = json.dumps(input_obj, cls=WolfBotEncoder)
        assert result == '{"type": "Team", "data": 3}'

        reverted_result = json.loads(result, cls=WolfBotDecoder)
        assert reverted_result == input_obj

    @staticmethod
    def test_default_game_result(example_small_game_result: GameResult) -> None:
        """ Should convert objects of different types to JSON. """
        result = json.dumps(example_small_game_result, cls=WolfBotEncoder)
        reverted_result = json.loads(result, cls=WolfBotDecoder)

        assert reverted_result == example_small_game_result

    @staticmethod
    def test_default_saved_game(example_small_saved_game: SavedGame) -> None:
        """ Should convert objects of different types to JSON. """
        player_objs = [Villager(0), Robber(1, 2, Role.SEER), Seer(2, (1, Role.ROBBER))]
        player_strs = ", ".join([json.dumps(player, cls=WolfBotEncoder) for player in player_objs])
        statement_objs = [
            Statement(
                "I am a Villager.", ((0, frozenset({Role.VILLAGER})),), speaker=Role.VILLAGER
            ),
            Statement(
                "I am a Robber and I swapped with Player 2. I am now a Seer.",
                ((1, frozenset({Role.ROBBER})), (2, frozenset({Role.SEER}))),
                ((SwitchPriority.ROBBER, 1, 2),),
                Role.ROBBER,
            ),
            Statement(
                "I am a Seer and I saw that Player 1 was a Robber.",
                ((2, frozenset({Role.SEER})), (1, frozenset({Role.ROBBER}))),
                speaker=Role.SEER,
            ),
        ]
        statement_strs = ", ".join(
            [json.dumps(statement, cls=WolfBotEncoder) for statement in statement_objs]
        )

        result = json.dumps(example_small_saved_game, cls=WolfBotEncoder)
        assert result == (
            '{"type": "SavedGame",'
            ' "original_roles": [{"type": "Role", "data": "Villager"},'
            ' {"type": "Role", "data": "Robber"}, {"type": "Role", "data": "Seer"}],'
            ' "game_roles": [{"type": "Role", "data": "Villager"},'
            ' {"type": "Role", "data": "Seer"}, {"type": "Role", "data": "Robber"}],'
            f' "all_statements": [{statement_strs}],'
            f' "player_objs": [{player_strs}]}}'
        )

        reverted_result = json.loads(result, cls=WolfBotDecoder)
        assert reverted_result == example_small_saved_game


class TestGetObjectInitializer:
    """ Tests for the get_object_initializer function. """

    @staticmethod
    def test_get_object_initializers() -> None:
        """ Should return the correct object initializer. """
        result = (
            encoder.get_object_initializer("Player"),
            encoder.get_object_initializer("Statement"),
            encoder.get_object_initializer("GameResult"),
            encoder.get_object_initializer("SavedGame"),
        )

        assert result == (Player, Statement, GameResult, SavedGame)
