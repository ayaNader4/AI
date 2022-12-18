import random

import evolution


class GA01Knapsack:
    capacity = 50  # capacity of knapsack
    max_pop = 100 # number of individuals in a generation
    items_count = 20  # number of items in the knapsack
    mutation_rate = 0.01
    weights = []
    values = []
    avg_fitness = []
    best_solutions = []

    def __init__(self, weights, values, n, capacity):
        self.weights = weights
        self.values = values
        self.items_count = n
        self.capacity = capacity

    def execute(self):
        # initializing current generation
        # print(self.items_count)
        next_pop = evolution.initial_pop_01(self)
        # print(next_pop)
        next_pop = evolution.grade_and_sort(self, next_pop, "bit_flip")
        print(next_pop)

        # the evolution loop
        for j in range(200):  # 800 is number of generations
            temp = next_pop[:]
            next_pop = []
            for p in temp:
                # extracts
                next_pop.append(p[2])

            # choose best 2 individuals + a random selection of individuals
            # can change the random select function to exclude the best 2 solutions
            # parents = next_pop[:2] + evolution.random_selection(self, next_pop)
            # the length keeps fluctuating, idk why..
            # print(len(parents))

            # # ROULETTE SELECTION
            parents_indices = evolution.select_parents(self, next_pop)
            print(parents_indices)

            parents = next_pop[:2] + [next_pop[i] for i in parents_indices]
            print(parents)
            # the difference maker is the 2 best individuals being a part of the parents
            # temp2 = [evolution.fitness(self, next_pop[i], "") for i in parents_indices]

            children = evolution.ga_crossover(self, parents)

            # random selects twice?
            # selected = evolution.random_selection(self, next_pop)
            temp = children + parents
            # 45

            # filling out the rest of the population with the best parents
            # 100 - length(children + selected)
            # for i in range(self.max_pop - (len(children) + len(parents))):
            #     temp.append(next_pop[i])

            next_pop = temp[:]

            # mutate by bit flipping
            next_pop = evolution.mutation(self, next_pop, "bit_flip")

            # order once more
            next_pop = evolution.grade_and_sort(self, next_pop, "bit_flip")
            # print("gen", j, next_pop)

            # slowly increases mutation rate, I guess we'll slowly start converging at 100 generations
            if j >= 100 and self.mutation_rate < 0.1:
                self.mutation_rate += 0.01

            pop_fitness = sum([individual[0] for individual in next_pop])
            avg = pop_fitness / self.max_pop
            self.avg_fitness.append(avg)

            self.best_solutions.append(next_pop[0][0])
        return next_pop[0], self.best_solutions


class GAUnboundedKnapsack:
    capacity = 50
    max_pop = 100
    items_count = 20
    mutation_rate = 0.01
    weights = []
    values = []
    best_solutions = []

    def __init__(self, weights, values, n, capacity):
        self.weights = weights
        self.values = values
        self.items_count = n
        self.capacity = capacity

    def random_selection(self, population):
        rs_rate = 0.2
        selected = []
        for indiv in population:
            if random.random() < rs_rate:
                selected.append(population[random.randint(self.max_pop // 3, self.max_pop - 1)])
        return selected

    def crossover(self, parents_list, n):
        crossover_point = random.randint(0, n - 1)
        children = []
        for i in range(len(parents_list) - 1):
            children.append(parents_list[i][:crossover_point] + parents_list[i + 1][crossover_point:])
        return children

    def execute(self):
        next_pop = evolution.initial_pop_ub(self)
        next_pop = evolution.grade_and_sort(self, next_pop, "")
        print(next_pop)

        for j in range(1000):

            temp = next_pop[:]
            next_pop = []
            for p in temp:
                next_pop.append(p[2])

            # parents = next_pop[:2] + self.random_selection(next_pop)
            parents_indices = evolution.select_parents(self, next_pop)
            parents = next_pop[:2] + [next_pop[i] for i in parents_indices]

            children = evolution.ga_crossover(self, parents)

            temp = children + parents
            for i in range(self.max_pop - (len(children) + len(parents))):
                temp.append(next_pop[i])


            next_pop = temp[:]

            # mutation done by bit swapping
            next_pop = evolution.mutation(self, next_pop, "bit_swapping")
            next_pop = evolution.grade_and_sort(self, next_pop, "")
            # print("gen", j, next_pop)
            if j >= 100 and self.mutation_rate < 0.1:
                self.mutation_rate += 0.01

            self.best_solutions.append(next_pop[0][0])
        return next_pop[0], self.best_solutions
