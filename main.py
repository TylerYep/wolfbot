""" main.py """
from src import const, one_night, replay_game_from_state


def main() -> None:
    """ Simulate play_one_night_werewolf. """
    if const.REPLAY:
        replay_game_from_state()
    else:
        disable_logging = const.NUM_GAMES > const.MAX_LOG_GAMES
        one_night.simulate_game(
            num_games=const.NUM_GAMES,
            save_replay=const.SAVE_REPLAY,
            disable_tqdm=not disable_logging,
            disable_logging=disable_logging,
        )


if __name__ == "__main__":
    main()
