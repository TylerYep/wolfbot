''' profile.py '''
import pstats
import cProfile

from main import main  # pylint: disable=unused-import


def profile():
    '''
    Prints top N methods, sorted by time.
    Equivalent to:
    python -m cProfile -o data/profile.txt main.py -n 100
    Options:
    time, cumulative, line, name, nfl, calls
    '''
    command = 'main(100)'
    profile_file = 'data/profile.txt'
    sort = 'time'

    cProfile.run(command, filename=profile_file, sort=sort)
    stats = pstats.Stats(profile_file)
    stats.sort_stats(sort).print_stats(50)


if __name__ == '__main__':
    profile()
