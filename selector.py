import math
import numpy as np
import random
import pandas as pd

from tqdm import tqdm
from tabulate import tabulate
from time import gmtime, strftime
from colorama import Fore


def time_of_work(func):
    import time

    def wrapper(self, *args, **kwargs):
        start = time.time()
        func(self, *args, **kwargs)
        end = time.time()
        print('[{}] Время выполнения: {} секунд.'.format(func.__name__, end-start))
    return wrapper


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
        self.__project_competence_table = np.array([])

        # Таблица для хранения значений уровней компетенций сотрудников [В десятичных дробях]
        self.__employee_competence_table = np.array([])

        # Таблица для хранения ставок работников
        self.__employee_rate_table = np.array([])

        # Словарь ID сотрудников
        self.__employee_names = []

        # Словарь названий компетенций
        self.__competence_names = []

        # Верхняя допустимая граница суммарной компетенции
        self.__competence_upper_limit = 4

        # Нижняя допустимая граница суммарной компетенции
        self.__competence_lower_limit = 0

        # Путь до таблицы хранения компетенций сотрудников XLSX
        self.__employee_competence_table_path = 'employee_competence_table.xlsx'

        # Путь до таблицы хранения уровней компетенции проектов
        self.__project_competence_table_path = 'project_competence_table.xlsx'

        # Путь до таблицы хранения ставок работников
        self.__employee_rate = 'employee_rate.xlsx'

        # Настройка вывода данных в консоль
        np.set_printoptions(linewidth=np.inf)
        np.set_printoptions(threshold=np.inf)

    def __str__(self):
        return "[REQUIRED COMPETENCE VALUES]: {}\n [UPPER LIMIT]: {}\n [LOWER LIMIT]: {}".format(
            self.__project_competence_table,
            self.__competence_upper_limit,
            self.__competence_lower_limit)

    # Функция чтения данных о компетенциях сотрудников
    def read_employee_competence_from_xlsx(self):
        print('Reading employee competences from {}'.format(self.__employee_competence_table_path))
        table = pd.read_excel(self.__employee_competence_table_path, index_col=0)
        self.__employee_competence_table = table.copy().transpose().to_numpy()
        self.__competence_names = table.copy().columns.to_list()
        self.__employee_names = table.copy().index.to_list()

    # Функция чтения данных о компетенциях сотрудников [ПЕРЕПИСАТЬ ПОСЛЕДНЮЮ СТРОКУ]
    def read_project_competence_from_xlsx(self):
        print('Reading project competences from {}'.format(self.__project_competence_table_path))
        table = pd.read_excel(self.__project_competence_table_path, index_col=0)
        self.__project_competence_table = table.copy().to_numpy()[0]  # < = ВОТ ЭТУ
        # print(self.__project_competence_table[0])

    # Функция чтения значений ставок сотрудников
    def read_employee_rate_from_xlsx(self):
        print('Reading employee rate from {}'.format(self.__employee_rate))
        table = pd.read_excel(self.__employee_rate, index_col=0)
        self.__employee_rate_table = table.transpose().copy().to_numpy()[0]
        print(self.__employee_rate_table)

    # Функция вывода таблицы уровней компетенции всех сотрудников
    def print_employee_competence_table(self):
        print("EMPLOYEE COMPETENCES TABLE:\n", self.__employee_competence_table)

    # Функция вывода таблицы необходимых компетенций проектов
    def print_project_competence_table(self):
        print("PROJECT COMPETENCES TABLE:\n", self.__project_competence_table)

    # Функция вывода имен сотрудников
    def print_employee_names(self):
        print(self.__employee_names)

    # Функция вывода названий компетенций
    def print_competence_name(self):
        print(self.__competence_names)

    # ==============================[GETTERS]===========================================================================

    # Функция, возвращающая таблицу компетенций сотрудников
    def get_employee_competence_table(self):
        return self.__employee_competence_table

    # Функция, возвращающая таблицы необходимых компетенций проектов
    def get_project_competence_table(self):
        return self.__project_competence_table

    # Функция, возвращающая имена сотрудников
    def get_employee_names(self):
        return self.__employee_names

    # Функция, возвращающая названия компетенций
    def get_competence_names(self):
        return self.__competence_names

    # Функция, возвращающая количество рассматриваемых работников
    def get_employee_count(self):
        return self.__employee_competence_table.shape[1]

    # Функция, возвращающая количество компетенций
    def get_competence_count(self):
        return self.__project_competence_table.shape[0]

    # Получить значения функций
    def get_functions_values(self, bin_array):
        """
        functions_values = []
        for i in range(self.get_competence_count()):
            functions_values.append((bin_array * self.__employee_competence_table[i].copy()).sum())
        """
        functions_values = np.sum(bin_array * self.__employee_competence_table.copy(), axis=1)
        return functions_values

    # Получить значение приспособленности,
    # полученное методом функции расстояния (method of distance function)
    # @time_of_work
    def get_fitness_value(self, bin_array):
        function_values = self.get_functions_values(bin_array)
        fitness = sum((np.array(function_values).copy() - self.__project_competence_table.copy()) ** 2)
        if math.sqrt(fitness) == 0:
            return 1
        else:
            return 1 / math.sqrt(fitness)

    # ==============================[SETTERS]===========================================================================

    # Функция установки верхней границы допустимых решений
    def set_competence_upper_limit(self, upper_level):
        self.__competence_upper_limit = upper_level

    # Функция установки нижней границы допустимых решений
    def set_competence_lower_limit(self, lower_level):
        self.__competence_lower_limit = lower_level

    # ==================================================================================================================

    # Проверка, подходит ли данное решение
    def is_relevant_solution(self, bin_array):

        functions_values = self.get_functions_values(bin_array)

        for i in range(len(functions_values)):
            if not (self.__project_competence_table[i] - self.__competence_lower_limit <= functions_values[i] <=
                    self.__project_competence_table[i] + self.__competence_upper_limit):
                return False
        return True


# Класс генетического алгоритма
class GA:
    def __init__(self, data=Data()):
        # Количество особей в поколении кратное 2
        self.count_of_individuals = 100

        # Количество поколений работы алгоритма
        self.count_of_generations = 100

        # Вероятность мутации каждого гена в составе цепочки ДНК
        self.probability_of_mutation = 0.05

        # Инициализация класса Data
        self.data = data

        # Количество генов, соответствующее количеству сотрудников
        self.count_of_genes = self.data.get_employee_count()

        # Матрица родительских особей
        self.__individual = []

        # Матрица приспособленности особей
        self.fitness_matrix = np.array([])

        # Матрица потомков
        self.__children_matrix = []

        # Матрица возможных решений
        row_columns_names = []
        row_columns_names.extend(self.data.get_employee_names())
        row_columns_names.extend(self.data.get_competence_names())
        row_columns_names.append('FITNESS')
        self.__solutions_matrix = pd.DataFrame(columns=row_columns_names)

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

    # Функция вывода цепочки ДНК всех дочерних особей текущего поколения
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
    # @time_of_work
    def __calculate_fitness(self):
        self.fitness_matrix = []

        for i in range(len(self.__individual)):
            self.fitness_matrix.append(self.data.get_fitness_value(self.__individual[i].chain))

        sum_fitness_matrix = sum(self.fitness_matrix)
        self.fitness_matrix = np.divide(self.fitness_matrix, sum_fitness_matrix)
        """
        for i in range(len(self.__individual)):
            self.fitness_matrix[i] = self.fitness_matrix[i] / sum_fitness_matrix
        """

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
    # @time_of_work
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
                row = []
                row.extend(self.__individual[i].chain)
                row.extend(self.data.get_functions_values(self.__individual[i].chain))
                row.append(str(self.data.get_fitness_value(self.__individual[i].chain)))
                # print(row)
                self.__solutions_matrix.loc[len(self.__solutions_matrix.index)] = row

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def __add_solution(self):
        for i in range(len(self.__individual)):
            row = []
            row.extend(self.__individual[i].chain)
            row.extend(self.data.get_functions_values(self.__individual[i].chain))
            row.append(str(self.data.get_fitness_value(self.__individual[i].chain)))
            self.__solutions_matrix.loc[len(self.__solutions_matrix.index)] = row
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    # Печать полученных результатов
    def print_result(self):
        print(self.data)
        if self.__solutions_matrix.empty:
            print("No solution was found")
        else:
            print("\n[SOLUTIONS]\n")
            self.__solutions_matrix = self.__solutions_matrix.drop_duplicates().sort_values('FITNESS',
                                                                           ascending=False).reset_index(drop=True)
            print(tabulate(self.__solutions_matrix, headers='keys', stralign='center', tablefmt='pipe'))
            print("________________________")
            print("* E#1 -- Employee #1")
            print("* C#1 -- Competence #1")

    # Печать информации по текущему поколению
    def __print_gen_info(self):
        for i in range(len(self.__individual)):
            print("[Individual # {}]   [Function]:{}   [Fitness]: {:.3f}   [DNA Chain]: {}".format(i,
                                                                                    self.data.get_functions_values(
                                                                                    self.__individual[i].chain),
                                                                                    self.fitness_matrix[i],
                                                                                    self.__individual[i].chain))

    # Запуск одного поколения генетического алгоритма
    def __run_generation(self):
        self.__gen_mutation()
        self.__breeding()
        self.__selection()
        self.__children_to_parent()
        self.__add_solution_option()
        # self.__add_solution()

    # Запуск алгоритма решения
    def solve(self):
        for generation in tqdm(range(self.count_of_generations), ncols=100, bar_format="%s{l_bar}{bar}{r_bar}"
                                                                                       % Fore.GREEN):
            self.__run_generation()
        # self.__print_gen_info()

    # Функция печати полученных результатов в файл xlsx
    def save_result_xlsx(self):
        if self.__solutions_matrix.empty:
            print("Nothing to write")
        else:
            self.__solutions_matrix.to_excel("output_{}.xlsx".format(strftime("%Y_%m_%d_%H_%M_%S", gmtime())))

