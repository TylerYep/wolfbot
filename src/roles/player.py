""" player.py """
from __future__ import annotations

import random
from typing import Any, Dict, List, Tuple

from overrides import EnforceOverrides

from src import const, util
from src.const import StatementLevel, logger
from src.predictions import make_prediction, make_random_prediction
from src.solvers import switching_solver as solver
from src.statements import KnowledgeBase, Statement


class Player(EnforceOverrides):  # type: ignore
    """ Player class. """

    def __init__(self, player_index: int):
        self.player_index = player_index
        self.role = type(self).__name__  # e.g. "Wolf"
        self.new_role = ""
        self.statements: List[Statement] = []
        self.prev_priority = StatementLevel.NOT_YET_SPOKEN
        if const.MULTI_STATEMENT:
            self.statements += self.get_partial_statements()

    def get_partial_statements(self) -> List[Statement]:
        """ Gets generic partial statements for each player. """
        partial_statements = []
        zero_sent = "I don't want to say who I am just yet."
        partial_statements.append(Statement(zero_sent, priority=StatementLevel.NO_INFO))

        if self.role not in const.EVIL_ROLES | frozenset({"Villager", "Hunter"}):
            partial_sent = f"I am a {self.role}, but I'm not going to say what I did or saw yet!"
            knowledge = ((self.player_index, frozenset({self.role})),)
            statement = Statement(partial_sent, knowledge, priority=StatementLevel.SOME_INFO)
            partial_statements.append(statement)
        return partial_statements

    def transform(self, role_type: str) -> Player:  # pylint: disable=too-many-locals
        """ Returns new Player identity. """
        from src.roles.werewolf import Wolf, Minion, Tanner
        from src.roles.village import (
            Villager,
            Seer,
            Robber,
            Troublemaker,
            Drunk,
            Insomniac,
            Hunter,
            Mason,
        )

        logger.debug(f"[Hidden] Player {self.player_index} ({self.role}) is a {role_type} now!")

        if role_type == "Wolf":
            return Wolf(self.player_index, [])
        if role_type == "Minion":
            return Minion(self.player_index, [])
        if role_type == "Tanner":
            return Tanner(self.player_index)
        if role_type == "Villager":
            return Villager(self.player_index)
        if role_type == "Hunter":
            return Hunter(self.player_index)
        if role_type == "Insomniac":
            # TODO you can lie and say you are a different character.
            return Insomniac(self.player_index, "Insomniac")
        if role_type == "Drunk":
            rand_center = util.get_center(const.IS_USER[self.player_index])
            return Drunk(self.player_index, rand_center)

        rand_int1 = util.get_player(const.IS_USER[self.player_index], exclude=(self.player_index,))
        if role_type == "Mason":
            return Mason(self.player_index, [self.player_index, rand_int1])

        rand_role = random.choice(list(const.ROLE_SET))
        if role_type == "Seer":
            return Seer(self.player_index, (rand_int1, rand_role))
        if role_type == "Robber":
            return Robber(self.player_index, rand_int1, rand_role)

        rand_int2 = util.get_player(
            const.IS_USER[self.player_index], exclude=(self.player_index, rand_int1)
        )
        if role_type == "Troublemaker":
            return Troublemaker(self.player_index, rand_int1, rand_int2)

        raise TypeError(f"Role Type: {role_type} is not a valid role.")

    @classmethod
    def awake_init(
        cls, player_index: int, game_roles: List[str], original_roles: List[str]
    ) -> Player:
        """ Initializes Player and performs their nighttime actions. """
        raise NotImplementedError

    @staticmethod
    def get_all_statements(player_index: int) -> List[Statement]:
        """ Required for all player types. Returns all possible role statements. """
        raise NotImplementedError

    def analyze(self, knowledge_base: KnowledgeBase) -> None:
        """ Updates Player state given new information. """
        # If someone says a Statement that involves you, set your new_role to their theory.
        if self.role in const.VILLAGE_ROLES:
            solver_result = random.choice(solver(tuple(knowledge_base.all_statements)))
            for i, truth in enumerate(solver_result.path):
                if truth:
                    statement = knowledge_base.all_statements[i]
                    self.new_role = statement.get_references(
                        self.player_index, knowledge_base.stated_roles
                    )

    def get_statement(self, knowledge_base: KnowledgeBase) -> Statement:
        """ Gets Player Statement. """
        del knowledge_base
        # If have a new role and are now evil, transform into that role.
        if self.new_role != "" and self.new_role in const.EVIL_ROLES:
            new_player_obj = self.transform(self.new_role)
            new_player_obj.prev_priority = self.prev_priority
            self = new_player_obj  # pylint: disable=self-cls-assignment
            if not [x for x in self.statements if x.priority > self.prev_priority]:
                from src.roles.werewolf.wolf_variants import get_wolf_statements_random

                self.statements = get_wolf_statements_random(self)

        self.statements = [x for x in self.statements if x.priority > self.prev_priority]

        # Choose a statement
        next_statement = random.choice(self.statements)

        # Evil players try to avoid giving info
        if const.MULTI_STATEMENT and const.USE_REG_WOLF and self.role in const.EVIL_ROLES:
            next_statement = min(self.statements, key=lambda x: x.priority)

        if const.IS_USER[self.player_index]:
            sample_statements = []
            choice = const.NUM_OPTIONS
            while choice == const.NUM_OPTIONS:
                logger.info("\nPlease choose from the following statements: ")
                sample_statements = (
                    random.sample(self.statements, const.NUM_OPTIONS) + [Statement("Next page...")]
                    if len(self.statements) > const.NUM_OPTIONS
                    else self.statements
                )
                for i, statement in enumerate(sample_statements):
                    logger.info(f"{i}. {statement.sentence}")
                choice = util.get_numeric_input(len(sample_statements))
            next_statement = sample_statements[choice]
        return next_statement

    def is_evil(self) -> bool:
        """ Decide whether a character should make an evil prediction or not. """
        # TODO When a wolf becomes good? Do I need to check for Wolf twice?
        return (
            self.role in const.EVIL_ROLES and self.new_role == ""
        ) or self.new_role in const.EVIL_ROLES

    def predict(self, statements: List[Statement]) -> Tuple[str, ...]:
        """ Gets a player's predictions for each index given all statements. """
        is_evil = self.is_evil()
        if const.SMART_VILLAGERS or is_evil:
            all_solutions = solver(tuple(statements), (self.player_index,))
            prediction = make_prediction(all_solutions, is_evil)
        else:
            prediction = make_random_prediction()
        return prediction

    def vote(self, prediction: Tuple[str, ...]) -> int:
        """
        Gets the player's vote for who the Wolf is for a given prediction.
        There are some really complicated game mechanics for the Minion.
        https://boardgamegeek.com/thread/1422062/pointing-center-free-parking
        """
        no_wolves_guess = (self.player_index + 1) % const.NUM_PLAYERS

        if const.IS_USER[self.player_index]:
            logger.info(
                f"\nWhich Player is a Wolf? (Enter {no_wolves_guess} if there are no Wolves)"
            )
            return util.get_player(is_user=True, exclude=(self.player_index,))

        if (
            const.INTERACTIVE_MODE
            and self.player_index < const.NUM_PLAYERS
            and util.weighted_coin_flip(const.INFLUENCE_PROB)
        ):
            # Convince other players to vote with you.
            logger.info(
                f"\nPlayer {self.player_index} trusts you. "
                f"Who should Player {self.player_index} vote for? "
                f"(Enter {no_wolves_guess} if there are no Wolves)"
            )
            return util.get_player(is_user=True, exclude=(self.player_index,))

        # TODO find the most likely Wolf and only vote for that one
        # Players cannot vote for themselves.
        found_wolf_inds = util.find_all_player_indices(
            prediction, "Wolf", exclude=(self.player_index,)
        )
        if found_wolf_inds:
            return random.choice(found_wolf_inds)

        return no_wolves_guess

    def __eq__(self, other: object) -> bool:
        """ Checks for equality between Players. Ensure that all fields exist and are identical. """
        assert isinstance(other, Player)
        self_json, other_json = self.json_repr(), other.json_repr()
        is_equal = all(self_json[key] == other_json[key] for key in self_json)
        return self.__dict__ == other.__dict__ and is_equal

    def json_repr(self) -> Dict[str, Any]:
        """ Gets JSON representation of a Player object. """
        return {"type": self.role, "player_index": self.player_index}

    def __repr__(self) -> str:
        """ Gets string representation of a Player object. """
        attrs = ""
        for key, item in self.json_repr().items():
            if key != "type":
                attrs += f"{item}, "
        return f"{self.role}({attrs[:-2]})"
