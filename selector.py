import numpy as np
import random


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
        # Количество особей в поколении
        self.count_of_individuals = 10

        # Количество поколений работы алгоритма
        self.count_of_generations = 1000

        # Вероятность мутации каждого гена в составе цепочки ДНК
        self.probability_of_mutation = 0.01

        # Данные для поиска
        self.data_matrix = np.array([5, 6, 3, 4, 5, 2, 3, 8, 4, 6, 3, 9, 15, 1, 7])

        # self.competence_level_matrix = np.array([])
        # self.desired_values = np.array([])

        # Искомое число
        self.desired_value = 15

        # Количество генов, соответствующее количеству перебираемых переменных
        self.count_of_genes = self.data_matrix.shape[0]

        # Матрица родительских особей
        self.parent_individual = []

        # Матрица приспособленности особей
        self.fitness_matrix = np.array([])

        # Значение целевой функции для каждой из особей
        self.function_matrix = np.array([])

        # Матрица потомков
        self.__children_matrix = []

        # Матрица возможных решений
        self.solutions_matrix = []

        # Настройка вывода данных в консоль
        np.set_printoptions(linewidth=np.inf)
        np.set_printoptions(threshold=np.inf)

        # Инициализировать начальную популяцию
        self.__init_population()

    # Инициализировать популяцию
    # заполнить матрицу родительских особей объектами класса DNA
    def __init_population(self):
        for i in range(self.count_of_individuals):
            self.parent_individual.append(DNA(count_of_genes=self.count_of_genes))

    # Функция вывода цепочки ДНК всех родительских особей текущего поколения
    def print_dna_matrix(self):
        for i in range(self.count_of_individuals):
            print(self.parent_individual[i].chain)

    # Функция расчета значения целевой функции для каждой особи поколения
    def __calculate_function(self):
        self.function_matrix = []
        # print(self.data_matrix)
        for i in range(self.count_of_individuals):
            self.function_matrix.append((self.parent_individual[i].chain * self.data_matrix.copy()).sum())
        # print(" [Function matrix]\n", self.function_matrix)

    # Функция расчета приспособленности каждой особи
    def __calculate_fitness(self):
        self.fitness_matrix = []

        for i in range(self.count_of_individuals):
            if self.function_matrix[i] - self.desired_value == 0:
                self.fitness_matrix.append(1)
            else:
                self.fitness_matrix.append(1 / abs(self.function_matrix[i] - self.desired_value))
        # print(self.fitness_matrix)

        sum_fitness_matrix = sum(self.fitness_matrix)
        for i in range(self.count_of_individuals):
            self.fitness_matrix[i] = self.fitness_matrix[i] / sum_fitness_matrix

    # Функция реализации мутации гена в каждом гене цепочки ДНК
    def __gen_mutation(self):
        for i in range(self.count_of_individuals):
            self.parent_individual[i].mutation()

    # Функция
    def __get_roulette_selected(self):
        random_value = random.random()
        i = 0
        low_limit = 0
        high_limit = self.fitness_matrix[0]
        while i != self.count_of_individuals:
            if (random_value > low_limit) and (random_value < high_limit):
                return i
            i += 1
            low_limit = high_limit
            high_limit += self.fitness_matrix[i]

    def __create_children(self):
        self.__children_matrix = []
        for count in range(self.count_of_individuals // 2):
            i = self.__get_roulette_selected()
            j = self.__get_roulette_selected()

            while i == j:
                j = self.__get_roulette_selected()

            two_children = self.parent_individual[i] + self.parent_individual[j]
            self.__children_matrix.append(two_children[0])
            self.__children_matrix.append(two_children[1])
        # for i in range(self.count_of_individuals):
        # print(self.__children_matrix[i].chain)

    def __children_to_parent(self):
        self.parent_individual = []
        for i in range(self.count_of_individuals):
            self.parent_individual.append(self.__children_matrix[i])

    def __add_solution_option(self):
        pass

    def __run_generation(self):
        self.__calculate_function()
        self.__calculate_fitness()

        # print("[Parents matrix]")
        # self.print_dna_matrix()
        for i in range(self.count_of_individuals):
            print("[Individual # {}]   [Function]:{}   [Fitness]: {:.3f}   [DNA Chain]: {}".format(i,
                                                                             self.function_matrix[i],
                                                                             self.fitness_matrix[i],
                                                                             self.parent_individual[i].chain))
        self.__gen_mutation()
        self.__create_children()
        self.__children_to_parent()

    def solve(self):
        for generation in range(self.count_of_generations):
            print("[Generation # {}]===============================================================".format(generation))
            self.__run_generation()
