import pylearn2

class GeneticAlgorithm(object):
    def __init__(self, max_units, top_units):
        self.max_units = max_units # max number of units in population
        self.top_units = top_units # number of top units (winners) used for evolving populatio
        self.population = []
        self.scale_factor = 200
        self.iteration = 1
        self.mutationRate = 1
        self.best_population = 1
        self.best_fitness = 1
        self.best_score = 0

    def reset(self):
        self.iteration = 1
        self.mutationRate = 1
        self.best_population = 1
        self.best_fitness = 1
        self.best_score = 0

    def createNewPopulation(self):
        for i in range(self.max_units):
            pass
