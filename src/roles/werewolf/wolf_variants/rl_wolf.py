""" rl_wolf.py """
import json
from collections import defaultdict
from typing import Any, Dict

from src import const
from src.const import logger
from src.statements import KnowledgeBase, Statement

from .reg_wolf import get_wolf_statements


def get_statement_rl(
    player_obj: Any, knowledge_base: KnowledgeBase, default_answer: Statement,
) -> Statement:
    """ Gets Reinforcement Learning Wolf statement. """
    statements = get_wolf_statements(player_obj, knowledge_base)

    # Necessary to put this here to avoid circular import
    from src.encoder import WolfBotDecoder

    exp_dict: Dict[str, Dict[Statement, int]] = {}
    with open(const.EXPERIENCE_PATH) as exp_file:
        exp_dict = json.load(exp_file, cls=WolfBotDecoder)
    experience = defaultdict(lambda: defaultdict(int), exp_dict)
    assert experience

    logger.info("Experience dict loaded.")

    state = (tuple(player_obj.wolf_indices), tuple(knowledge_base.all_statements))
    scores = experience[str(state)]
    best_choice = (default_answer, -100)
    for potential_statement, score in scores.items():
        if score > best_choice[1]:
            best_choice = (potential_statement, score)
    if best_choice[0] is None:
        return default_answer
    for statement in statements:
        if best_choice[0] == statement:
            return statement

    return Statement("")  # TODO
