''' rl_wolf.py '''
import json
from collections import defaultdict
from const import logger
import const

from .reg_wolf import get_wolf_statements

def get_statement_rl(player_index, wolf_indices, stated_roles, previous_statements, default_answer):
    ''' Gets Reinforcement Learning Wolf statement. '''
    statements = get_wolf_statements(player_index, wolf_indices, stated_roles, previous_statements)

    # Necessary to put this here to avoid circular import
    from encoder import WolfBotDecoder

    exp_dict = dict()
    with open(const.EXPERIENCE_PATH, 'r') as exp_file:
        exp_dict = json.load(exp_file, cls=WolfBotDecoder)
    EXPERIENCE = defaultdict(lambda: defaultdict(int), exp_dict)
    assert EXPERIENCE

    state = (tuple(wolf_indices), tuple([s.sentence for s in previous_statements]))
    scores = EXPERIENCE[str(state)]
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

    # TODO Is this already covered in the previous return
    logger.warning('No match found. Using random statement...')
    return default_answer
