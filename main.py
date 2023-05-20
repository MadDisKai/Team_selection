import selector
import pandas as pd
import numpy as np

if __name__ == '__main__':

    prob = selector.Data()
    alg = selector.Enum()

    pp = selector.Solver(data=prob)
    pp.solve(alg.genetic_algorithm_punctuated_equilibrium)

    # pp = selector.GaPunctuatedEquilibrium(data=prob)
    # pp.solve()
    # pp.save_result_xlsx()
