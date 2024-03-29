import json
import sys
from typing import Any, Generic, TypeVar, cast, override

from wolfbot import const
from wolfbot.enums import Role, Team
from wolfbot.roles import Player, get_role_obj
from wolfbot.statements import Statement
from wolfbot.stats import GameResult, SavedGame

T = TypeVar("T")


class WolfBotEncoder(json.JSONEncoder):
    """Encoder for all WolfBot objects."""

    @override
    def default(self, o: Any) -> Any:
        """Overrides encoding method."""
        if isinstance(o, Role | Team | Player | Statement | GameResult | SavedGame):
            return o.json_repr()
        if isinstance(o, set):
            return {"type": "Set", "data": sorted(o)}
        if isinstance(o, frozenset):
            return {"type": "FrozenSet", "data": sorted(o)}
        return json.JSONEncoder.default(self, o)


class WolfBotDecoder(json.JSONDecoder):
    """Decoder for all WolfBot objects."""

    def __init__(self) -> None:
        super().__init__(object_hook=self.json_to_objects)

    @staticmethod
    def json_to_objects(obj: dict[str, Any]) -> Any:
        """Implements decoding method."""
        obj_type = obj.pop("type", None)
        if obj_type == "Set":
            return set(obj["data"])
        if obj_type == "FrozenSet":
            return frozenset(obj["data"])
        if obj_type == "Role":
            return Role(obj["data"])
        if obj_type == "Team":
            return Team(obj["data"])
        if obj_type == "Statement":
            obj["knowledge"] = tuple(tuple(know) for know in obj["knowledge"])
            obj["switches"] = tuple(tuple(switch) for switch in obj["switches"])
            return ObjectInitializer[Statement]().get(obj_type)(**obj)
        if obj_type == "GameResult":
            for key, value in obj.items():
                if key != "winning_team":
                    obj[key] = tuple(value)
            return ObjectInitializer[GameResult]().get(obj_type)(**obj)
        if obj_type == "SavedGame":
            for key, value in obj.items():
                obj[key] = tuple(value)
            return ObjectInitializer[SavedGame]().get(obj_type)(**obj)
        if obj_type in (rol.value for rol in const.ROLE_SET):
            if obj_type == Role.SEER.value:
                obj["choice_1"] = tuple(obj["choice_1"])
                obj["choice_2"] = tuple(obj["choice_2"])
            elif obj_type == Role.MASON.value:
                obj["mason_indices"] = tuple(obj["mason_indices"])
            return get_role_obj(Role(obj_type))(**obj)
        return obj


class ObjectInitializer(Generic[T]):
    """Generic class used to initialize an object of a given type."""

    @staticmethod
    def get(obj_name: str) -> Any:
        """Retrieves class initializer from its string name."""
        return cast(type[T], getattr(sys.modules[__name__], obj_name))
