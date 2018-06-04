import pickle
import statistics
import matplotlib.pyplot as plt
import numpy as np
with open('train_stats.pkl', 'rb') as f:
    stats = pickle.load(f)

correct = [sim.correct[2]/10 for sim in stats]
x = [10*i for i in range(len(correct))]
i = len(correct)//1
correct, x = correct[:i], x[:i]

fig, ax = plt.subplots()
ax.set_title('Training the Wolf')
ax.scatter(x[:i], correct[:i])
ax.set_xlabel('Number of simulations')
ax.set_ylabel('Probability that the wolf was found (%)')
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
plt.show()

print(correct)
