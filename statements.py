# TODO MAKE THESE GLOBAL CONSTANTS
NUM_PLAYERS = 6
ROLES = ('Villager', 'Villager', 'Villager', 'Wolf', 'Wolf', 'Seer')

def get_villager_statements(player_index):
    return [Statement('I am a Villager.' , [(player_index, 'V')])]

def get_seer_statements(player_index, seen_index, seen_role):
    sentence = "I am a Seer and I saw that Player " + str(seen_index) + " was a " + str(seen_role) + "."
    knowledge = [(player_index, 'S'), (seen_index, seen_role)]
    return [Statement(sentence, knowledge)]

def get_wolf_statements(player_index, wolf_indices):
    statements = [get_villager_statements(player_index)]
    for i in range(NUM_PLAYERS):
        for role in ROLES:
            if i not in wolf_indices:
                statements += get_seer_statements(player_index, i, role)
    return statements


class Statement:
    def __init__(self, sentence, knowledge):
        self.sentence = sentence
        self.knowledge = knowledge

    # def __iter__(self):
    #     return iter()

    def __hash__(self):
        return hash(self.sentence)

    def __eq__(self, other):
        if not isinstance(other, type(self)): return NotImplemented
        return self.sentence == other.sentence and self.knowledge == other.knowledge

    def negate(self):
        # returns a new negated statement
        return Statement()

### Testing ###
if __name__ == '__main__':
    s = get_villager_statements(4)
    print(type(s))
    for hi in s:
        print(hi.sentence, hi.knowledge)
