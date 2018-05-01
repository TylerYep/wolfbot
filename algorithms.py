# TODO complete this function.
def is_consistent(statement, state):
    pass

def baseline_solver(statements, n_players):
    def _bl_solver_rec(ind, state):
        if ind == len(statements):
            return 0
        else:
            t_count, f_count = -1*float('inf')
            if is_consistent(statements[ind], state):
                newstate = updateState() #TODO
                t_count = 1 + _bl_solver_rec(ind+1, newstate)
            if is_consistent(statements[ind].negate(), state):
                newstate = updateState() #TODO
                t_count = _bl_solver_rec(ind+1, newstate)
            return max(f_count, t_count)

    state = ['?' for i in range(n_players)]
    _bl_solver_rec(0, state, 0)
