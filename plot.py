import pickle
import statistics
#import matplotlib.pyplot as plt
#import numpy as np
#with open('train_stats.pkl', 'rb') as f:
#    stats = pickle.load(f)
#
#correct = [sim.correct[2]/10 for sim in stats]
#x = [10*i for i in range(len(correct))]
#i = len(correct)//1
#correct, x = correct[:i], x[:i]
#
#fig, ax = plt.subplots()
#ax.set_title('Training the Wolf')
#ax.scatter(x[:i], correct[:i])
#ax.set_xlabel('Number of simulations')
#ax.set_ylabel('Probability that the wolf was found (%)')
#ax.spines['right'].set_visible(False)
#ax.spines['top'].set_visible(False)
#plt.show()

# Credit: Josh Hemann

#random_solver
#
#Accuracy for all predictions: 0.14739166666666667
#Accuracy with lenient center scores: 0.18905833333333333
#S1: Found at least 1 Wolf player: 0.316
#S2: Found all Wolf players: 0.1051
#Percentage of correct Wolf guesses (including Wolves in the center): 0.1699
#
#baseline_solver
#
#Accuracy for all predictions: 0.5577416666666667
#Accuracy with lenient center scores: 0.6273
#S1: Found at least 1 Wolf player: 0.731
#S2: Found all Wolf players: 0.4469
#Percentage of correct Wolf guesses (including Wolves in the center): 0.58105
#
#switching_solver
#
#Accuracy for all predictions: 0.807975
#Accuracy with lenient center scores: 0.8550416666666667
#S1: Found at least 1 Wolf player: 0.8401
#S2: Found all Wolf players: 0.629
#Percentage of correct Wolf guesses (including Wolves in the center): 0.7069
#Time taken: 1193.2269577980042
#
#EXPECTIMAX
#Accuracy for all predictions: 0.7185
#Accuracy with lenient center scores: 0.7605
#S1: Found at least 1 Wolf player: 0.479
#S2: Found all Wolf players: 0.186
#Percentage of correct Wolf guesses (including Wolves in the center): 0.3925
#Time taken: 1072.169737815857
#
#RANDOM
#Accuracy for all predictions: 0.815
#Accuracy with lenient center scores: 0.8616666666666667
#S1: Found at least 1 Wolf player: 0.847
#S2: Found all Wolf players: 0.656
#Percentage of correct Wolf guesses (including Wolves in the center): 0.712
#Time taken: 57.86407232284546

#### SECOND PLOT ############



#import numpy as np
#import matplotlib.pyplot as plt
#from matplotlib.ticker import MaxNLocator
#from collections import namedtuple
#
#
#n_groups = 3
#
#m1 = (0.147, 0.627, 0.855)
#
#m2 = (0.316, 0.731, 0.840)
#
#m3 = (0.105, 0.447, 0.629)
#
#fig, ax = plt.subplots()
#
#index = np.arange(n_groups)
#bar_width = 0.3
#
#opacity = 1
#
#rects3 = ax.bar(index, m3, bar_width,
#                alpha=opacity, 
#                label='Guessed all wolves')
#
#rects2 = ax.bar(index + 2*bar_width, m2, bar_width,
#                alpha=opacity, color='r',
#                label='Guessed more than 1 wolf')
#
#rects1 = ax.bar(index+bar_width, m1, bar_width,
#                alpha=opacity,
#                label='All role guesses')
#
#ax.set_ylabel('Percentages')
#ax.set_title('Comparing Solver Algorithms')
#ax.set_xticks(index + bar_width*1.12)
#ax.set_xticklabels(('Random Solver', 'Baseline Solver', 'Switching Solver'))
#ax.legend()
#ax.spines['right'].set_visible(False)
#ax.spines['top'].set_visible(False)
#
#fig.tight_layout()
#plt.show()

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from collections import namedtuple


n_groups = 2

m1 = (0.147, 0.627, 0.855)

m2 = (0.847, 0.479)

m3 = (0.656, 0.186)

fig, ax = plt.subplots()

index = np.arange(n_groups)
bar_width = 0.3

opacity = 1

rects3 = ax.bar(index, m3, bar_width,
                alpha=opacity, 
                label='Guessed all wolves')

rects2 = ax.bar(index + bar_width, m2, bar_width,
                alpha=opacity, color='r',
                label='Guessed more than 1 wolf')


ax.set_ylabel('Percentages')
ax.set_title('Comparing Wolf Players')
ax.set_xticks(index + bar_width/2)
ax.set_xticklabels(('Random Wolf', 'Expecimax Wolf'))
ax.legend()
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

fig.tight_layout()
plt.show()
