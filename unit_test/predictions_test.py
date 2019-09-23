''' predictions_test.py '''
from src import predictions, const

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
    def test_basic_guesses(self):
        ''' Should initialize a SolverState. '''
        pass


class TestRecurseAssign:
    def test_recurse_assign(self):
        ''' Should initialize a SolverState. '''
        pass


class TestGetSwitchDict:
    def test_get_switch_dict(self):
        ''' Should initialize a SolverState. '''
        pass


class TestPrintGuesses:
    def test_print_guesses(self, caplog, medium_game_roles):
        ''' Correctly print and format roles. '''
        const.ROLES = medium_game_roles
        predictions.print_guesses(list(medium_game_roles))

        captured = caplog.records[0].getMessage()
        expected = '\n[Wolfbot] Role guesses: [Robber, Drunk, Wolf, Troublemaker, Seer]\n' + \
                   '          Center cards: [Minion]\n'
        assert captured == expected
