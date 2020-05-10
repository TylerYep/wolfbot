""" profile.py """
import cProfile
import pstats

from src import one_night  # pylint: disable=unused-import


def profile() -> None:
    """
    Prints top N methods, sorted by time.
    Equivalent to:
        python -m cProfile -o data/profile.txt main.py -n 100
    Options:
        time, cumulative, line, name, nfl, calls
    -----------
    ncalls - for the number of calls.

    time/tottime - for the total time spent in the given function
    (and excluding time made in calls to sub-functions)

    percall - is the quotient of tottime divided by ncalls

    cumulative/cumtime - is the cumulative time spent in this and all subfunctions
    (from invocation till exit). This figure is accurate even for recursive functions.

    percall - is the quotient of cumtime divided by primitive calls
    """
    command = "one_night.simulate_game(200, disable_tqdm=False)"
    profile_file = "data/profile.txt"
    sort = "time"

    cProfile.run(command, filename=profile_file, sort=sort)
    stats = pstats.Stats(profile_file)
    stats.sort_stats(sort).print_stats(50)


if __name__ == "__main__":
    profile()
