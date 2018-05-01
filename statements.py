class Statement:
    def __init__(self, str, info):
        self.str = str
        self.info = info

def get_villager_statements(player_ind):
    return {Statement('I am a villager' , (player_ind, 'V'))}

# TODO fill these in
def get_seer_statements(player_ind):
    pass

def get_wolf_statements(player_ind):
    # TODO call above two functions
    pass

s = get_villager_statements(4)
print(type(s))
for hi in s:
    print(hi.str, hi.info)
