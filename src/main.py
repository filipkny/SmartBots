from Simulation import simulate
from matplotlib import pyplot as plt
import os
import numpy as np


def generateAndSaveGraph(filename):
    lines = [line.rstrip('\n') for line in open(filename)]

    runs = [x.split(",")[0] for x in lines]
    scores = [x.split(",")[1] for x in lines]

    avg = []
    avgs = []
    for i in range(len(scores)):
        score = float(scores[i])
        if len(avg) < 2000:
            avg.append(score)
        else:
            avg.pop(0)
            avg.append(score)
        avgs.append(sum(avg) / len(avg))

    plt.plot(range(len(avgs)), avgs)

    variance = np.var(avgs)
    gradient = np.gradient(avgs)
    print(filename + "-->  " +
          "Max: " + str(max(avgs)) +
          " | Variance: "  + str(variance) +
          " | Average gradient: " + str(sum(gradient)/len(gradient)))
    plt.title(filename)
    plt.grid(True)
    plt.savefig(filename + ".png")
    plt.show()

def fullSimulate():
    strats = ['best1bin',
              'best1exp',
              'rand1exp',
              'randtobest1exp',
              'best2exp',
              'rand2exp',
              'randtobest1bin',
              'best2bin',
              'rand2bin',
              'rand1bin']

    muts = [0.25,0.45,0.65] #0.45
    bound_rads = [0.1, 1] #0.1
    pops = [3, 10, 15] #3
    recombs = [0.2, 0.4, 0.6, 0.8] #1
    big_recombs = [1, 1.25, 1.5, 1.75]

    result, filename = simulate(strat='best1bin', pop_size=5, mut=0.45, bound_rad=0.1,iters=1000, recomb=0.6,FlappyDataFile="flappyRunData",plotDataFile="flappyPlotData")
    print("done")
    generateAndSaveGraph(filename)




if __name__ == '__main__':
    fullSimulate()
