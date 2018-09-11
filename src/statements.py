import const

class Statement:
    def __init__(self, sentence, knowledge, switches=[]):
        '''
        sentence is a string representation of the statement
        knowledge is a list of (player_index, set(role)) tuples
        switches is a list of (player_index, new_index) tuples
        '''
        self.sentence = sentence
        self.knowledge = knowledge
        self.switches = switches
        self.speaker = next(iter(knowledge[0][1])) if len(self.knowledge) != 0 else None

    def negate(self):
        ''' Returns a negated version of the first clause in a statement. '''
        neg = []
        if len(self.knowledge) != 0:
            playerClause = self.knowledge[0]
            newSet = set(const.ROLES) - playerClause[1]
            neg = [(playerClause[0], newSet)]
        return Statement('NOT + ' + self.sentence, neg, [])

    def negateAll(self):
        ''' Returns a negated version of every clause in the statement. '''
        neg = []
        for tupl in self.knowledge:
            newSet = set(const.ROLES) - tupl[1]
            neg.append((tupl[0], newSet))
        return Statement('NOT + ' + self.sentence, neg, [])

    def __repr__(self):
        return "Statement(\'" + self.sentence + "\', " + str(self.knowledge) + ", " + str(self.switches) + '),'


### Testing ###
if __name__ == '__main__':
    s = Seer.get_seer_statements(3, 4, 'Villager')
    for statement in s:
        print(statement)
    st = s[0].negate()
    print(st)
