import const
from const import logger

def makePredictions(solution):
    '''
    Uses a list of true/false statements and possible role sets
    to return a list of predictions for all roles
    '''
    consistent_statements = solution.path
    consistent_roles = solution.possible_roles
    switch_dict = solution.switch_dict

    all_role_guesses = []
    curr_role_counts = dict(const.ROLE_COUNTS)
    for j in range(const.NUM_ROLES):
        guess_set = consistent_roles[j]

        if j >= len(consistent_statements):     # Center cards
            for r in const.ROLE_SET:
                if curr_role_counts[r] == 0:
                    guess_set |= set(r)
            if len(guess_set) == 1:
                all_role_guesses.append(next(iter(guess_set)))
            else:
                for r in const.ROLE_SET:
                    if curr_role_counts[r] >= 1:
                        curr_role_counts[r] -= 1
                        all_role_guesses.append(r)
                        break

        elif consistent_statements[j]:      # Player is telling the truth
            role = next(iter(guess_set))
            curr_role_counts[role] -= 1
            all_role_guesses.append(role)

        elif not consistent_statements[j]:      # Player is lying
            all_role_guesses.append('Wolf')
            curr_role_counts['Wolf'] -= 1
            logger.info("I suspect Player " + str(j) + " is a Wolf!")

    final_guesses = []
    for i in range(len(all_role_guesses)):
        final_guesses.append(all_role_guesses[switch_dict[i]])
    return final_guesses

def verifyPredictions(game_roles, all_role_guesses):
    correctGuesses = 0
    totalWolves = 0
    for r in range(len(all_role_guesses)):
        if game_roles[r] == 'Wolf' == all_role_guesses[r]:
            correctGuesses += 1
    for card in game_roles[:const.NUM_PLAYERS]:
        if card == 'Wolf':
            totalWolves += 1
    return correctGuesses, totalWolves, correctGuesses >= 1, correctGuesses == totalWolves
