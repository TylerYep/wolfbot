""" main.py """
import logging
import time

from tqdm import tqdm

from src import Statistics, const, logger, play_one_night_werewolf, replay_game


def main(num_games: int = const.NUM_GAMES) -> None:
    """ Simulate play_one_night_werewolf and create a Statistics instance for the runs. """
    start_time = time.time()
    if num_games > const.MAX_LOG_GAMES:
        logger.setLevel(logging.WARNING)

    stat_tracker = Statistics()
    for _ in tqdm(range(num_games), disable=num_games <= const.MAX_LOG_GAMES):
        game_result = play_one_night_werewolf(const.SAVE_REPLAY)
        stat_tracker.add_result(game_result)
    stat_tracker.print_statistics()
    logger.warning(f"\nTime taken: {time.time() - start_time}")


if __name__ == "__main__":
    if const.REPLAY:
        replay_game()
    else:
        main()
