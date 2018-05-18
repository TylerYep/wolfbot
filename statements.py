import const

class Statement:
    def __init__(self, sentence, knowledge, switches):
        '''
        sentence is a string representation of the statement
        knowledge is a list of (player_index, set(role)) tuples
        switches is a list of (player_index, new_index) tuples
        '''
        self.sentence = sentence
        self.knowledge = knowledge
        self.switches = switches

    def negate(self):
        ''' Returns a negated version of the first clause in a statement. '''
        firstClause = self.knowledge[0]
        newSet = set(const.ROLES) - firstClause[1]
        neg = [(firstClause[0], newSet)]
        return Statement('NOT + ' + self.sentence, neg, []) #TODO

    def negateAll(self):
        ''' Returns a negated version of every clause in the statement. '''
        neg = []
        for tupl in self.knowledge:
            newSet = set(const.ROLES) - tupl[1]
            neg.append((tupl[0], newSet))
        return Statement('NOT + ' + self.sentence, neg, []) #TODO

    def __repr__(self):
        return str(self.sentence) # + " " + str(self.knowledge) + " " + str(self.switches)


### Testing ###
if __name__ == '__main__':
    s = get_seer_statements(3, 4, 'Villager')
    for statement in s:
        print(statement.sentence, statement.knowledge)
    st = s[0].negate()
    print(st.sentence, st.knowledge)
