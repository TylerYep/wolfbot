''' rl_wolf.py '''
from typing import Any, Dict, List
from collections import defaultdict
import json

from src.statements import Statement
from src.const import logger
from src import const

from .reg_wolf import get_wolf_statements

def get_statement_rl(player_obj: Any,
                     stated_roles: List[str],
                     previous_statements: List[Statement],
                     default_answer: Statement) -> Statement:
    ''' Gets Reinforcement Learning Wolf statement. '''
    statements = get_wolf_statements(player_obj, stated_roles, previous_statements)

    # Necessary to put this here to avoid circular import
    from src.encoder import WolfBotDecoder

    exp_dict: Dict[str, Dict[Statement, int]] = {}
    with open(const.EXPERIENCE_PATH, 'r') as exp_file:
        exp_dict = json.load(exp_file, cls=WolfBotDecoder)
    experience = defaultdict(lambda: defaultdict(int), exp_dict)
    assert experience

    logger.info('Experience dict loaded.')

    state = (tuple(player_obj.wolf_indices), tuple([s.sentence for s in previous_statements]))
    scores = experience[str(state)]
    choice = None
    best_score = -100
    for potential_statement, score in scores.items():
        if score > best_score:
            best_score = score
            choice = potential_statement
    if choice is None:
        return default_answer
    for statement in statements:
        if choice == statement.sentence:
            return statement

    return Statement("") # TODO
