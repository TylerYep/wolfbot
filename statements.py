import const

def get_villager_statements(player_index):
    ''' Returns list of Statements a Villager can say. '''
    return [Statement("I am a Villager." , [(player_index, {'Villager'})])]

def get_seer_statements(player_index, seen_index, seen_role):
    ''' Returns list of Statements a Seer can say. '''
    sentence = "I am a Seer and I saw that Player " + str(seen_index) + " was a " + str(seen_role) + "."
    knowledge = [(player_index, {'Seer'}), (seen_index, {seen_role})]
    return [Statement(sentence, knowledge)]

def get_wolf_statements(player_index, wolf_indices):
    ''' Returns list of Statements a Wolf can say. '''
    statements = get_villager_statements(player_index)
    for i in range(const.NUM_PLAYERS):
        # Wolf imitating seer more likely to declare they saw a villager?
        for role in const.ROLES:
            # Wolf should not give away other wolves or themselves
            if i not in wolf_indices and role != 'Seer':
                statements += get_seer_statements(player_index, i, role)
    return statements

# TODO
def get_robber_statements(player_index, robber_choice_index, robber_choice_character):
    return [Statement("", "")]

# TODO
def get_mason_statements(player_index, mason_indices):
    otherMason = mason_indices[0] if mason_indices[0] != player_index else mason_indices[1]
    if len(mason_indices) == 1:
        return [Statement("I am a Mason. The other Mason is unknown.", "")]
    else:
        return [Statement("I am a Mason. The other Mason is Player " + otherMason, "")]

class Statement:
    def __init__(self, sentence, knowledge):
        self.sentence = sentence
        self.knowledge = knowledge
        # knowledge contains tuples of (player_index, set(role))

    def negate(self):
        ''' Returns a negated version of the first clause in a statement. '''
        firstClause = self.knowledge[0]
        newSet = set(const.ROLES) - firstClause[1]
        neg = [(firstClause[0], newSet)]
        return Statement('NOT + ' + self.sentence, neg)

    def negateAll(self):
        ''' Returns a negated version of every clause in the statement. '''
        neg = []
        for tupl in self.knowledge:
            newSet = set(const.ROLES) - tupl[1]
            neg.append((tupl[0], newSet))
        return Statement('NOT + ' + self.sentence, neg)

### Testing ###
if __name__ == '__main__':
    s = get_seer_statements(3, 4, 'Villager')
    for statement in s:
        print(statement.sentence, statement.knowledge)
    st = s[0].negate()
    print(st.sentence, st.knowledge)
