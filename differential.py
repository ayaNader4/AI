import random
import evolution


class DE01Knapsack:
    capacity = 50
    max_pop = 100
    items_count = 20  # number of items in a collection
    CR = 0.7  # crossover rate
    weights = []
    values = []
    definiteCrossovers = 0;
    best_solutions = []

    def __init__(self, weights, values, n, capacity):
        self.weights = weights
        self.values = values
        self.items_count = n
        self.capacity = capacity

    def execute(self):
        next_pop = evolution.initial_pop_01(self)
        next_pop = evolution.grade_and_sort(self, next_pop, "")
        print(next_pop)
        for j in range(30):
            temp = next_pop[:]
            next_pop = []
            for p in temp:
                next_pop.append(p[2])

            children = evolution.de_crossover(self, next_pop, "binary")
            next_pop = evolution.grade_and_sort(self, children, "")

            # print("gen", j, next_pop)
            self.best_solutions.append(next_pop[0][0])
        return next_pop[0], self.best_solutions


class DEUnboundedKnapsack:
    capacity = 50
    max_pop = 100
    items_count = 20  # number of items in a collection
    CR = 0.7  # crossover rate
    weights = []
    values = []
    best_solutions = []

    def __init__(self, weights, values, n, capacity):
        self.weights = weights
        self.values = values
        self.items_count = n
        self.capacity = capacity

    def execute(self):
        next_pop = evolution.initial_pop_ub(self)
        next_pop = evolution.grade_and_sort(self, next_pop, "")

        for j in range(170):
            temp = next_pop[:]
            next_pop = []
            for p in temp:
                next_pop.append(p[2])

            children = evolution.de_crossover(self, next_pop, "ub")
            next_pop = evolution.grade_and_sort(self, children, "")
            # print("gen", j, next_pop)

            self.best_solutions.append(next_pop[0][0])
        return next_pop[0], self.best_solutions
