from scipy.optimize import differential_evolution
import numpy as np
from game import Game

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


bound = 3

good_start = [ 0.42808821, -2.20599695, -1.36463635, -2.64356078, -0.3414663 ,
        1.54710738, -2.42923382,  0.69040533, -1.59005237,  2.78380053,
       -2.25658969,  0.99114311, -2.482751  , -1.89836315,  0.51885838,
        0.7911339 ,  0.79377306, -1.64218754]

bounds = np.array([(-bound,bound)] * 18)
game = Game(MANUAL_PLAY = False, AI_PLAY=True)
result = differential_evolution(game.main ,bounds,maxiter=2000, disp=True)
print("For bound number " + str(bound))
print(result)

# TODO make nicer prints, add options
# TODO save weights and load them
