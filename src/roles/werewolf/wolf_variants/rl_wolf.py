from ...village import Player, Villager, Mason, Seer, Robber, Troublemaker, Drunk, Insomniac
import const
import json

def get_statement_rl(wolf_indices, previous_statements):
    EXPERIENCE = dict()
    # Necessary to put this here to avoid circular import
    from encoder import WolfBotDecoder
    with open(const.EXPERIENCE_PATH, 'r') as f:
        EXPERIENCE = json.load(f, cls=WolfBotDecoder)
    assert(len(EXPERIENCE) > 0)

    state = (tuple(wolf_indices), tuple([s.sentence for s in previous_statements]))
    scores = EXPERIENCE[state]
    choice = None
    best_score = -100
    for potential_statement, score in scores.items():
        if score > best_score:
            best_score = score
            choice = potential_statement
    if choice is None:
        return super().get_statement()
    for statement in statements:
        if choice == statement.sentence:
            return statement

    # TODO Is this already covered in the previous return
    logger.warning('No match found. Using random statement...')
    return super().get_statement()
