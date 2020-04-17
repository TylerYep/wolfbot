""" tanner_test.py """
# from src.roles import Tanner
#
#
# class TestTanner:
#     ''' Tests for the Tanner player class. '''
#
#     @staticmethod
#     def test_awake_init(large_game_roles):
#         '''
#         Should initialize a Tanner. Note that the player_index of the Tanner is
#         not necessarily the index where the true Tanner is located.
#         '''
#         player_index = 3
#         expected = None
#
#         tanner = Tanner.awake_init(player_index, [], [])
#
#         assert tanner.statements == expected
