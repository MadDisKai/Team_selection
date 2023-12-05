import selector
# import pandas as pd
# import numpy as np
# import time

if __name__ == '__main__':
    
    PAIR_COUNT = 0
    id_array = []
    value_array = []

    prob = selector.Data()

    pp = selector.Solver(data=prob)

    # pp.enable_logger()
    pp.set_try_count(1)
    pp.set_current_algorithm(3)

    pp.solve()
