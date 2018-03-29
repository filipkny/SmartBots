from scipy.optimize import differential_evolution
import numpy as np
from game import Game
from Defaults import PIPEGAPSIZE
# 10k/fit - prob not good
# 10 and 5 def not working
# 348 after 5k iters for 2
# 334 after 2k iters for 1
# 340 after 5k iters for 1


# 1/fit -
# ends after 2179 at 358 avg for bound 3

# 10/fit
# ends after 1639 at 368.6 avg for bound 3

# 100/fit
# ends after 2179 at 364.1 avg for bound 3
# Game number 2904 is over with average fitness now of  313 and maximum score of 6 b0.1
# Game number 3259 is over with average fitness now of  331 and maximum score of 8 b2
# Game number 2179 is over with average fitness now of  350 and maximum score of 8 b1

#-fit
# ends after 3.5k with 333 avg with max 14 for bound 3

#-1/fit
# Game number 2478 is over with average fitness now of  335 and maximum score of 10 b3

# fit
# Game number 2483 is over with average fitness now of  307 and maximum score of 7 - b3
# Game number 1471 is over with average fitness now of  300 and maximum score of 5 -b1




# good_start = [ 0.42808821, -2.20599695, -1.36463635, -2.64356078, -0.3414663 ,
#         1.54710738, -2.42923382,  0.69040533, -1.59005237,  2.78380053,
#        -2.25658969,  0.99114311, -2.482751  , -1.89836315,  0.51885838,
#         0.7911339 ,  0.79377306, -1.64218754]
#
# weights = [-1.66564265904, -0.00244411156234, 0.5859536557, -1.26551042752, -1.71955897353, -0.213616066075,
#            1.05844665273, -1.94223671616, -1.0371670467, -0.563423663427, 2.42988683925, 1.0056792515, -2.78343858473,
#            0.195530535462, -0.183752541701, -2.26010914343, 1.40986998411, 2.01867854855]
#
# weightsBetter = [-1.71834055626,-0.0744778494839,0.589837506551,-1.27884310128,-1.65631958389,-0.312334262196,0.989548618519,-2.01429096266,-1.06583105164,-0.612841182912,2.3709671524,0.950296356776,-2.72503359616,0.190704156724,-0.23177529325,-2.28961793758,1.37718581756,2.02822885328]

def simulate(recomb = 0.3, pop_size = 10, mut = 0.7, bound_rad = 3, plotDataFile ="PlotData.txt" , FlappyDataFile = 'FlappyData.txt'):
    genetic_params = {
        "recombination": recomb,#0.3,
        "pop_size": pop_size,#23,
        "mutation": mut,#0.7,  # try 0.2
        "bound_rad": bound_rad#3
    }

    bounds = np.array([(-genetic_params["bound_rad"], genetic_params["bound_rad"])] * 18)

    game = Game(MANUAL_PLAY=False, AI_PLAY=True, plotDataFile = plotDataFile, flappyDataFile=FlappyDataFile)


    with open(FlappyDataFile, 'a') as file:
        output = "---------- Simulation number " + str(1) + \
                 " with bound radius: " + str(genetic_params["bound_rad"]) + \
                 " recombination: " + str(genetic_params["recombination"]) + \
                 " pop size: " + str(genetic_params["pop_size"]) + \
                 " mutation: " + str(genetic_params["mutation"]) + \
                 " gap size: " + str(PIPEGAPSIZE) + \
                 " ----------\n"
        file.write(output)

    result = differential_evolution(
        game.main,
        bounds,
        maxiter=20000,
        disp=True,
        recombination=genetic_params["recombination"],
        popsize=genetic_params["pop_size"],
        mutation=genetic_params["mutation"])

