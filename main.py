import selector
import pandas as pd
import numpy as np
import time

if __name__ == '__main__':

    prob = selector.Data()
    alg = selector.Enum()

    # prob.print_employee_competence_table()

    # pp = selector.Solver(data=prob)
    # pp.solve(alg.genetic_algorithm_unfixed_population)

    pp = selector.GaGenitor(data=prob)
    pp.solve()
    pp.save_result_xlsx()

    """
    times = []
    hist = []
    fit = []
    count = 10

    for i in range(count):
    
        pp = selector.GaUnfixedPopulationSize(data=prob)
        start = time.time()
        pp.solve()
        end = time.time()

        hist.append(pp.get_hist())
        times.append(end-start)
        fit.append(pp.get_solution()['FITNESS'])

    for i in range(count):
        print(hist[i])
    for i in range(count):
        print(times[i])
    print("======")
    for i in range(count):
        print(fit[i])
    """