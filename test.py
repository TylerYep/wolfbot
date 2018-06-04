from roles import Villager, Mason, Seer, Robber, Troublemaker, Drunk, Insomniac
from wolf import Wolf
import const
from algorithms import is_consistent, SolverState
from copy import deepcopy
#possible_roles = [deepcopy(const.ROLE_SET) for i in range(const.NUM_ROLES)]
#start_state = SolverState(possible_roles, [])
#
#statements = []
#statements.extend(Seer.get_seer_statements(0, 0  + const.NUM_PLAYERS, 'Mason', 1 + const.NUM_PLAYERS, 'Villager'))
#statements.extend(Drunk.get_drunk_statements(1, const.NUM_PLAYERS))
#for statement in statements:
#    start_state = is_consistent(statement, start_state)
#    print(start_state)

for i in range(100):
    try:
        if i%10 == 0:
            print(1/0)
    except:
        print('something went wrong')
