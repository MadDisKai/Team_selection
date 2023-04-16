import selector
import pandas as pd
import numpy as np

if __name__ == '__main__':

    prob = selector.Data()

    pp = selector.Solver(data=prob)
    pp.solve()

    # prob.print_employee_competence_table()
    # prob.print_project_competence_table()
    """
    dataA = {'E#1': 1, 'E#3': 1, 'E#14': 1, 'C#1': 23.45}
    ser = pd.Series(data=dataA, index=['E#1', 'E#3', 'E#14', 'C#1'])
    print(ser.index[0])

    probA = selector.Data()
    probA.read_employee_competence_from_xlsx()
    probA.read_project_competence_from_xlsx()
    probA.read_employee_rate_from_xlsx()

    probA.print_project_competence_table()
    probA.print_employee_competence_table()
    probA.print_employee_names()
    print(probA.get_employee_count())

    probA.delete_employees(ser)

    probA.print_employee_competence_table()
    probA.print_employee_names()
    print(probA.get_employee_count())
    """
