import const
from const import logger
from copy import deepcopy

def make_predictions(solution):
    '''
    Uses a list of true/false statements and possible role sets
    to return a list of predictions for all roles
    '''
    consistent_statements = solution.path
    consistent_roles = deepcopy(solution.possible_roles)

    switch_dict = {i:i for i in range(const.NUM_ROLES)}
    switches = sorted(solution.switches, key=lambda x: x[0])
    for priority, i, j in switches:
        temp = switch_dict[i]
        switch_dict[i] = switch_dict[j]
        switch_dict[j] = temp

    all_role_guesses = []
    curr_role_counts = dict(const.ROLE_COUNTS)
    for j in range(const.NUM_ROLES):
        guess_set = consistent_roles[j]
        if j >= len(consistent_statements) or consistent_statements[j]:     # Center cards or Player is telling the truth
            for r in const.ROLE_SET:                # Remove already chosen cards
                if curr_role_counts[r] == 0:
                    guess_set -= set([r])

            if len(guess_set) == 1:                 # Player is telling the truth
                role = next(iter(guess_set))
                curr_role_counts[role] -= 1
                all_role_guesses.append(role)
            else:
                all_role_guesses.append('')

        elif not consistent_statements[j]:      # Player is lying
            all_role_guesses.append('Wolf')
            curr_role_counts['Wolf'] -= 1
            #logger.info("I suspect Player " + str(j) + " is a Wolf!")

    # Assign the remaining unknown cards by recursing and finding a consistent placement
    solved = []
    def recurse_assign(all_role_guesses, curr_role_counts):
        new_guesses = list(all_role_guesses)
        nonlocal solved
        found = True
        for i in range(const.NUM_ROLES):
            if all_role_guesses[i] == '':
                found = False
        if found:
            solved = list(new_guesses)
            return True

        for i in range(const.NUM_ROLES):
            if all_role_guesses[i] == '':
                for r in solution.possible_roles[i]:
                    if curr_role_counts[r] > 0:
                        curr_role_counts[r] -= 1
                        new_guesses[i] = r
                        if recurse_assign(new_guesses, dict(curr_role_counts)): return True
                        curr_role_counts[r] += 1
                        new_guesses[i] = ''
        return False

    found_solution = recurse_assign(list(all_role_guesses), dict(curr_role_counts))
    if not found_solution:
        for j in range(len(all_role_guesses)):
            if all_role_guesses[j] == 'Wolf':
                all_role_guesses[j] = ''
                curr_role_counts['Wolf'] += 1
        recurse_assign(list(all_role_guesses), dict(curr_role_counts))
    final_guesses = []
    for i in range(len(solved)):
        final_guesses.append(solved[switch_dict[i]])
    return final_guesses


def print_guesses(all_role_guesses):
    logger.info("\n[Wolfbot] Role guesses: " + str(all_role_guesses[:const.NUM_PLAYERS]) +
                "\n\t  Center cards: " + str(all_role_guesses[const.NUM_PLAYERS:]) + '\n')

def verify_predictions(game_roles, all_role_guesses):
    correctGuesses = 0
    totalWolves = 0
    for r in range(len(all_role_guesses)):
        if game_roles[r] == 'Wolf' == all_role_guesses[r]:
            correctGuesses += 1
    for card in game_roles[:const.NUM_PLAYERS]:
        if card == 'Wolf':
            totalWolves += 1
    return correctGuesses, totalWolves, correctGuesses >= 1, correctGuesses == totalWolves
