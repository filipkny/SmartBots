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
    plt.show()
    #plt.savefig(filename + ".png")


def fullSimulate():
    muts = [0.2, 0.7, 1.2, 1.7] #0.2
    bound_rads = [0.1, 1] #0.1
    pops = [3, 10, 15] #3
    recombs = [0.2, 0.5, 0.8] #0.5

    # for recomb in recombs:
    #     for mut in muts:
    #         for bound_rad in bound_rads:
    #             for pop in pops:

    result, filename = simulate(pop_size=3, mut=0.2, bound_rad=0.1,iters=1000, recomb=0.5,FlappyDataFile="SingleSequenceRunData1",plotDataFile="SinglePlotData")
    generateAndSaveGraph(filename)


   


fullSimulate()

#  filename = 'data/' + \
   # "rec" + str(recomb) + \
   # "pop" + str(pop) + \
   # "mut" + str(mut) + \
   # "brad" + str(bound_rad) + \
   # "wnum" + str(6)