import numpy as np
from matplotlib import pyplot as plt
from qiskit import Aer
from qiskit.visualization import plot_histogram
from scipy.optimize import minimize

from VehicleRouting.standard.factories.MaxCutFactories import TwoConnectedMaxCutFactory
from VehicleRouting.standard.problems.MaxCutProblem import MaxCutProblem
from VehicleRouting.functions.functionsMaxCut import get_expectation, get_execute_circuit, create_qaoa_circuit
from VehicleRouting.standard.plotter.GraphPlotter import GraphPlotter

number_of_vertices = 4
problem_factory = TwoConnectedMaxCutFactory()
problem = MaxCutProblem(problem_factory)
plotter = GraphPlotter(problem)
plotter.plot_problem()

graph = problem.get_graph()

expectation = get_expectation(graph, p=1)

# Returns a function to be optimized
p = 4
expectation = get_execute_circuit(graph)

# Optimize
initial_parameter = np.ones(2 * p)
optimization_method = 'COBYLA'
optimization_object = minimize(expectation, initial_parameter, method=optimization_method)
print(optimization_object)

backend = Aer.get_backend('aer_simulator')
backend.shots = 2 ^ 12

# Create Circuit with Optimized Parameters
optimized_parameters = optimization_object.x
qc_res = create_qaoa_circuit(graph, optimized_parameters)
qc_res.draw(output="mpl")

counts = backend.run(qc_res, seed_simulator=10).result().get_counts()

print(counts)
plot_histogram(counts)

plt.show()
