from roles import Player, Villager, Mason, Seer, Robber, Troublemaker, Drunk, Insomniac
from copy import deepcopy
from algorithms import switching_solver, SolverState, is_consistent
from predictions import make_predictions
from statements import Statement
from const import logger
import const
import pickle
from pprint import pprint
import random

class Wolf(Player):
    def __init__(self, player_index, wolf_indices):
        super().__init__(player_index)
        self.role = 'Wolf'
        self.statements = self.get_wolf_statements(player_index, wolf_indices)
        self.wolf_indices = wolf_indices

    @staticmethod
    def get_wolf_statements(player_index, wolf_indices):
        statements = []
        if 'Villager' in const.ROLE_SET:
            statements += Villager.get_villager_statements(player_index)
        if 'Insomniac' in const.ROLE_SET:
            for role in const.ROLES:
                if role != 'Wolf':
                    statements += Insomniac.get_insomniac_statements(player_index, role)
        if 'Mason' in const.ROLE_SET:
            statements += Mason.get_mason_statements(player_index, [player_index])
            for i in range(const.NUM_PLAYERS):
                if player_index != i:
                    mason_indices = [player_index, i]
                    statements += Mason.get_mason_statements(player_index, mason_indices)
        if 'Drunk' in const.ROLE_SET:
            for k in range(const.NUM_CENTER):
                statements += Drunk.get_drunk_statements(player_index, k + const.NUM_PLAYERS)
        if 'Troublemaker' in const.ROLE_SET:
            for i in range(const.NUM_PLAYERS):
                for j in range(i+1, const.NUM_PLAYERS):
                    # Troublemaker should not refer to other wolves or themselves
                    if i != j != player_index and i != player_index and i not in wolf_indices and j not in wolf_indices:
                        statements += Troublemaker.get_troublemaker_statements(player_index, i, j)
        if 'Robber' in const.ROLE_SET:
            for i in range(const.NUM_PLAYERS):
                for role in const.ROLES:
                    if role != 'Wolf':      # "I robbed Player 0 and now I'm a Wolf..."
                        statements += Robber.get_robber_statements(player_index, i, role)
        if 'Seer' in const.ROLE_SET:
            for role in const.ROLES:
                for i in range(const.NUM_PLAYERS):
                    if i not in wolf_indices and role != 'Seer':      # "Hey, I'm a Seer and I saw another Seer..."
                        statements += Seer.get_seer_statements(player_index, i, role, None, None)
            # Wolf using these usually gives himself away
            for c1 in range(const.NUM_CENTER):
                for c2 in range(c1 + 1, const.NUM_CENTER):
                    for role1 in const.ROLES:
                        for role2 in const.ROLES:
                            if role1 != 'Seer' and role2 != 'Seer' and c1 != c2:
                                if role1 != role2 or const.ROLE_COUNTS[role1] >= 2:
                                    statements += Seer.get_seer_statements(player_index,
                                            c1  + const.NUM_PLAYERS, role1, c2 + const.NUM_PLAYERS, role2)
        return statements

    def getNextStatement(self, stated_roles, previous_statements, possible_statements):
        #return super().getNextStatement()
        def eval(solution):
            val = 5
            if len(solution) == 0:
                return -10
            for wolfi in self.wolf_indices:
                if solution[wolfi] == 'Wolf':
                    val -= 5
            return val

        def _get_next_vals(statement_list, actions, state, ind, depth, is_wolf=False):
            values = []
            for statement in actions:
                if is_wolf: new_state = state #If you're the wolf, let yourself be inconsistent (also we need a value for each state)_
                else: new_state = is_consistent(statement, state)
                if new_state:
                    values.append(expectimax(deepcopy(statement_list) + [statement], new_state, ind+1, depth - 1))
            return [v[0] for v in values]

        def expectimax(statement_list, state, ind, depth=None):
            if ind == const.NUM_PLAYERS:
                sol = switching_solver(statement_list)
                solution = make_predictions(sol)
                return eval(solution), None
            if ind == self.player:              # It's Me
                vals = _get_next_vals(statement_list, self.statements, state, ind, depth, True)
                best_move = self.statements[vals.index(max(vals))]
                return max(vals), best_move
            else:           # If he's the other wolf, he can also say anything... TODO make them play as a team?
                vals = _get_next_vals(statement_list, possible_statements[ind], state, ind, depth)
                if len(vals) == 0: return 10, None
                return sum(vals) / len(vals), None
        
        possible_roles = [deepcopy(const.ROLE_SET) for i in range(const.NUM_ROLES)]
        start_state = SolverState(possible_roles, [])
        for i in range(self.player):
            if i not in self.wolf_indices:
                start_state = is_consistent(previous_statements[i], start_state)
        #best_val, best_move =  expectimax(previous_statements, self.player, 5)
        best_val, best_move =  expectimax(previous_statements, start_state, self.player, 5)
        return best_move

#possib = get_possible_statements()
#pprint.pprint(possib)
#
