class Statement:
    def __init__(self, str, info):
        self.str = str
        self.info = info
        
    def negate(self):
        # returns a new negated statement
        return Statement()

def get_villager_statements(player_ind):
    return {Statement('I am a villager' , (player_ind, 'V'))}

# TODO fill these in
def get_seer_statements(player_ind, seen_ind, role):
    pass
# def getSeerStatement(index, role):
#     return "I am a Seer and I saw that Player " + str(index) + " was a " + str(role) + "."

def get_wolf_statements(player_ind):
    # TODO call above two functions
    # for index in range(self.NUM_PLAYERS):
    #     for role in self.ROLES:
    #         self.statements.append(self.getSeerStatement(index, role))

    pass

if __name__ == '__main__':
    s = get_villager_statements(4)
    print(type(s))
    for hi in s:
        print(hi.str, hi.info)
