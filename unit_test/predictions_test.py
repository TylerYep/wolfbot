''' predictions_test.py '''
from src import predictions, const
from src.algorithms import SolverState

class TestMakeRandomPrediction:
    def test_random_prediction(self, medium_game_roles):
        ''' Should return a random shuffled list as the predicted roles. '''
        const.ROLES = medium_game_roles

        result = predictions.make_random_prediction()

        assert result == ['Seer', 'Wolf', 'Drunk', 'Robber', 'Minion', 'Troublemaker']


class TestMakeEvilPrediction:
    def test_evil_prediction(self):
        ''' Should initialize a SolverState. '''
        pass


class TestMakeFastPrediction:
    def test_fast_prediction(self):
        ''' Should initialize a SolverState. '''
        pass


class TestMakePrediction:
    def test_make_prediction(self):
        ''' Should initialize a SolverState. '''
        pass


class TestGetBasicGuesses:
    def test_basic_guesses_small(self, example_small_solverstate):
        '''
        Should correctly interpret a solution as a list of current predictions
        as well as a dictionary of counts.
        '''
        result = predictions.get_basic_guesses(example_small_solverstate)

        assert result == (['Seer', '', 'Robber'], {'Robber': 0, 'Seer': 0, 'Villager': 1})

    def test_basic_guesses_medium(self, example_medium_solverstate):
        '''
        Should correctly interpret a solution as a list of current predictions
        as well as a dictionary of counts.
        '''
        result = predictions.get_basic_guesses(example_medium_solverstate)
        expected = (['Seer', '', 'Drunk', '', '', ''],
                    {'Drunk': 0, 'Minion': 1, 'Robber': 1, 'Seer': 0, 'Troublemaker': 1, 'Wolf': 1})

        assert result == expected

    def test_basic_guesses_large(self, example_large_solverstate):
        '''
        Should correctly interpret a solution as a list of current predictions
        as well as a dictionary of counts.
        '''
        result = predictions.get_basic_guesses(example_large_solverstate)
        expected = (['Robber', 'Minion', 'Seer', 'Villager', 'Mason', 'Mason', 'Drunk', 'Wolf',
                     '', '', '', '', '', '', ''],
                    {'Wolf': 1, 'Villager': 2, 'Robber': 0, 'Seer': 0, 'Tanner': 1, 'Mason': 0,
                     'Minion': 0, 'Drunk': 0, 'Troublemaker': 1, 'Insomniac': 1, 'Hunter': 1})

        assert result == expected


class TestRecurseAssign:
    def test_recurse_assign(self):
        ''' Should initialize a SolverState. '''
        pass


class TestGetSwitchDict:
    def test_get_empty_switch_dict(self, small_game_roles):
        ''' Should return the identity switch dict. '''
        possible_roles = (frozenset({'Robber', 'Villager', 'Seer'}),) * 3
        state = SolverState(possible_roles)

        result = predictions.get_switch_dict(state)

        assert result == {i: i for i in range(const.NUM_ROLES)}

    def test_get_switch_dict(self, example_large_solverstate):
        ''' Should return the correct switch dict for a SolverState result. '''
        expected = {i: i for i in range(const.NUM_ROLES)}
        expected[6] = 9
        expected[0] = 6
        expected[9] = 0

        result = predictions.get_switch_dict(example_large_solverstate)

        assert result == expected

class TestPrintGuesses:
    def test_print_guesses(self, caplog, medium_game_roles):
        ''' Correctly print and format roles. '''
        const.ROLES = medium_game_roles
        predictions.print_guesses(list(medium_game_roles))

        captured = caplog.records[0].getMessage()
        expected = '\n[Wolfbot] Role guesses: [Robber, Drunk, Wolf, Troublemaker, Seer]\n' + \
                   '          Center cards: [Minion]\n'
        assert captured == expected
