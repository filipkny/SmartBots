from scipy.optimize import differential_evolution
from Game import Game
from Defaults import PIPEGAPSIZE

def simulate(strat = None, recomb = 0.3, pop_size = 10, mut = 0.7, bound_rad = 3,num_weights = 6, iters=200, plotDataFile ="PlotData.txt" , FlappyDataFile = 'FlappyData.txt', dataFolder='../data/'):

    plotDataFile =  dataFolder + plotDataFile + \
                   "rec" + str(recomb) + \
                   "pop" + str(pop_size) + \
                   "mut" + str(mut) + \
                   "brad" + str(bound_rad) + \
                   "wnum" + str(num_weights) + \
                   "strat" + str(strat)

    FlappyDataFile = dataFolder + FlappyDataFile

    genetic_params = {
        "recombination": recomb,#0.3,
        "pop_size": pop_size,#23,
        "mutation": mut,#0.7,  # try 0.2
        "bound_rad": bound_rad#3
    }

    bounds = [(-genetic_params["bound_rad"], genetic_params["bound_rad"])] * num_weights

    game = Game(MANUAL_PLAY=False, AI_PLAY=True, plotDataFile = plotDataFile, flappyDataFile=FlappyDataFile)

    with open(FlappyDataFile, 'a') as file:
        output = "---------- Simulation number " + str(1) + \
                 " with bound radius: " + str(genetic_params["bound_rad"]) + \
                 " recombination: " + str(genetic_params["recombination"]) + \
                 " pop size: " + str(genetic_params["pop_size"]) + \
                 " mutation: " + str(genetic_params["mutation"]) + \
                 " gap size: " + str(PIPEGAPSIZE) + \
                 " num weights: " + str(num_weights) + \
                 " strat: " + str(strat) + \
                 " ----------\n"
        file.write(output)

    result = differential_evolution(
        game.main,
        bounds,
        maxiter=iters,
        disp=True,
        recombination=genetic_params["recombination"],
        popsize=genetic_params["pop_size"],
        mutation=genetic_params["mutation"],
        strategy=strat)

    print(result)
    print("Done with de")
    return result,plotDataFile