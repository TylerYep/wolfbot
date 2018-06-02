from roles import Player, Villager, Mason, Seer, Robber, Troublemaker, Drunk, Insomniac
from algorithms import switching_solver, SolverState, is_consistent
from predictions import make_predictions
from possible import get_possible_statements
from statements import Statement
from const import logger
import const
import pickle
from copy import deepcopy
import random

class Wolf(Player):
    def __init__(self, player_index, wolf_indices):
        super().__init__(player_index)
        self.role = 'Wolf'
        self.statements = self.get_wolf_statements(player_index, wolf_indices)
        self.wolf_indices = wolf_indices
        if const.USE_WOLF_RL:
            with open(const.EXPERIENCE_PATH, 'rb') as f:
                self.experience = pickle.load(f)

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

    def get_statement(self, stated_roles, previous_statements):
        if const.USE_WOLF_RL:
            return self.get_statement_rl(previous_statements)
        elif const.USE_WOLF_AI and self.player not in [0, 1]:
            return self.get_statement_expectimax(stated_roles, previous_statements)
        else:
            return super().get_statement()

    def get_statement_rl(self, previous_statements):
        state = (tuple(self.wolf_indices), tuple([s.sentence for s in previous_statements]))
        scores = self.experience[state]
        choice = None
        best_score = -100
        for potential_statement, score in scores.items():
            if score > best_score:
                best_score = score
                choice = potential_statement
        if choice is None:
            return super().get_statement()
        for statement in self.statements:
            if choice == statement.sentence:
                return statement

    def get_statement_expectimax(self, stated_roles, previous_statements):
        possible_statements = get_possible_statements(self.wolf_indices)

        # wolves in a positions - # of ones that are actually wolves, size of set
        def eval(solver_result, predictions):
            ''' Evaluates a complete or incomplete game. '''
            val = 10 * const.EVAL_UNIT
            if len(predictions) == 0: return -10 * const.EVAL_UNIT
            for wolfi in self.wolf_indices:
                if predictions[wolfi] == 'Wolf':
                    val -= 5 * const.EVAL_UNIT
            return val

        def _get_next_vals(statement_list, actions, state, ind, depth, is_wolf=False):
            ''' Evaluate current state (value of consistent statements) and return values. '''
            values = []
            for statement in actions:
                if is_wolf: new_state = state # If you're the wolf, let yourself be inconsistent (each state needs a value)
                else: new_state = is_consistent(statement, state)
                if new_state:
                    new_statements = deepcopy(statement_list) + [statement]
                    values.append(expectimax(new_statements, new_state, ind + 1, depth - 1))
            return [v[0] for v in values]

        def expectimax(statement_list, state, ind, depth=None):
            ''' Runs expectimax on the list of statements and the current state using the given depth. '''
            if ind == const.NUM_PLAYERS or depth == 0:
                solver_result = switching_solver(statement_list)
                predictions = make_predictions(solver_result)
                return eval(solver_result, predictions), None
            if ind == self.player:              # Choose your own move, maximize val
                indices = random.sample(range(len(self.statements)), const.BRANCH_FACTOR * self.player)
                trimmed_statements = [self.statements[i] for i in sorted(indices)]
                vals = _get_next_vals(statement_list, trimmed_statements, state, ind, depth, True)
                best_move = self.statements[vals.index(max(vals))]
                if len(vals) == 0: return -5 * const.EVAL_UNIT, super.getNextStatement()
                return max(vals), best_move
            else:                               # Get expected value of remaining statements
                indices = random.sample(range(len(possible_statements[ind])), const.BRANCH_FACTOR * self.player)
                trimmed_statements = [possible_statements[ind][i] for i in sorted(indices)]
                vals = _get_next_vals(statement_list, trimmed_statements, state, ind, depth)
                if len(vals) == 0: return 10 * const.EVAL_UNIT, None
                return sum(vals) / len(vals), None

        possible_roles = [deepcopy(const.ROLE_SET) for i in range(const.NUM_ROLES)]
        start_state = SolverState(possible_roles, [])
        for i in range(self.player):
            if i not in self.wolf_indices:
                st = is_consistent(previous_statements[i], start_state)
                if st: start_state = st
        print("player index: ", self.player)
        best_val, best_move =  expectimax(previous_statements, start_state, self.player, const.EXPECTIMAX_DEPTH)
        return best_move
