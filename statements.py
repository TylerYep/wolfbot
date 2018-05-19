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
        return Statement('NOT + ' + self.sentence, neg, []) #TODO

    def __repr__(self):
        return "Statement(\'" + self.sentence + "\', " + str(self.knowledge) + ", " + str(self.switches) + '),'

def possible_statements():
    possible = {}
    for player_index in range(const.NUM_PLAYERS):
        possible[player_index] = Villager.get_villager_statements(player_index)
        for k in range(const.NUM_CENTER):
            possible[player_index] += Drunk.get_drunk_statements(player_index, k + const.NUM_PLAYERS)
        for i in range(const.NUM_PLAYERS):
            if player_index != i:
                mason_indices = [player_index, i]
                possible[player_index]+= Mason.get_mason_statements(player_index, mason_indices)

            for j in range(const.NUM_PLAYERS): # Troublemaker should not refer to other wolves or themselves
                if i != j != player_index and i != player_index: #and i not in wolf_indices and j not in wolf_indices:
                    possible[player_index] += Troublemaker.get_troublemaker_statements(player_index, i, j)

            # Wolf-seer more likely to declare they saw a villager
            for role in const.ROLES:
                if role != 'Seer':      # "Hey, I'm a Seer and I saw another Seer..."
                    possible[player_index]+= Seer.get_seer_statements(player_index, i, role)
                if role != 'Wolf':      # "I robbed a Wolf and now I'm a Wolf..."
                    possible[player_index]+= Robber.get_robber_statements(player_index, i, role)
    return possible

### Testing ###
if __name__ == '__main__':
    s = Seer.get_seer_statements(3, 4, 'Villager')
    for statement in s:
        print(statement)
    st = s[0].negate()
    print(st)
