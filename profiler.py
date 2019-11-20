''' profile.py '''
import pstats
# from pstats import SortKey

# python -m cProfile -o data/profile.txt main.py -n 100
# TIME, CUMULATIVE, LINE, NAME, NFL
def main():
    ''' Prints top N methods. '''
    stats = pstats.Stats('data/profile.txt')
    stats.sort_stats('cumulative').print_stats(30)

if __name__ == '__main__':
    main()
