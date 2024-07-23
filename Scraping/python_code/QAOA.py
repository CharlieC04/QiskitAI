#------------------------------------------------------------------------------
# Qaoa.py
#
# Implementation of the Quantum Approximate Optimization Algorithm (QAOA) [1],[2] 
# specifically tailored for solving the MaxCut problem on graphs [3].
# This class facilitates the creation of QAOA circuits with 
# various types of mixer operators and allows execution on a quantum simulator 
# backend provided by Qiskit.
#
# The `Qaoa` class provides methods to:
# - Initialize with QAOA parameters, graph instance, mixer type, and backend settings
# - Create cost operator and various mixer operators (x, xx, y, yy, xy)
# - Generate the complete QAOA circuit
#
# Initialization parameters include the number of QAOA layers, angles for the 
# mixer and cost operators, and options for setting verbosity, measurement, and 
# random seed. The class checks for consistency in the provided parameters and 
# supports visualizing the graph and QAOA circuit.
#
# Refs.
# [1] https://arxiv.org/abs/1411.4028
# [2] https://learning.quantum.ibm.com/tutorial/quantum-approximate-optimization-algorithm
# [3] https://en.wikipedia.org/wiki/Maximum_cut
#
# © Leonardo Lavagna 2024
# @ NESYA https://github.com/NesyaLab
#------------------------------------------------------------------------------


import numpy as np
from matplotlib import pyplot as plt
from classes import Problems as P
from functions import qaoa_utilities as utils
from qiskit import QuantumCircuit
from qiskit_aer import Aer
from typing import List, Tuple
from networkx import Graph
from qiskit.circuit import ParameterVector


class Qaoa:
    def __init__(self, p: int = 0, G: Graph = None, betas: List[float] = None, gammas: List[float] = None, 
                 mixer: str = "x", backend = Aer.get_backend('qasm_simulator'), measure: bool = True, 
                 seed: int = None, verbose: bool = True):
        """Initialize class QAOA.
        
        Args:
            p (int): Positive number of QAOA layers. The default is 0.
            G (Graph): A graph created with the Problem class used as MaxCut problem instance. The default is None.
            betas (float): Angles for the mixer operator.
            gammas (float): Angles for the cost operator.
            mixer (str): Type of mixer operator to be used. The default is "x".
            backend (Qiskit backend): Qiskit backend to execute the code on a quantum simulator. 
                                      The default is Aer.get_backend('qasm_simulator').
            measure (bool): If True measure the qaoa circuit. The default is True.
            seed (int): Seed for a pseudo-random number generator. The default is None.
            verbose (bool): If True enters in debugging mode. The default is True.
        """
        # Setup
        self.p = p
        self.G = G
        self.mixer = mixer
        self.backend = backend
        self.measure = measure
        self.verbose = verbose  
        self.seed = seed
        self.problems_class = P.Problems(p_type="custom", G=self.G)
        if self.seed is not None:
            np.random.seed(self.seed)  
        if self.G is None:
            self.N = 0
            self.w = [[]]
            self.betas = []
            self.gammas = []
        if self.G is not None:
            self.N = G.get_number_of_nodes()
            self.w = G.get_adjacency_matrix()
            if betas is None or gammas is None:
                self.betas = utils.generate_parameters(n=self.p, k=1)
                self.gammas = utils.generate_parameters(n=self.p, k=2)
            if betas is not None and gammas is not None:
                self.betas = betas
                self.gammas = gammas
                
        # Checking...
        if self.problems_class.__class__.__name__ != self.G.__class__.__name__ and G is not None:
            raise Exception("Invalid parameters. The graph G should be created with the Problems class.")
        if (self.p == 0 and self.G is not None) or (self.p > 0 and G is None):
            raise ValueError("If G is not the empty graph p should be a strictly positive integer, and viceversa.")       
        if len(self.betas) != p or len(self.gammas) != p or len(self.betas) != len(self.gammas):
            raise ValueError("Invalid angles list. The length of betas and gammas should be equal to p.")
            
        # Initializing...
        if self.verbose is True:            
            print(" --------------------------- ")
            print("| Intializing Qaoa class... |".upper())
            print(" --------------------------- ")     
            print("-> Getting problem instance...".upper())
            if self.G is not None:
                self.G.get_draw()
                plt.show()
            if self.G is None:
                print("\t * G = ø")
            if self.betas is None and self.G is not None:
                print("-> Beta angles not provided. Generating angles...".upper())
                print(f"\t * betas = {self.betas}")
            if self.gammas is None and self.G is not None:
                print("-> Gamma angles not provided. Generating angles...".upper())
                print(f"\t * gammas = {self.gammas}")
            print("-> Getting the ansatz...".upper())
            if self.G is not None:
                print(self.get_circuit())
            if self.G is None:
                print("\t  * Qaoa circuit = ø")
            print("-> The Qaoa class was initialized with the following parameters.".upper())
            print(f"\t * Number of layers: p = {self.p};")
            if self.G is None:
                print(f"\t * Graph: G = ø;")
            if self.G is not None:
                print(f"\t * Graph: G = {self.G.p_type};")
            print("\t * Angles:") 
            print(f"\t\t - betas = {self.betas};")
            print(f"\t\t - gammas = {self.gammas};")
            print(f"\t * Mixer Hamiltonian type: '{self.mixer}';")
            print(f"\t * Random seed: seed = {self.seed};")
            print(f"\t * Measurement setting: measure = {self.measure}.")

    
    def cost_operator(self, gamma: float) -> QuantumCircuit:
        """Create an instance of the cost operator with angle 'gamma'.
        
        Args:
            gamma (float): Angle for the cost operator.

        Returns:
            QuantumCircuit: Circuit representing the cost operator.
        """
        qc = QuantumCircuit(self.N, self.N)
        for i,j in self.G.get_edges():
            qc.cx(i, j)
            qc.rz(gamma, j)
            qc.cx(i, j)
        return qc
    
    
    def x_mixer_operator(self, beta: float) -> QuantumCircuit:
        """Create an instance of the x-mixer operator with angle 'beta'.
        
        Args:
            beta (float): Angle for the mixer operator.

        Returns:
            QuantumCircuit: Circuit representing the mixer operator.
        """
        qc = QuantumCircuit(self.N, self.N)
        for v in self.G.get_nodes():
            qc.rx(beta, v)
        return qc
    
    
    def xx_mixer_operator(self, beta: float) -> QuantumCircuit:
        """Create an instance of the xx-mixer operator with angle 'beta'.
        
        Args:
            beta (float): Angle for the mixer operator.

        Returns:
            QuantumCircuit: Circuit representing the mixer operator.
        """
        qc = QuantumCircuit(self.N, self.N)
        for i, j in self.G.get_edges():
            if self.w[i, j] > 0:
                qc.rxx(beta, i, j)

        return qc
    
    
    def y_mixer_operator(self, beta: float) -> QuantumCircuit:
        """Create an instance of the y-mixer operator with angle 'beta'.
        
        Args:
            beta (float): Angle for the mixer operator.

        Returns:
            QuantumCircuit: Circuit representing the mixer operator.
        """
        qc = QuantumCircuit(self.N, self.N)
        for v in self.G.get_nodes():
            qc.ry(2 * beta, v)
        return qc
    
    
    def yy_mixer_operator(self, beta: float) -> QuantumCircuit:
        """Create an instance of the yy-mixer operator with angle 'beta'.
        
        Args:
            beta (float): Time-slice angle for the mixer operator.

        Returns:
            QuantumCircuit: Circuit representing the mixer operator.
        """
        qc = QuantumCircuit(self.N, self.N)
        for i, j in self.G.get_edges():
            if self.w[i, j] > 0:
                qc.ryy(beta / 2, i, j)
                
        return qc
    
    
    def xy_mixer_operator(self, phi: float, psi: float) -> QuantumCircuit:
        """Create an instance of the xy-mixer operator with angle 'beta'. 
        
        Args:
            beta (float): Angle for the mixer operator.

        Returns:
            QuantumCircuit: Circuit representing the mixer operator.
        """
        qc = QuantumCircuit(self.N, self.N)
        # X_iX_j
        for i, j in self.G.get_edges():
            if self.w[i, j] > 0:
                qc.rxx(phi / 2, i, j)
        # Y_iY_j
        for i, j in self.G.get_edges():
            if self.w[i, j] > 0:
                qc.ryy(psi / 2, i, j)
                
        return qc
    
    
    def get_circuit(self) -> QuantumCircuit:
        """Create an instance of the Qaoa circuit with given parameters.
        
        Returns:
            QuantumCircuit: Circuit representing the Qaoa.
        """
        qc = QuantumCircuit(self.N, self.N)
        params = ParameterVector("params", 2 * self.p)
        betas = params[0 : self.p]
        gammas = params[self.p : 2 * self.p]
        qc.h(range(self.N))
        qc.barrier(range(self.N))
        for i in range(self.p):
            qc = qc.compose(self.cost_operator(gammas[i]))
            qc.barrier(range(self.N))
            if self.mixer == "x":
                qc = qc.compose(self.x_mixer_operator(betas[i]))
                qc.barrier(range(self.N))
            elif self.mixer == "xx":
                qc = qc.compose(self.xx_mixer_operator(betas[i]))
                qc.barrier(range(self.N))
            elif self.mixer == "y":
                qc = qc.compose(self.y_mixer_operator(betas[i])) 
                qc.barrier(range(self.N))
            elif self.mixer == "yy":
                qc = qc.compose(self.yy_mixer_operator(betas[i]))
                qc.barrier(range(self.N))
            elif self.mixer == "xy":
                qc = qc.compose(self.xy_mixer_operator(betas[i],betas[i]))
                qc.barrier(range(self.N))
            qc.barrier(range(self.N))
        if self.measure:  
            qc.measure(range(self.N), range(self.N))
        
        return qc