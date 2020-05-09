""" main.py """
import logging

from src import const, logger, one_night, replay_game


def main(num_games: int = const.NUM_GAMES) -> None:
    """ Simulate play_one_night_werewolf and create a Statistics instance for the runs. """
    if num_games > const.MAX_LOG_GAMES:
        logger.setLevel(logging.WARNING)
    one_night.simulate_game(
        num_games, disable_tqdm=num_games <= const.MAX_LOG_GAMES, save_replay=const.SAVE_REPLAY
    )


if __name__ == "__main__":
    if const.REPLAY:
        replay_game()
    else:
        main()
