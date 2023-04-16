import selector
import pandas as pd
import numpy as np

if __name__ == '__main__':

    prob = selector.Data()

    pp = selector.Solver(data=prob)
    pp.solve()
