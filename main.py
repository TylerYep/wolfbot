''' main.py '''
import time
from tqdm import tqdm

from src import Statistics, play_one_night_werewolf, logger, const, replay_game

def main(save_replay: bool) -> None:
    ''' Simulate play_one_night_werewolf and create a Statistics instance for the runs. '''
    start_time = time.time()
    stat_tracker = Statistics()
    for _ in tqdm(range(const.NUM_GAMES), disable=const.NUM_GAMES <= 10):
        game_result = play_one_night_werewolf(save_replay)
        stat_tracker.add_result(game_result)
    stat_tracker.print_statistics()
    logger.warning(f'\nTime taken: {time.time() - start_time}')


if __name__ == '__main__':
    if const.REPLAY:
        replay_game()
    else:
        main(const.SAVE_REPLAY)
