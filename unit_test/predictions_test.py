''' predictions_test.py '''
from src import predictions, const
from src.algorithms import SolverState

class TestMakeRandomPrediction:
    ''' Tests for the random_prediction function. '''

    @staticmethod
    def test_random_prediction(medium_game_roles):
        ''' Should return a random shuffled list as the predicted roles. '''
        const.ROLES = medium_game_roles

        result = predictions.make_random_prediction()

        assert result == ['Seer', 'Wolf', 'Drunk', 'Robber', 'Minion', 'Troublemaker']


class TestMakeEvilPrediction:
    ''' Tests for the make_evil_prediction function. '''

    @staticmethod
    def test_random_evil_prediction(medium_game_roles):
        ''' Should give a random prediction when an empty SolverState is passed in. '''
        const.ROLES = medium_game_roles
        solution_arr = [SolverState([])]

        result = predictions.make_evil_prediction(solution_arr)

        assert result == ['Seer', 'Wolf', 'Drunk', 'Robber', 'Minion', 'Troublemaker']

    @staticmethod
    def test_evil_prediction(example_medium_solverstate_list):
        ''' Should give a random prediction when an empty SolverState is passed in. '''
        result = predictions.make_evil_prediction(example_medium_solverstate_list)

        assert result == ['Seer', 'Minion', 'Troublemaker', 'Drunk', 'Wolf', 'Robber']


class TestMakeUnrestrictedPrediction:
    ''' Tests for the make_unrestricted_prediction function. '''

    @staticmethod
    def test_empty_unrestricted_prediction(medium_game_roles):
        ''' Should return an empty list to denote that no prediction could be made. '''
        const.ROLES = medium_game_roles
        solution = SolverState([])

        result = predictions.make_unrestricted_prediction(solution)

        assert result == []

    @staticmethod
    def test_unrestricted_prediction(example_medium_solverstate):
        ''' Should return a list of predictions without requiring adherence to possible sets. '''
        result = predictions.make_unrestricted_prediction(example_medium_solverstate)

        assert result == ['Seer', 'Troublemaker', 'Wolf', 'Minion', 'Robber', 'Drunk']


class TestMakePrediction:
    ''' Tests for the make_prediction function. '''

    @staticmethod
    def test_make_evil_prediction(example_medium_solverstate_list):
        ''' Should return evil prediction when is_evil=True. '''
        result = predictions.make_prediction(example_medium_solverstate_list, True)

        assert result == ['Seer', 'Minion', 'Troublemaker', 'Drunk', 'Wolf', 'Robber']

    @staticmethod
    def test_make_prediction(example_medium_solverstate_list):
        ''' Should return valid prediction for villager players. '''
        result = predictions.make_prediction(example_medium_solverstate_list, False)

        assert result == ['Robber', 'Seer', 'Troublemaker', 'Minion', 'Wolf', 'Drunk']


class TestGetBasicGuesses:
    ''' Tests for the get_basic_guesses function. '''

    @staticmethod
    def test_basic_guesses_small(example_small_solverstate):
        '''
        Should correctly interpret a solution as a list of current predictions
        as well as a dictionary of counts.
        '''
        result = predictions.get_basic_guesses(example_small_solverstate)

        assert result == (['Seer', '', 'Robber'], {'Robber': 0, 'Seer': 0, 'Villager': 1})

    @staticmethod
    def test_basic_guesses_medium(example_medium_solverstate):
        '''
        Should correctly interpret a solution as a list of current predictions
        as well as a dictionary of counts.
        '''
        expected = (['Seer', '', 'Drunk', '', '', ''],
                    {'Drunk': 0, 'Minion': 1, 'Robber': 1, 'Seer': 0, 'Troublemaker': 1, 'Wolf': 1})

        result = predictions.get_basic_guesses(example_medium_solverstate)

        assert result == expected

    @staticmethod
    def test_basic_guesses_large(example_large_solverstate):
        '''
        Should correctly interpret a solution as a list of current predictions
        as well as a dictionary of counts.
        '''
        expected = (['Robber', 'Minion', 'Seer', 'Villager', 'Mason', 'Mason', 'Drunk',
                     'Tanner', '', '', '', '', '', '', ''],
                    {'Drunk': 0, 'Hunter': 1, 'Insomniac': 1, 'Mason': 0, 'Minion': 0, 'Robber': 0,
                     'Seer': 0, 'Tanner': 0, 'Troublemaker': 1, 'Villager': 2, 'Wolf': 2})

        result = predictions.get_basic_guesses(example_large_solverstate)

        assert result == expected


class TestRecurseAssign:
    ''' Tests for the recurse_assign function. '''

    @staticmethod
    def test_no_action(example_small_solverstate, small_game_roles):
        ''' Should not make any assignments if all assignments are made. '''
        counts = {'Robber': 0, 'Seer': 0, 'Villager': 0}

        result = predictions.recurse_assign(example_small_solverstate,
                                            small_game_roles,
                                            counts)

        assert result == small_game_roles

    @staticmethod
    def test_no_solution_medium(example_medium_solverstate):
        ''' Should return empty list if no arrangement of assignments is valid. '''
        # TODO start writing this test
        role_guesses = ['Robber', '', 'Seer', 'Villager', 'Mason', 'Mason', 'Drunk',
                        '', '', '', '', '', '', '', '']
        counts = {'Drunk': 0, 'Hunter': 1, 'Insomniac': 1, 'Mason': 0, 'Minion': 1, 'Robber': 0,
                  'Seer': 0, 'Tanner': 1, 'Troublemaker': 1, 'Villager': 2, 'Wolf': 2}

        result = predictions.recurse_assign(example_medium_solverstate,
                                            role_guesses,
                                            counts)

        assert result == []

    @staticmethod
    def test_small_predict_solution(example_small_solverstate):
        ''' Should return empty list if no arrangement of assignments is valid. '''
        role_guesses = ['Seer', '', 'Robber']
        counts = {'Robber': 0, 'Seer': 0, 'Villager': 1}

        result = predictions.recurse_assign(example_small_solverstate,
                                            role_guesses,
                                            counts)

        assert result == ['Seer', 'Villager', 'Robber']

    @staticmethod
    def test_medium_predict_solution(example_medium_solverstate):
        ''' Should return empty list if no arrangement of assignments is valid. '''
        role_guesses = ['Seer', '', 'Drunk', '', '', '']
        counts = {'Drunk': 0, 'Minion': 1, 'Robber': 1, 'Seer': 0, 'Troublemaker': 1, 'Wolf': 1}

        result = predictions.recurse_assign(example_medium_solverstate,
                                            role_guesses,
                                            counts)

        assert result == ['Seer', 'Troublemaker', 'Drunk', 'Minion', 'Wolf', 'Robber']

    @staticmethod
    def test_large_predict_solution(example_large_solverstate):
        ''' Should return empty list if no arrangement of assignments is valid. '''
        role_guesses = ['Robber', '', 'Seer', 'Villager', 'Mason', 'Mason', 'Drunk',
                        '', '', '', '', '', '', '', '']
        counts = {'Drunk': 0, 'Hunter': 1, 'Insomniac': 1, 'Mason': 0, 'Minion': 1, 'Robber': 0,
                  'Seer': 0, 'Tanner': 1, 'Troublemaker': 1, 'Villager': 2, 'Wolf': 2}

        result = predictions.recurse_assign(example_large_solverstate,
                                            role_guesses,
                                            counts)

        assert result == ['Robber', 'Troublemaker', 'Seer', 'Villager', 'Mason', 'Mason',
                          'Drunk', 'Wolf', 'Tanner', 'Hunter', 'Minion', 'Insomniac', 'Villager',
                          'Villager', 'Wolf']


class TestGetSwitchDict:
    ''' Tests for the get_switch_dict function. '''

    @staticmethod
    def test_get_empty_switch_dict(small_game_roles):
        ''' Should return the identity switch dict. '''
        const.ROLES = small_game_roles
        possible_roles = [{'Robber', 'Villager', 'Seer'}] * 3
        state = SolverState(possible_roles)

        result = predictions.get_switch_dict(state)

        assert result == {i: i for i in range(const.NUM_ROLES)}

    @staticmethod
    def test_get_switch_dict(example_large_solverstate):
        ''' Should return the correct switch dict for a SolverState result. '''
        expected = {i: i for i in range(const.NUM_ROLES)}
        expected[6] = 9
        expected[0] = 6
        expected[9] = 0

        result = predictions.get_switch_dict(example_large_solverstate)

        assert result == expected


class TestPrintGuesses:
    ''' Tests for the print_guesses function. '''

    @staticmethod
    def test_print_guesses(caplog, medium_game_roles):
        ''' Correctly print and format roles. '''
        const.ROLES = medium_game_roles

        predictions.print_guesses(list(medium_game_roles))

        captured = caplog.records[0].getMessage()
        expected = '\n[Wolfbot] Role guesses: [Robber, Drunk, Wolf, Troublemaker, Seer]\n' + \
                   '          Center cards: [Minion]\n'
        assert captured == expected
