""" voting_test.py """
import random

from conftest import verify_output, verify_output_string
from src import const, voting
from src.roles import Drunk, Minion, Robber, Seer, Villager, Wolf
from src.stats import GameResult


class TestConsolidateResults:
    """ Tests for the consolidate_results function. """

    @staticmethod
    def test_consolidate_without_voting_small(caplog, example_small_saved_game):
        """ Should return a final GameResult without voting. """
        const.USE_VOTING = False

        result = voting.consolidate_results(example_small_saved_game)

        expected = (
            "Solver interpretation: (True, True, True)",
            "[WolfBot] Player roles: [Villager, Seer, Robber]",
            "          Center cards: []\n",
        )
        assert result == GameResult(
            ["Villager", "Seer", "Robber"], ["Villager", "Seer", "Robber"], []
        )
        verify_output(caplog, expected)

    @staticmethod
    def test_consolidate_without_voting_medium(caplog, example_medium_saved_game):
        """ Should return a final GameResult without voting. """
        const.USE_VOTING = False

        result = voting.consolidate_results(example_medium_saved_game)

        expected = (
            "Solver interpretation: (True, True, True, False, False)",
            "Solver interpretation: (True, False, True, True, False)",
            "Solver interpretation: (False, False, True, True, True)",
            "[WolfBot] Player roles: [Robber, Seer, Troublemaker, Minion, Wolf]",
            "          Center cards: [Drunk]\n",
        )
        assert result == GameResult(
            ["Seer", "Wolf", "Troublemaker", "Drunk", "Minion", "Robber"],
            ["Robber", "Seer", "Troublemaker", "Minion", "Wolf", "Drunk"],
            [1],
        )
        verify_output(caplog, expected)

    @staticmethod
    def test_consolidate_with_voting_medium(example_medium_saved_game):
        """ Should return a final GameResult with voting. """
        result = voting.consolidate_results(example_medium_saved_game)

        assert result == GameResult(
            ["Seer", "Wolf", "Troublemaker", "Drunk", "Minion", "Robber"],
            ["Minion", "Wolf", "Troublemaker", "Drunk", "Seer", "Robber"],
            [1],
            "Villager",
        )


class TestIsPlayerEvil:
    """ Tests for the is_player_evil function. """

    @staticmethod
    def test_no_evil_player(small_game_roles):
        """ Should determine if a player has turned evil after night falls. """
        const.ROLES = small_game_roles
        player_list = [Villager(0), Robber(1, 2, "Seer"), Seer(2, (1, "Robber"), (None, None))]

        result = voting.is_player_evil(player_list, 0, [])

        assert result is False

    @staticmethod
    def test_find_evil_players(medium_game_roles):
        """ Should determine if a player has turned evil after night falls. """
        const.ROLES = medium_game_roles
        player_list = [
            Seer(0, (2, "Drunk"), (None, None)),
            Wolf(1, [1], 5, "Troublemaker"),
            Drunk(2, 5),
            Robber(3, 2, "Drunk"),
            Minion(4, [1]),
        ]

        result = [voting.is_player_evil(player_list, i, [1]) for i in range(len(player_list))]

        assert result == [False, True, False, False, True]

    @staticmethod
    def test_turned_evil_player(medium_game_roles):
        """ Should determine if a player has turned evil after night falls. """
        const.ROLES = medium_game_roles
        player_list = [
            Seer(0, (2, "Drunk"), (None, None)),
            Wolf(1, [1], 5, "Troublemaker"),
            Drunk(2, 5),
            Robber(3, 1, "Wolf"),
            Minion(4, [1]),
        ]

        result = voting.is_player_evil(player_list, 3, [1])

        assert result is True


class TestGetIndividualPreds:
    """ Tests for the get_individual_preds function. """

    @staticmethod
    def test_medium_individual_preds(medium_game_roles, medium_statement_list):
        """ Should get the individual predictions for all players. """
        const.ROLES = medium_game_roles
        player_objs = [
            Seer(0, (2, "Drunk")),
            Wolf(1, [1], 5, "Troublemaker"),
            Drunk(2, 5),
            Robber(3, 1, "Wolf"),
            Minion(4, [1]),
        ]

        result = voting.get_individual_preds(player_objs, medium_statement_list, [1])

        assert result == [
            ["Seer", "Wolf", "Troublemaker", "Drunk", "Minion", "Robber"],
            ["Wolf", "Seer", "Robber", "Minion", "Troublemaker", "Drunk"],
            ["Seer", "Wolf", "Troublemaker", "Drunk", "Minion", "Robber"],
            ["Wolf", "Minion", "Troublemaker", "Drunk", "Seer", "Robber"],
            ["Wolf", "Minion", "Troublemaker", "Drunk", "Seer", "Robber"],
        ]


class TestGetVotingResult:
    """ Tests for the get_voting_result function. """

    @staticmethod
    def test_small_voting_result(caplog, small_game_roles):
        """ Should get voting results from the individual predictions. """
        const.ROLES = small_game_roles
        indiv_preds = [["Villager", "Seer", "Robber"]] * 3

        result = voting.get_voting_result(indiv_preds)

        assert result == (["Villager", "Seer", "Robber"], [1.0] * 3, [0, 1, 2], [1, 2, 0])
        verify_output_string(caplog, "\nVote Array: [1, 1, 1]\n")

    @staticmethod
    def test_medium_voting_result(caplog, medium_game_roles):
        """ Should get voting results from the individual predictions. """
        const.ROLES = medium_game_roles
        indiv_preds = [
            ["Seer", "Wolf", "Troublemaker", "Drunk", "Minion", "Robber"],
            ["Wolf", "Seer", "Robber", "Minion", "Troublemaker", "Drunk"],
            ["Seer", "Wolf", "Troublemaker", "Drunk", "Minion", "Robber"],
            ["Wolf", "Minion", "Troublemaker", "Drunk", "Seer", "Robber"],
            ["Wolf", "Minion", "Troublemaker", "Drunk", "Seer", "Robber"],
        ]

        result = voting.get_voting_result(indiv_preds)

        assert result == (
            ["Seer", "Wolf", "Troublemaker", "Drunk", "Minion", "Robber"],
            [0.6, 0.4, 0.8, 0.8, 0.4, 0.8],
            [0],
            [1, 0, 1, 0, 0],
        )
        verify_output_string(caplog, "\nVote Array: [3, 2, 0, 0, 0]\n")

    @staticmethod
    def test_large_voting_result(caplog, large_game_roles, large_individual_preds):
        """ Should get voting results from the individual predictions. """
        const.ROLES = large_game_roles
        random.shuffle(large_individual_preds)

        result = voting.get_voting_result(large_individual_preds)

        assert result == (
            [
                "Villager",
                "Insomniac",
                "Mason",
                "Tanner",
                "Villager",
                "Drunk",
                "Seer",
                "Minion",
                "Wolf",
                "Villager",
                "Wolf",
                "Hunter",
                "Troublemaker",
                "Mason",
                "Robber",
            ],
            [
                1.0,
                2 / 3,
                1.0,
                5 / 12,
                1.0,
                0.75,
                0.5,
                5 / 12,
                5 / 12,
                7 / 12,
                7 / 12,
                11 / 12,
                0.5,
                2 / 3,
                0.75,
            ],
            [3, 10],
            [8, 10, 1, 9, 5, 7, 5, 3, 3, 10, 10, 3],
        )
        verify_output_string(caplog, "\nVote Array: [0, 1, 0, 3, 0, 2, 0, 1, 1, 1, 3, 0]\n")


class TestEvalFinalGuesses:
    """ Tests for the eval_final_guesses function. """

    @staticmethod
    def test_werewolf_wins(caplog, medium_game_roles):
        """ Should declare Werewolf victory if no wolves are found, but one exists. """
        const.ROLES = medium_game_roles
        guessed_wolf_inds = list(range(const.NUM_PLAYERS))
        vote_inds = [1] * const.NUM_PLAYERS

        result = voting.eval_final_guesses(medium_game_roles, guessed_wolf_inds, vote_inds)

        expected = (
            "No wolves were found.",
            "But Player(s) [2] was a Wolf!\n",
            "Werewolf Team wins!",
        )
        assert result == "Werewolf"
        verify_output(caplog, expected)

    @staticmethod
    def test_village_wins_no_wolf(caplog, small_game_roles):
        """ Should declare Villager victory if no wolves are found, and there are none. """
        const.ROLES = small_game_roles
        guessed_wolf_inds = list(range(const.NUM_PLAYERS))
        vote_inds = [1] * const.NUM_PLAYERS

        result = voting.eval_final_guesses(small_game_roles, guessed_wolf_inds, vote_inds)

        expected = ("No wolves were found.", "That was correct!\n", "Village Team wins!")
        assert result == "Villager"
        verify_output(caplog, expected)

    @staticmethod
    def test_village_wins_found_wolf(caplog, medium_game_roles):
        """ Should declare Villager victory if no wolves are found, and there are none. """
        const.ROLES = medium_game_roles
        guessed_wolf_inds = [2]
        vote_inds = [1, 2, 2, 2, 1]

        result = voting.eval_final_guesses(medium_game_roles, guessed_wolf_inds, vote_inds)

        expected = (
            "Player 2 was chosen as a Wolf.",
            "Player 2 was a Wolf!\n",
            "Village Team wins!",
        )
        assert result == "Villager"
        verify_output(caplog, expected)

    @staticmethod
    def test_hunter_wins(caplog, large_game_roles):
        """
        Should declare Village victory if no wolves are found,
        Hunter is killed, and Hunter voted for a true Wolf.
        """
        const.ROLES = large_game_roles[::-1]
        guessed_wolf_inds = [0, 9]
        vote_inds = [7, 10, 0, 9, 7, 9, 7, 7, 7, 0, 0, 0]
        expected = (
            "(Player 0) Hunter died and killed Player 7 too!\n",
            "Player 0 was chosen as a Wolf.",
            "Player 0 was a Hunter!\n",
            "Player 9 was chosen as a Wolf.",
            "Player 9 was a Tanner!\n",
            "Player 7 was chosen as a Wolf.",
            "Player 7 was a Wolf!\n",
            "Village Team wins!",
        )

        result = voting.eval_final_guesses(const.ROLES, guessed_wolf_inds, vote_inds)

        assert result == "Villager"
        verify_output(caplog, expected)

    @staticmethod
    def test_tanner_wins(caplog, large_game_roles):
        """ Should declare Tanner victory if no wolves are found, and Tanner was chosen. """
        const.ROLES = large_game_roles
        guessed_wolf_inds = [2, 5]
        vote_inds = [8, 7, 1, 9, 5, 10, 5, 3, 3, 10, 10, 3]

        result = voting.eval_final_guesses(large_game_roles, guessed_wolf_inds, vote_inds)

        expected = (
            "Player 2 was chosen as a Wolf.",
            "Player 2 was a Robber!\n",
            "Player 5 was chosen as a Wolf.",
            "Player 5 was a Tanner!\n",
            "Tanner wins!",
        )
        assert result == "Tanner"
        verify_output(caplog, expected)


class TestGetPlayerVote:
    """ Tests for the get_player_vote function. """

    @staticmethod
    def test_vote_for_wolf(medium_game_roles):
        """ If a player suspects a Wolf, they should vote for that player. """
        const.ROLES = medium_game_roles
        prediction = ["Seer", "Wolf", "Troublemaker", "Drunk", "Minion", "Robber"]

        result = voting.get_player_vote(2, prediction)

        assert result == 1

    @staticmethod
    def test_no_vote_for_center_wolf(medium_game_roles):
        """ If a player suspects a Wolf in the center, they should not vote for that player. """
        const.ROLES = medium_game_roles
        prediction = ["Seer", "Troublemaker", "Drunk", "Minion", "Robber", "Wolf"]

        result = voting.get_player_vote(2, prediction)

        assert result == 3

    @staticmethod
    def test_vote_right(small_game_roles):
        """ If no Wolves are found, players should vote for the person to their right. """
        const.ROLES = small_game_roles
        prediction = ["Villager", "Seer", "Robber"]

        result = [voting.get_player_vote(i, prediction) for i in range(const.NUM_PLAYERS)]

        assert result == [1, 2, 0]

    @staticmethod
    def test_interactive_vote(monkeypatch, medium_game_roles):
        """ Prompt the user for their vote. """
        player_index = 2
        const.ROLES = medium_game_roles
        const.IS_USER[player_index] = True
        prediction = ["Seer", "Troublemaker", "Drunk", "Minion", "Robber", "Wolf"]
        monkeypatch.setattr("builtins.input", lambda x: "4")

        result = voting.get_player_vote(player_index, prediction)

        assert result == 4
