import math
import numpy as np
import random
import pandas as pd
from tqdm import tqdm


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


# Класс подготовки данных
class Data:
    def __init__(self):

        # Таблица для хранения значений уровней компетенций проекта
        self.__project_competence_table = np.array([20, 24, 22, 12])

        # Таблица для хранения значений уровней компетенций сотрудников [В десятичных дробях]
        """
        self.__employee_competence_table = np.array(
            [[5.27, 6.59, 1.75, 1.48, 2.55, 8.07, 1.91, 2.89, 8.54, 0.17, 9.68, 7.21, 6.69, 1.81, 7.08],
             [2.13, 8.21,  0.6, 5.16, 5.74, 3.28, 5.41, 1.26, 7.54, 7.22, 3.43, 7.01, 0.28, 5.25, 7.83],
             [5.83, 1.06, 1.42, 7.09, 8.36, 2.34, 7.73, 8.16, 2.02, 3.25, 0.94, 6.48, 1.57, 7.8,  3.9],
             [3.13, 5.38, 5.02, 8.55, 5.85, 2.03, 1.85, 3.83, 6.13, 1.71, 9.58, 3.3,  7.1,  8.21, 1.97]])
        """
        # Таблица для хранения значений уровней компетенций сотрудников [В целых числах]
        self.__employee_competence_table = np.array([[1, 8, 7, 3, 8, 6, 6, 4, 6, 7, 6, 5, 1, 6, 4],
                                                     [8, 7, 2, 6, 2, 9, 4, 10, 5, 2, 6, 10, 6, 6, 5],
                                                     [5, 5, 10, 6, 6, 10, 2, 10, 5, 5, 1, 4, 2, 6, 7],
                                                     [9, 8, 7, 4, 4, 6, 10, 1, 1, 2, 5, 1, 1, 5, 10]])

        # Словарь ID сотрудников
        self.__employee_names = []

        # Словарь названий компетенций
        self.__competence_names = []

        # Верхняя допустимая граница суммарной компетенции
        self.__competence_upper_limit = 4

        # Нижняя допустимая граница суммарной компетенции
        self.__competence_lower_limit = 0

    def __str__(self):
        return "[REQUIRED COMPETENCE VALUES]: {}\n [UPPER LIMIT]: {}\n [LOWER LIMIT]: {}".format(
            self.__project_competence_table,
            self.__competence_upper_limit,
            self.__competence_lower_limit)

    # Функция, возвращающая количество рассматриваемых работников
    def get_employee_count(self):
        return self.__employee_competence_table.shape[1]

    # Функция, возвращающая количество компетенций
    def get_competence_count(self):
        return self.__project_competence_table.shape[0]

    # Получить значения функций
    def get_functions_values(self, bin_array):
        functions_values = []
        for i in range(self.get_competence_count()):
            functions_values.append((bin_array * self.__employee_competence_table[i].copy()).sum())
        return functions_values

    # Получить значение приспособленности,
    # полученное методом функции расстояния (method of distance function)
    def get_fitness_value(self, bin_array):
        function_values = self.get_functions_values(bin_array)
        fitness = 0
        for i in range(self.get_competence_count()):
            fitness += (function_values[i] - self.__project_competence_table[i]) ** 2
        if math.sqrt(fitness) == 0:
            return 1
        else:
            return 1 / math.sqrt(fitness)

    # Проверка, подходит ли данное решение
    def is_relevant_solution(self, bin_array):

        functions_values = self.get_functions_values(bin_array)

        for i in range(len(functions_values)):
            if not (self.__project_competence_table[i] - self.__competence_lower_limit <= functions_values[i] <=
                    self.__project_competence_table[i] + self.__competence_upper_limit):
                return False
        return True

    def read_from_csv(self):
        pass


# Класс генетического алгоритма
class GA:
    def __init__(self):
        # Количество особей в поколении кратное 2
        self.count_of_individuals = 10

        # Количество поколений работы алгоритма
        self.count_of_generations = 5000

        # Вероятность мутации каждого гена в составе цепочки ДНК
        self.probability_of_mutation = 0.05

        # Инициализация класса Data
        self.data = Data()

        # Количество генов, соответствующее количеству сотрудников
        self.count_of_genes = self.data.get_employee_count()

        # Матрица родительских особей
        self.__individual = []

        # Матрица приспособленности особей
        self.fitness_matrix = np.array([])

        # Матрица потомков
        self.__children_matrix = []

        # Матрица возможных решений
        self.__solutions_matrix = pd.DataFrame(columns=['CHAIN', 'VALUES', 'FITNESS'])

        # Настройка вывода данных в консоль
        np.set_printoptions(linewidth=np.inf)
        np.set_printoptions(threshold=np.inf)

        # Инициализировать начальную популяцию
        self.__init_population()

    # Инициализировать популяцию
    # заполнить матрицу родительских особей объектами класса DNA
    def __init_population(self):
        for i in range(self.count_of_individuals):
            # self.parent_individual.append(DNA(count_of_genes=self.count_of_genes))
            self.__individual.append(DNA(count_of_genes=self.count_of_genes))

    # Функция вывода цепочки ДНК всех родительских особей текущего поколения
    def __print_dna_matrix(self):
        for i in range(len(self.__individual)):
            print(self.__individual[i].chain)

    def __print_children_matrix(self):
        print("CHILDREN MATRIX")
        for i in range(len(self.__children_matrix)):
            print(self.__children_matrix[i].chain)

    # Функция мутации гена
    def __gen_mutation(self):
        for i in range(self.count_of_individuals):
            self.__individual[i].mutation()

    # Функция скрещивания
    def __breeding(self):
        for count in range(self.count_of_individuals // 2):
            i = random.randint(0, self.count_of_individuals - 1)
            j = random.randint(0, self.count_of_individuals - 1)

            while i == j:
                j = random.randint(0, self.count_of_individuals - 1)

            two_children = self.__individual[i] + self.__individual[j]
            self.__individual.append(two_children[0])
            self.__individual.append(two_children[1])

    # Функция расчета приспособленности каждой особи
    def __calculate_fitness(self):
        self.fitness_matrix = []

        for i in range(len(self.__individual)):
            self.fitness_matrix.append(self.data.get_fitness_value(self.__individual[i].chain))

        sum_fitness_matrix = sum(self.fitness_matrix)
        for i in range(len(self.__individual)):
            self.fitness_matrix[i] = self.fitness_matrix[i] / sum_fitness_matrix

    # Функция, определяющая методом рулетки скрещивающиеся особи
    def __get_roulette_selected(self):
        random_value = random.random()
        i = 0
        low_limit = 0
        high_limit = self.fitness_matrix[0]
        while i != len(self.__individual):
            if (random_value > low_limit) and (random_value < high_limit):
                return i
            i += 1
            low_limit = high_limit
            high_limit += self.fitness_matrix[i]

    # Функция отбора особей для следующего поколения
    def __selection(self):
        self.__children_matrix = []

        for i in range(self.count_of_individuals):
            self.__calculate_fitness()
            j = self.__get_roulette_selected()
            self.__children_matrix.append(self.__individual[j])
            self.__individual.pop(j)

    # Функция переопределения потомков в родителей
    def __children_to_parent(self):
        self.__individual = []
        for i in range(self.count_of_individuals):
            self.__individual.append(self.__children_matrix[i])

    # Функция отбора возможных решений
    def __add_solution_option(self):
        for i in range(len(self.__individual)):
            if self.data.is_relevant_solution(self.__individual[i].chain):
                self.__solutions_matrix.loc[len(self.__solutions_matrix.index)] = [str(self.__individual[i].chain),
                                                                               str(self.data.get_functions_values(
                                                                                   self.__individual[i].chain)),
                                                                               self.data.get_fitness_value(
                                                                                   self.__individual[i].chain)]

    # Печать полученных результатов
    def print_result(self):
        print(self.data)
        if self.__solutions_matrix.empty:
            print("No solution was found")
        else:
            result = self.__solutions_matrix.drop_duplicates().reset_index(drop=True).sort_values('FITNESS',
                                                                                                  ascending=False)
            print(result.to_string())

    # Печать информации по текущему поколению
    def __print_gen_info(self):
        for i in range(len(self.__individual)):
            print("[Individual # {}]   [Function]:{}   [Fitness]: {:.3f}   [DNA Chain]: {}".format(i,
                                                                                    self.data.get_functions_values(
                                                                                    self.__individual[
                                                                                                           i].chain),
                                                                                    self.fitness_matrix[
                                                                                                       i],
                                                                                    self.__individual[
                                                                                                       i].chain))

    # Запуск одного поколения генетического алгоритма
    def __run_generation(self):
        self.__gen_mutation()
        self.__breeding()
        self.__selection()
        self.__children_to_parent()
        self.__add_solution_option()

    # Запуск алгоритма решения
    def solve(self):
        for generation in tqdm(range(self.count_of_generations), ncols=100):
            self.__run_generation()
        # self.__print_gen_info()
