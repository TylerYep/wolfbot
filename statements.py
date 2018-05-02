import const

def get_villager_statements(player_index):
    return [Statement('I am a Villager.' , [(player_index, 'Villager')])]

def get_seer_statements(player_index, seen_index, seen_role):
    sentence = "I am a Seer and I saw that Player " + str(seen_index) + " was a " + str(seen_role) + "."
    knowledge = [(player_index, 'Seer'), (seen_index, seen_role)]
    return [Statement(sentence, knowledge)]

def get_wolf_statements(player_index, wolf_indices):
    statements = get_villager_statements(player_index)
    for i in range(const.NUM_PLAYERS):
        for role in const.ROLES:
            if i not in wolf_indices:
                statements += get_seer_statements(player_index, i, role)
    return statements


class Statement:
    def __init__(self, sentence, knowledge):
        self.sentence = sentence
        self.knowledge = knowledge

    def negate(self):
        ''' Returns a negated version of the statement. '''
        return Statement()

### Testing ###

if __name__ == '__main__':
    s = get_villager_statements(4)
    print(type(s))
    for hi in s:
        print(hi.sentence, hi.knowledge)
