""" main.py """
from src import const, one_night, replay


def main() -> None:
    """Simulate play_one_night_werewolf."""
    if const.REPLAY:
        replay.replay_game_from_state()
    else:
        enable_logging = const.NUM_GAMES < const.MAX_LOG_GAMES
        one_night.simulate_game(
            num_games=const.NUM_GAMES,
            save_replay=const.SAVE_REPLAY,
            enable_tqdm=not enable_logging,
            enable_logging=enable_logging,
        )


if __name__ == "__main__":
    main()
