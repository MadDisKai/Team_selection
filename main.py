import selector
import numpy as np

if __name__ == '__main__':

    prob = selector.GA()
    prob.solve()
    prob.print_result()

    """
    test = selector.Data()
    # print(test.get_employee_count())
    print(test.get_fitness_value(np.array([1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1])))        # 30
    print(test.get_fitness_value(np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0])))        # 15
    print(test.get_fitness_value(np.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])))
    print(test.get_fitness_value(np.array([1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])))        # 9
    print(test.is_relevant_solution(np.array([0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0])))
    """