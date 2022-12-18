import random

import numpy as np

capacity = 50  # capacity of knapsack
max_pop = 100  # number of individuals in a generation
items_count = 20  # number of items in the knapsack
mutation_rate = 0.01
weights = []
values = []


def initial_pop_01(self):
    pop = [[random.randint(0, 1) for i in range(self.items_count)] for i in range(self.max_pop)]
    return pop


def initial_pop_ub(self):
    # creating the solutions
    # capacity // minimum weight guarantees that an individual gene can't be infeasible, but the solution overall might
    # 50 // 10 = 0 - 5
    # [3, 2, 0, 1, 2, 0]
    pop = [[random.randint(0, self.capacity // min(self.weights)) for i in range(self.items_count)] for i in
           range(self.max_pop)]
    return pop


def fitness(self, individual, mode):
    indiv_value, indiv_weight, individual = summation(self, individual)

    # fixes the infeasible solutions for genetic only, should make this a separate function
    # mode will be "" if differential, and will be either "bit_flip" or "bit_swapping" for genetic
    if mode == "bit_flip":
        while indiv_weight > self.capacity:
            # performs mutation, depending on the mode sent
            individual = mutation_helpers(self, individual, mode)
            indiv_value, indiv_weight, individual = summation(self, individual)
    else:
        if indiv_weight > self.capacity:
            # the value becomes negative if the weight exceeds capacity
            return tuple([self.capacity - indiv_weight, indiv_weight, individual])

    return tuple([indiv_value, indiv_weight, individual])


def summation(self, individual):
    indiv_weight = 0
    indiv_value = 0
    for i in range(len(individual)):
        indiv_weight += individual[i] * self.weights[i]
        indiv_value += individual[i] * self.values[i]
    return tuple([indiv_value, indiv_weight, individual])


def grade_and_sort(self, population, mode):
    graded = []
    for individual in population:
        graded.append(fitness(self, individual, mode))
    # gets sorted in descending order, so best individuals are first and worst/invalid individuals are last
    graded.sort(reverse=True)
    return graded


def tournament_selection(self, parent_population, tournament_size):
    """ Use deterministic tournament selection to select parents.
    Let the Hunger Games commence!
    Args:
        parent_population(np.array): Parent population matrix.
        population_size(int): Size of population.
        tournament_size(int): Number of competitor individuals per tournament.
    Returns:
        np.array: Winning individual parent chromosome.
    """
    selected_parent = parent_population[random.randint(0, self.items_count - 1)]
    highest_fitness_score = fitness(self, selected_parent, "")[0]

    for n in range(tournament_size):
        i = random.randint(0, self.items_count - 1)
        parent = parent_population[i]

        temp = fitness(self, parent, "")
        fitness_score = temp[0]

        if fitness_score >= highest_fitness_score:
            selected_parent = parent
            highest_fitness_score = fitness_score

    return selected_parent


def select_parents(self, next_pop):
    # selected_parents = []
    # for n in range(self.max_pop):
    #     selected_parent = tournament_selection(self, next_pop, tournament_size)
    #     selected_parents.append(selected_parent)

    # Computes the totality of the population fitness
    population_fitness = sum([abs(fitness(self, individual, "")[0]) for individual in next_pop])

    # Computes for each chromosome the probability
    individual_probabilities = [abs((fitness(self, individual, "")[0] / population_fitness)) for individual in next_pop]

    indices = list(range(0, len(next_pop)))

    # Selects one chromosome based on the computed probabilities
    return np.random.choice(indices, size=self.max_pop // 6, p=individual_probabilities)


def random_selection(self, population):
    rs_rate = 0.2
    selected = []
    for _ in population:
        # chooses 20% of people
        if random.random() < rs_rate:
            # selects a random person between 33 - 99, effectively removing the best 33% of the population from being
            # selected
            selected.append(population[random.randint(self.max_pop // 3, self.max_pop - 1)])
    # print(len(selected))
    return selected


def ga_crossover(self, parents_list):
    crossover_point = random.randint(0, self.items_count - 1)
    children = []
    for i in range(self.max_pop - len(parents_list)):
        random_index1 = 0
        random_index2 = 0
        while random_index1 == random_index2:
            random_index1 = random.randint(0, len(parents_list) - 1)
            random_index2 = random.randint(0, len(parents_list) - 1)
        # nth child is a cross-over between nth parent + n+1th parent
        children.append(parents_list[random_index1][:crossover_point] + parents_list[random_index2][crossover_point:])
    # not guaranteed that all of them are feasible
    return children


def mutation_helpers(self, individual, mode):
    if mode == "bit_flip":
        # pick a random gene
        rand_index = random.randint(0, self.items_count - 1)

        # flip the gene
        individual[rand_index] = int(not individual[rand_index])

    elif mode == "bit_swapping":
        # picks 2 random genes
        rand_index1 = random.randint(0, self.items_count - 1)
        rand_index2 = random.randint(0, self.items_count - 1)

        # swap
        temp = individual[rand_index1]
        individual[rand_index1] = individual[rand_index2]
        individual[rand_index2] = temp

    elif mode == "bit_resetting":
        random_index = random.randint(0, self.items_count - 1)
        if individual[random_index] > self.capacity // min(self.weights):
            individual[random_index] -= self.capacity // min(self.weights)
        else:
            individual[random_index] += self.capacity // min(self.weights)

    return individual


def mutation(self, population, mode):
    if mode == "bit_flip":
        for i in range(len(population)):
            if random.random() < self.mutation_rate:
                population[i] = mutation_helpers(self, population[i], "bit_flip")
    if mode == "bit_swapping":
        for i in range(len(population)):
            if random.random() < self.mutation_rate:
                population[i] = mutation_helpers(self, population[i], "bit_swapping")
    return population


# def mutation_bit_flip(self, population):
#     for i in range(len(population)):
#         if random.random() < self.mutation_rate:
#             population[i] = mutation_helpers(self, population[i], "bit_flip")
#     return population
#
#
# def mutation_bit_swapping(self, population):
#     for i in range(len(population)):
#         if random.random() < self.mutation_rate:
#             population[i] = mutation_helpers(self, population[i], "bit_swapping")
#     return population


def de_crossover(self, parents_list, mode):
    new_parents = []
    for i in range(len(parents_list)):
        # mutate (do the equation and create trial vector)
        if mode == "ub":
            v = de_ub_mutation(self, parents_list, parents_list[i], i)
        else:
            v = de_binary_mutation(self, parents_list, parents_list[i], i)
        # calculate fitness of parents
        ind_fit = fitness(self, parents_list[i], "")

        # calculate fitness of trial vectors
        v_fit = fitness(self, v, "")

        if v_fit[0] > ind_fit[0]:
            # select trial
            new_parents.append(v_fit[2])
        else:
            # select target
            new_parents.append(ind_fit[2])
    return new_parents


def de_binary_mutation(self, population, ind, index):
    # not sure why only between 0 and 1
    F = random.randint(0, 1)
    selected = [ind]

    # pick 3 other random individuals
    candidates = list(range(0, len(population)))
    candidates.remove(index)  # [5]
    random_index = random.sample(candidates, 3)
    # [20, 84, 54]
    #  r1, r2, r3

    # add them along with the target
    selected.append(population[random_index[0]])
    selected.append(population[random_index[1]])
    selected.append(population[random_index[2]])

    # mutant
    vector = []
    for i in range(self.items_count):
        # the equation is v = x1 + F(x2 - x3)
        # [r4, r1, r2, r3]
        # r2 = [1, 0, 1, 1, 1]
        # r3 = [0, 1, 1, 1, 0]
        # xo = [1, 1, 0, 0, 1]
        # mi = [1, 1, 0, 0, 1]
        xor = selected[2][i] ^ selected[3][i]  # x2 xoring x3
        aand = F & xor  # F anding xor

        # xo = [1, 1, 0, 0, 1]
        # F = 0.9
        # aa = [1, 1, 0, 0, 1]
        oor = selected[1][i] | aand  # x1 oring aand

        # r1 = [0, 1, 1, 0, 0]
        # aa = [1, 1, 0, 0, 1]
        # v  = [1, 1, 1, 0, 1]
        vector.append(oor)

    v_trial = []

    flag = 0
    for i in range(self.items_count):
        # crossing over, doesn't have a definite crossover
        if random.random() <= self.CR:
            # choose mutant vector
            v_trial.append(vector[i])
            flag = 1
        else:
            # choose target vector
            v_trial.append(ind[i])
    if flag == 0:
        rand_index = random.randint(0, self.items_count - 1)
        v_trial[rand_index] = vector[rand_index]
    return v_trial


def de_ub_mutation(self, population, ind, index):
    F = 0.5  # mutation factor
    selected = [ind]  # x4

    candidates = list(range(0, len(population)))
    candidates.remove(index)
    random_index = random.sample(candidates, 3)

    selected.append(population[random_index[0]])  # x1
    selected.append(population[random_index[1]])  # x2
    selected.append(population[random_index[2]])  # x3

    vector = []
    for i in range(self.items_count):
        res = round(selected[1][i] + F * (selected[2][i] - selected[3][i]))  # x1 + F*(x2-x3)
        vector.append(abs(res))

    v_trial = []
    flag = 0
    for i in range(self.items_count):
        if random.random() <= self.CR:
            v_trial.append(vector[i])
            flag = 1
        else:
            v_trial.append(ind[i])
    if flag == 0:
        rand_index = random.randint(0, self.items_count - 1)
        v_trial[rand_index] = vector[rand_index]
    return v_trial
