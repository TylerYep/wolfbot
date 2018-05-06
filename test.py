from roles import *
import pickle
from algorithms import *
with open('test.pkl', 'rb') as f:
    roles, all_statments = pickle.load(f)

print('SOLUTION: ', roles)
print('STATEMENTS: ')
for i, s in enumerate(all_statments):
    print(i,': ' ,s)

a = switching_solver(all_statments)
c, d = baseline_solver(all_statments)

print(a.path, c)
