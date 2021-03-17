import MyGenetic
import pickle

with open('GaData.pkl', 'rb') as f:
    pop, f_iter = pickle.load(f)

(bestFit, idx) = MyGenetic.minFit(pop)

wx = pop[idx].Genes[0]
width = pop[idx].Genes[1]
depth = pop[idx].Genes[2]
length = pop[idx].Genes[3]
f = round(pop[idx].Genes[4])
print("best value obtained with wx = {0:3.2f}, width = {1:3.2f}, depth = {2:3.2f}, length = {3:3.2f} and Frequency = {4}.".format(
    wx, width, depth, length, f
))
print("best fittness value is: {0:12.9f} .".format(bestFit))
