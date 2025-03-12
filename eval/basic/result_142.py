from qiskit.quantum_info import random_density_matrix, purity, DensityMatrix
import numpy as np
def purity_dataset():
    """ Return a list of 10 single qubit density matrices whose purity is greater than 0.5.
    """
    purity_list = []
    for i in range(10):
        rho = random_density_matrix(2)
        purity_list.append(purity(rho))
    return purity_list

def purity_dataset_2():
    """ Return a list of 10 single qubit density matrices whose purity is less than 0.5.
    """
    purity_list = []
    for i in range(10):
        rho = random_density_matrix(2)
        purity_list.append(purity(rho))
    return purity_list

def purity_dataset_3():
    """ Return a list of 10 single qubit density matrices whose purity is equal to 0.5.
    """
    purity_list = []
    for i in range(10):
        rho = random_density_matrix(2)
        purity_list.append(purity(rho))
    return purity_list

def purity_dataset_4():
    """ Return a list of 10 single qubit density matrices whose purity is equal to 1.
    """
    purity_list = []
    for