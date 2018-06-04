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

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from collections import namedtuple


n_groups = 5

m1 = (20, 35, 30, 35, 27)

m2 = (25, 32, 34, 20, 25)

m3 = ()

fig, ax = plt.subplots()

index = np.arange(n_groups)
bar_width = 0.35

opacity = 0.4


rects1 = ax.bar(index, means_men, bar_width,
                alpha=opacity, color='b',
                error_kw=error_config,
                label='Men')

rects2 = ax.bar(index + bar_width, means_women, bar_width,
                alpha=opacity, color='r',
                error_kw=error_config,
                label='Women')

ax.set_xlabel('Group')
ax.set_ylabel('Scores')
ax.set_title('Scores by group and gender')
ax.set_xticks(index + bar_width / 2)
ax.set_xticklabels(('A', 'B', 'C', 'D', 'E'))
ax.legend()

fig.tight_layout()
plt.show()
