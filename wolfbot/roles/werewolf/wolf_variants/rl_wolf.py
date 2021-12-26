import json
from collections import defaultdict
from typing import Any

from wolfbot import const
from wolfbot.log import logger
from wolfbot.roles.werewolf.wolf_variants.reg_wolf import get_wolf_statements
from wolfbot.statements import KnowledgeBase, Statement


def get_statement_rl(
    player_obj: Any, knowledge_base: KnowledgeBase, default_answer: Statement
) -> Statement:
    """Gets Reinforcement Learning Wolf statement."""
    statements = get_wolf_statements(player_obj, knowledge_base)

    # Necessary to put this here to avoid circular import
    from wolfbot.encoder import WolfBotDecoder

    exp_dict: dict[str, dict[Statement, int]] = {}
    with open(const.EXPERIENCE_PATH, encoding="utf-8") as exp_file:
        exp_dict = json.load(exp_file, cls=WolfBotDecoder)
    experience = defaultdict(lambda: defaultdict(int), exp_dict)
    if not experience:
        logger.info("Experience dict did not load properly.")

    state = (tuple(player_obj.wolf_indices), tuple(knowledge_base.all_statements))
    scores = experience[str(state)]
    logger.info(f"Experience dict loaded.\n    {len(scores)} matching states.")

    best_choice = (default_answer, -100)
    for potential_statement, score in scores.items():
        if score > best_choice[1]:
            best_choice = (potential_statement, score)
    if best_choice[0] is None:
        logger.info("Using default statement...")
        return default_answer
    for statement in statements:
        if best_choice[0] == statement:
            return statement

    raise RuntimeError("Reached end of rl_wolf code.")
