""" one_night_test.py """
import random

from conftest import set_roles, verify_output, verify_output_file, verify_output_string
from src import const, one_night
from src.roles import Drunk, Minion, Player, Robber, Seer, Wolf
from src.stats import GameResult


class TestPlayOneNightWerewolf:
    """ Tests for the play_one_night_werewolf function. """

    @staticmethod
    def test_one_night_small(caplog, example_small_game_result):
        """ Correctly play one round of one night werewolf. """
        result = one_night.play_one_night_werewolf()

        assert result == example_small_game_result
        verify_output_file(caplog, "unit_test/test_data/one_night_small.out")

    @staticmethod
    def test_one_night_medium(caplog, example_medium_game_result):
        """ Correctly play one round of one night werewolf. """
        result = one_night.play_one_night_werewolf()

        assert result == example_medium_game_result
        verify_output_file(caplog, "unit_test/test_data/one_night_medium.out")

    @staticmethod
    def test_one_night_large(caplog, example_large_game_result):
        """ Correctly play one round of one night werewolf. """
        result = one_night.play_one_night_werewolf()

        assert result == example_large_game_result
        verify_output_file(caplog, "unit_test/test_data/one_night_large.out")


# class TestPlayOneNightWerewolfInteractive:
#     """ Tests for the play_one_night_werewolf function. """

#     @staticmethod
#     def test_one_night_small(monkeypatch, example_small_game_result):
#         """ Correctly play one round of one night werewolf. """
#         const.INTERACTIVE_MODE = True
#         monkeypatch.setattr('builtins.input', lambda x: "0")

#         result = one_night.play_one_night_werewolf()

#         assert result == example_small_game_result


class TestConsolidateResults:
    """ Tests for the consolidate_results function. """

    @staticmethod
    def test_consolidate_small(example_small_saved_game):
        """ Should return a final GameResult after voting. """
        result = one_night.consolidate_results(example_small_saved_game)

        assert result == GameResult(
            ["Villager", "Seer", "Robber"], ["Villager", "Seer", "Robber"], [], "Village"
        )

    @staticmethod
    def test_consolidate_medium(example_medium_saved_game):
        """ Should return a final GameResult after voting. """
        result = one_night.consolidate_results(example_medium_saved_game)

        assert result == GameResult(
            ["Seer", "Wolf", "Troublemaker", "Drunk", "Minion", "Robber"],
            ["Minion", "Wolf", "Troublemaker", "Drunk", "Seer", "Robber"],
            [1],
            "Village",
        )


class TestGetIndividualPreds:
    """ Tests for the get_individual_preds function. """

    @staticmethod
    def test_medium_individual_preds(medium_game_roles, medium_statement_list):
        """ Should get the individual predictions for all players. """
        player_objs = [
            Seer(0, (2, "Drunk")),
            Wolf(1, [1], 5, "Troublemaker"),
            Drunk(2, 5),
            Robber(3, 1, "Wolf"),
            Minion(4, [1]),
        ]

        result = one_night.get_individual_preds(player_objs, medium_statement_list)

        assert result == [
            ("Seer", "Wolf", "Troublemaker", "Drunk", "Minion", "Robber"),
            ("Wolf", "Seer", "Robber", "Minion", "Troublemaker", "Drunk"),
            ("Seer", "Wolf", "Troublemaker", "Drunk", "Minion", "Robber"),
            ("Wolf", "Minion", "Troublemaker", "Drunk", "Seer", "Robber"),
            ("Wolf", "Minion", "Troublemaker", "Drunk", "Seer", "Robber"),
        ]


class TestConfidence:
    """ Tests for the get_confidence function. """

    @staticmethod
    def test_small_confidence(small_game_roles):
        """ Should get voting results from the individual predictions. """
        indiv_preds = [["Villager", "Seer", "Robber"]] * 3

        result = one_night.get_confidence(indiv_preds)

        assert result == [1.0] * 3

    @staticmethod
    def test_medium_confidence(medium_game_roles):
        """ Should get voting results from the individual predictions. """
        indiv_preds = [
            ["Seer", "Wolf", "Troublemaker", "Drunk", "Minion", "Robber"],
            ["Wolf", "Seer", "Robber", "Minion", "Troublemaker", "Drunk"],
            ["Seer", "Wolf", "Troublemaker", "Drunk", "Minion", "Robber"],
            ["Wolf", "Minion", "Troublemaker", "Drunk", "Seer", "Robber"],
            ["Wolf", "Minion", "Troublemaker", "Drunk", "Seer", "Robber"],
        ]

        result = one_night.get_confidence(indiv_preds)

        assert result == [0.6, 0.4, 0.8, 0.8, 0.4, 0.8]

    @staticmethod
    def test_large_confidence(large_game_roles, large_individual_preds):
        """ Should get voting results from the individual predictions. """
        random.shuffle(large_individual_preds)

        result = one_night.get_confidence(large_individual_preds)

        assert result == [
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
        ]


class TestGetVotingResult:
    """ Tests for the get_voting_result function. """

    @staticmethod
    def test_small_voting_result(caplog, small_game_roles):
        """ Should get voting results from the individual predictions. """
        indiv_preds = [("Villager", "Seer", "Robber")] * len(small_game_roles)
        player_list = [Player(i) for i in range(len(small_game_roles))]

        result = one_night.get_voting_result(player_list, indiv_preds)

        assert result == (["Villager", "Seer", "Robber"], [0, 1, 2], [1, 2, 0])
        verify_output_string(caplog, "\nVote Array: [1, 1, 1]\n")

    @staticmethod
    def test_medium_voting_result(caplog, medium_game_roles):
        """ Should get voting results from the individual predictions. """
        indiv_preds = [
            ("Seer", "Wolf", "Troublemaker", "Drunk", "Minion", "Robber"),
            ("Wolf", "Seer", "Robber", "Minion", "Troublemaker", "Drunk"),
            ("Seer", "Wolf", "Troublemaker", "Drunk", "Minion", "Robber"),
            ("Wolf", "Minion", "Troublemaker", "Drunk", "Seer", "Robber"),
            ("Wolf", "Minion", "Troublemaker", "Drunk", "Seer", "Robber"),
        ]
        player_list = [Player(i) for i in range(len(medium_game_roles))]

        result = one_night.get_voting_result(player_list, indiv_preds)

        assert result == (
            ["Seer", "Wolf", "Troublemaker", "Drunk", "Minion", "Robber"],
            [0],
            [1, 0, 1, 0, 0],
        )
        verify_output_string(caplog, "\nVote Array: [3, 2, 0, 0, 0]\n")

    @staticmethod
    def test_large_voting_result(caplog, large_game_roles, large_individual_preds):
        """ Should get voting results from the individual predictions. """
        random.shuffle(large_individual_preds)
        player_list = [Player(i) for i in range(len(large_game_roles))]

        result = one_night.get_voting_result(player_list, large_individual_preds)

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
            [3],
            [8, 10, 1, 9, 5, 7, 5, 3, 3, 10, 8, 3],
        )
        verify_output_string(caplog, "\nVote Array: [0, 1, 0, 3, 0, 2, 0, 1, 2, 1, 2, 0]\n")


class TestEvalWinningTeam:
    """ Tests for the eval_winning_team function. """

    @staticmethod
    def test_werewolf_wins(caplog, medium_game_roles):
        """ Should declare Werewolf victory if no wolves are found, but one exists. """
        guessed_wolf_inds = list(range(const.NUM_PLAYERS))
        vote_inds = [1] * const.NUM_PLAYERS

        result = one_night.eval_winning_team(medium_game_roles, guessed_wolf_inds, vote_inds)

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
        guessed_wolf_inds = list(range(const.NUM_PLAYERS))
        vote_inds = [1] * const.NUM_PLAYERS

        result = one_night.eval_winning_team(small_game_roles, guessed_wolf_inds, vote_inds)

        expected = ("No wolves were found.", "That was correct!\n", "Village Team wins!")
        assert result == "Village"
        verify_output(caplog, expected)

    @staticmethod
    def test_village_wins_found_wolf(caplog, medium_game_roles):
        """ Should declare Villager victory if no wolves are found, and there are none. """
        guessed_wolf_inds = [2]
        vote_inds = [1, 2, 2, 2, 1]

        result = one_night.eval_winning_team(medium_game_roles, guessed_wolf_inds, vote_inds)

        expected = (
            "Player 2 was chosen as a Wolf.",
            "Player 2 was a Wolf!\n",
            "Village Team wins!",
        )
        assert result == "Village"
        verify_output(caplog, expected)

    @staticmethod
    def test_hunter_wins(caplog, large_game_roles):
        """
        Should declare Village victory if no wolves are found,
        Hunter is killed, and Hunter voted for a true Wolf.
        """
        set_roles(*large_game_roles[::-1])
        guessed_wolf_inds = [0, 9]
        vote_inds = [7, 10, 0, 9, 7, 9, 7, 7, 7, 0, 0, 0]
        expected = (
            "Player 0 was chosen as a Wolf.",
            "Player 0 was a Hunter!\n",
            "(Player 0) Hunter died and killed Player 7 too!\n",
            "Player 9 was chosen as a Wolf.",
            "Player 9 was a Tanner!\n",
            "Player 7 was chosen as a Wolf.",
            "Player 7 was a Wolf!\n",
            "Village Team wins!",
        )

        result = one_night.eval_winning_team(const.ROLES, guessed_wolf_inds, vote_inds)

        assert result == "Village"
        verify_output(caplog, expected)

    @staticmethod
    def test_tanner_wins(caplog, large_game_roles):
        """ Should declare Tanner victory if no wolves are found, and Tanner was chosen. """
        guessed_wolf_inds = [2, 5]
        vote_inds = [8, 7, 1, 9, 5, 10, 5, 3, 3, 10, 10, 3]

        result = one_night.eval_winning_team(large_game_roles, guessed_wolf_inds, vote_inds)

        expected = (
            "Player 2 was chosen as a Wolf.",
            "Player 2 was a Robber!\n",
            "Player 5 was chosen as a Wolf.",
            "Player 5 was a Tanner!\n",
            "Tanner wins!",
        )
        assert result == "Tanner"
        verify_output(caplog, expected)
