''' profile.py '''
import pstats

# python -m cProfile -o ./text.txt main.py -n 100
def main():
    ''' Prints top N methods. '''
    stats = pstats.Stats('./text.txt')
    stats.sort_stats('cumulative').print_stats(20)

if __name__ == '__main__':
    main()
