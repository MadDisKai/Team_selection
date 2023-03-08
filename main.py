import selector
import numpy as np

if __name__ == '__main__':

    prob = selector.Data()
    prob.read_employee_competence_from_xlsx()
    prob.read_project_competence_from_xlsx()
    prob.read_employee_rate_from_xlsx()

    # prob.print_employee_competence_table()
    # prob.print_project_competence_table()

"""
    prob_A = selector.GA(data=prob)
    prob_A.solve()
    prob_A.print_result()
"""
