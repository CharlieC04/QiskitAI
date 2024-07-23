import networkx as nx
import numpy as np
from Helper_Functions import getBestMaxcut, custom_graphs, ry_simulator, greedyMaxcutSolver, customSATSolverCircuit
from qiskit import transpile, Aer
from QAOA_Cost_Function import CostFunction

v = 6
d = 3


for i in range(0, 1):

    graph = nx.random_graphs.random_regular_graph(d, v, seed=16)
    print(graph.edges())
    cost = CostFunction('maxcut', graph)
    g = greedyMaxcutSolver(graph, cost)
    b = getBestMaxcut(cost, v)
    print(g, b)


