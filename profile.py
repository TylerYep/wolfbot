''' profile.py '''
import pstats

# python -m cProfile -o ./text.txt main.py -n 100
stats = pstats.Stats('./text.txt')
stats.sort_stats('cumulative').print_stats(20)
