#------------------------------------------------------------------------------
# qaoa_optimizers.py
#
# This module provides optimization routines for Quantum Approximate Optimization 
# Algorithm (QAOA) [1],[2] instances applied to the Maximum Cut (MaxCut) problem [3]. 
# The functions facilitate the optimization of QAOA parameters using classical 
# optimization methods.
#
# The module includes the following functions:
# - objective_function(init_point, circuit, shots): Computes the objective 
#   function for QAOA by running the quantum circuit and evaluating the MaxCut 
#   energy.
# - callback(x): Callback function for counting the number of optimization steps 
#   during the optimization process.
# - simple_optimization(circuit, method='COBYLA', seed=None, shots=1024, 
#   verbose=True): Performs a simple optimization routine using a specified 
#   classical optimization method (default is 'COBYLA') and returns the optimized 
#   parameters and objective function value.
#
# Refs.
# [1] https://arxiv.org/abs/1411.4028
# [2] https://learning.quantum.ibm.com/tutorial/quantum-approximate-optimization-algorithm
# [3] https://en.wikipedia.org/wiki/Maximum_cut
#
# © Leonardo Lavagna 2024
# @ NESYA https://github.com/NesyaLab
#------------------------------------------------------------------------------


import random 
import numpy as np
from typing import List, Tuple
from networkx import Graph
from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
from scipy.optimize import minimize
from functions import maxcut_utilities as m_utils
from config import backend, verbose


num_evaluations = 0


def objective_function(init_point, circuit, shots):
        # Setup
        G = circuit.G
        qc = circuit.get_circuit()
        qc = qc.assign_parameters(init_point)
        # Executing the circuit to get the energies...
        t_qc = transpile(qc, backend=backend)
        job = backend.run(t_qc, shots=shots)
        counts = job.result().get_counts(qc)
        # Getting the results...
        energy = m_utils.compute_maxcut_energy(G, m_utils.invert_counts(counts), verbose=verbose)
        
        return -energy
        

def callback(x: List):
    """
    Function to be called at each iteration of the optimization step (in the minimize method) to count the number of optimization steps.

    Args:
        x (list): current solution of the optimization step
    """
    global num_evaluations
    num_evaluations += 1


def simple_optimization(circuit, method: str = 'COBYLA', seed: int = None, shots: int = 1024, verbose: bool = True) -> Tuple[np.ndarray, float]:
    """
    Perform a simple optimization routine.

    Args:
        circuit (QuantumCircuit): Quantum circuit.
        method (str): Type of optimizer. The default is 'COBYLA'.
        seed (int): Seed needed for reproducibility. The default is None.
        verbose (bool): If True enters in debugging mode. The default is False.

    Returns:
        tuple: Optimized parameters and corresponding objective function value.
    """
    # Setup
    betas = circuit.betas
    gammas = circuit.gammas
    init_point = list(betas) + list(gammas)
    if verbose:
        print(" --------------------------------- ")
        print("| Parameters for the optimization. |".upper())
        print(" --------------------------------- ")
        print("\t * betas:", betas)
        print("\t * gammas:", gammas)
        print("\t * init_point:", init_point)
    
    # Optimizing... 
    if verbose is True:
        print(" --------------- ")
        print("| Optimizing... |".upper())
        print(" --------------- ")
        optimizer = minimize(objective_function, init_point, args=(circuit,shots), callback=callback, method=method)   
    elif verbose is False:
        optimizer = minimize(objective_function, init_point, args=(circuit,shots), method=method)
        
    # Getting the results...  
    optimal_value = -optimizer.fun
    optimal_angles = optimizer.x
    if verbose:
        print(" --------- ")
        print("| Results. |".upper())
        print(" --------- ")
        print("\t * optimal_anlges:", optimal_angles)
        print("\t * optimal_value:", optimal_value)
    
    return optimizer.x, optimizer.fun