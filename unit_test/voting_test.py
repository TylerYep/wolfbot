''' voting_test.py '''
from src import voting, const
from src.stats import GameResult
from src.roles import Drunk, Minion, Seer, Robber, Villager, Wolf

class TestConsolidateResults:
    ''' Tests for the consolidate_results function. '''

    @staticmethod
    def test_consolidate_without_voting_small(caplog, example_small_saved_game):
        ''' Should return a final GameResult without voting. '''
        const.USE_VOTING = False

        result = voting.consolidate_results(example_small_saved_game)

        assert result == GameResult(['Villager', 'Seer', 'Robber'],
                                    ['Villager', 'Seer', 'Robber'],
                                    [])
        captured = tuple(map(lambda x: x.getMessage(), caplog.records))
        expected = ('Solver interpretation: (True, True, True)\n',
                    '[Wolfbot] Role guesses: [Villager, Seer, Robber]',
                    '          Center cards: []\n')
        assert '\n'.join(captured) == '\n'.join(expected)

    @staticmethod
    def test_consolidate_without_voting_medium(caplog, example_medium_saved_game):
        ''' Should return a final GameResult without voting. '''
        const.USE_VOTING = False

        result = voting.consolidate_results(example_medium_saved_game)

        captured = tuple(map(lambda x: x.getMessage(), caplog.records))
        assert result == GameResult(['Seer', 'Wolf', 'Troublemaker', 'Drunk', 'Minion', 'Robber'],
                                    ['Robber', 'Seer', 'Troublemaker', 'Minion', 'Wolf', 'Drunk'],
                                    [1])
        expected = ('Solver interpretation: (True, True, True, False, False)',
                    'Solver interpretation: (True, False, True, True, False)',
                    'Solver interpretation: (False, False, True, True, True)\n',
                    '[Wolfbot] Role guesses: [Robber, Seer, Troublemaker, Minion, Wolf]',
                    '          Center cards: [Drunk]\n')
        assert '\n'.join(captured) == '\n'.join(expected)

    @staticmethod
    def test_consolidate_with_voting_medium(caplog, example_medium_saved_game):
        ''' Should return a final GameResult with voting. '''
        result = voting.consolidate_results(example_medium_saved_game)

        captured = tuple(map(lambda x: x.getMessage(), caplog.records))
        assert result == GameResult(['Seer', 'Wolf', 'Troublemaker', 'Drunk', 'Minion', 'Robber'],
                                    ['Minion', 'Wolf', 'Troublemaker', 'Drunk', 'Seer', 'Robber'],
                                    [1],
                                    'Villager')
        expected = ('Player prediction: [Robber, Seer, Troublemaker, Minion, Wolf, Drunk]',
                    'Player prediction: [Robber, Seer, Troublemaker, Wolf, Minion, Drunk]',
                    'Player prediction: [Seer, Minion, Troublemaker, Drunk, Wolf, Robber]',
                    'Player prediction: [Minion, Wolf, Troublemaker, Drunk, Seer, Robber]',
                    'Player prediction: [Minion, Wolf, Troublemaker, Drunk, Seer, Robber]',
                    'Vote Array: [0, 2, 0, 1, 2]\n',
                    '[Wolfbot] Role guesses: [Minion, Wolf, Troublemaker, Drunk, Seer]',
                    '          Center cards: [Robber]\n',
                    'Confidence level: [0.4, 0.4, 1.0, 0.6, 0.4, 0.6]',
                    'Player 1 was chosen as a Wolf.',
                    'Player 1 was a Wolf!\n',
                    'Player 4 was chosen as a Wolf.',
                    'Player 4 was a Minion!\n\n'
                    'Village Team wins!')
        assert '\n'.join(captured) == '\n'.join(expected)


class TestIsPlayerEvil:
    ''' Tests for the is_player_evil function. '''

    @staticmethod
    def test_no_evil_player(small_game_roles):
        ''' Should determine if a player has turned evil after night falls. '''
        const.ROLES = small_game_roles
        player_list = [Villager(0), Robber(1, 2, 'Seer'), Seer(2, (1, 'Robber'), (None, None))]

        result = voting.is_player_evil(player_list, 0, [])

        assert result is False

    @staticmethod
    def test_find_evil_players(medium_game_roles):
        ''' Should determine if a player has turned evil after night falls. '''
        const.ROLES = medium_game_roles
        player_list = [Seer(0, (2, 'Drunk'), (None, None)), Wolf(1, [1], 5, 'Troublemaker'),
                       Drunk(2, 5), Robber(3, 2, 'Drunk'), Minion(4, [1])]

        result = [voting.is_player_evil(player_list, i, [1]) for i in range(len(player_list))]

        assert result == [False, True, False, False, True]

    @staticmethod
    def test_turned_evil_player(medium_game_roles):
        ''' Should determine if a player has turned evil after night falls. '''
        const.ROLES = medium_game_roles
        player_list = [Seer(0, (2, 'Drunk'), (None, None)), Wolf(1, [1], 5, 'Troublemaker'),
                       Drunk(2, 5), Robber(3, 1, 'Wolf'), Minion(4, [1])]

        result = voting.is_player_evil(player_list, 3, [1])

        assert result is True


class TestGetIndividualPreds:
    ''' Tests for the get_individual_preds function. '''

    @staticmethod
    def test_get_individual_preds():
        ''' Should initialize a SolverState. '''
        pass


class TestEvalFinalGuesses:
    ''' Tests for the eval_final_guesses function. '''

    @staticmethod
    def test_eval_final_guesses():
        ''' Should initialize a SolverState. '''
        pass


class TestGetVotingResult:
    ''' Tests for the get_voting_result function. '''

    @staticmethod
    def test_get_voting_result():
        ''' Should initialize a SolverState. '''
        pass


class TestGetPlayerVote:
    ''' Tests for the get_player_vote function. '''

    @staticmethod
    def test_get_player_vote():
        ''' Should initialize a SolverState. '''
        pass
