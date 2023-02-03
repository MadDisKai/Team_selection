import numpy as np
import random
import math

class DNA:
    def __init__(self, count_of_genes=10, probability_of_mutation=0.01, chain=None):

        self.probability_of_mutation = probability_of_mutation
        self.count_of_genes = count_of_genes

        if chain is not None:
            self.chain = chain
        else:
            self.chain = np.array([random.randint(0, 1) for i in range(self.count_of_genes)])

    def __str__(self):
        return "[DNA chain]: \n{}".format(self.chain)

    def __add__(self, other):
        crossover_point = random.randint(1, self.count_of_genes - 1)

        child_1_chain = self.chain.copy()
        child_2_chain = other.chain.copy()

        temp = child_1_chain[crossover_point:].copy()
        child_1_chain[crossover_point:] = child_2_chain[crossover_point:].copy()
        child_2_chain[crossover_point:] = temp.copy()

        child_1 = DNA(chain=child_1_chain.copy())
        child_2 = DNA(chain=child_2_chain.copy())
        return [child_1, child_2]

    def __invert_gen(self, gen_number):
        self.chain[gen_number] = not self.chain[gen_number]

    def mutation(self):
        for gen in range(self.count_of_genes - 1):
            probability = random.random()
            if probability < self.probability_of_mutation:
                self.__invert_gen(gen)


class GA:
    def __init__(self):
        self.count_of_individuals = 10
        self.count_of_generations = 100
        self.probability_of_mutation = 0.01
        self.data_matrix = np.array([5, 6, 3, 4, 5, 2, 3, 8, 4, 6, 3, 9, 15, 1, 7])
        self.desired_value = 15

        self.count_of_genes = self.data_matrix.shape[0]
        self.parent_individual = []
        self.fitness_matrix = np.array([])
        self.function_matrix = np.array([])

        np.set_printoptions(linewidth=np.inf)
        np.set_printoptions(threshold=np.inf)

        self.__init_population()

    def __init_population(self):
        for i in range(self.count_of_individuals):
            self.parent_individual.append(DNA(count_of_genes=self.count_of_genes))

    def print_dna_matrix(self):
        for i in range(self.count_of_individuals):
            print(self.parent_individual[i].chain)

    def __calculate_function(self):
        self.function_matrix = []
        # print(self.data_matrix)
        for i in range(self.count_of_individuals):
            self.function_matrix.append((self.parent_individual[i].chain * self.data_matrix).sum())
        print(self.function_matrix)

    def __calculate_fitness(self):
        self.fitness_matrix = []

        for i in range(self.count_of_individuals):
            self.fitness_matrix.append(1 / abs(self.function_matrix[i] - self.desired_value))
        print(self.fitness_matrix)

        sum_fitness_matrix = sum(self.fitness_matrix)
        for i in range(self.count_of_individuals):
            self.fitness_matrix[i] = self.fitness_matrix[i] / sum_fitness_matrix
        print(self.fitness_matrix)
        print(sum(self.fitness_matrix))

    def __gen_mutation(self):
        for i in range(self.count_of_individuals):
            self.parent_individual[i].mutation()

    def __get_roulette_selected(self):
        pandom_val = random.random()
        pass

    def solve(self):
        self.__calculate_function()
        self.__calculate_fitness()

        self.__gen_mutation()
        self.print_dna_matrix()

