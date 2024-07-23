import matplotlib.pyplot as plt
import numpy as np

from VehicleRouting.standard.factories.VehicleRoutingProblemFactories import Experiment1VehicleRoutingProblemFactory
from VehicleRouting.standard.problems.VehicleRoutingProblem import VehicleRoutingProblem
from VehicleRouting.functions.functionsVehicleRouting import get_execute_circuit
from VehicleRouting.functions.functionsVehicleRouting import create_qaoa_circuit
from qiskit import Aer
from qiskit.visualization import plot_histogram
from scipy.optimize import minimize


# Setting Up Graph
from VehicleRouting.standard.plotter.GraphPlotter import GraphPlotter
from VehicleRouting.standard.concretization.GraphStrategy import SimpleExperimentProblemStrategy

problem_factory = Experiment1VehicleRoutingProblemFactory()
problem = VehicleRoutingProblem(problem_factory)
plotter = GraphPlotter(problem)
plotter.plot_problem()

graph = problem.get_graph()

# Returns a function to be optimized
p = 2
expectation = get_execute_circuit(graph)

# Optimize
initial_parameter = np.ones(2*p)
optimization_method = 'COBYLA'
optimization_object = minimize(expectation, initial_parameter, method=optimization_method)
print(optimization_object)

# Get a simulator
backend = Aer.get_backend('aer_simulator')
backend.shots = 2 ^ 12

# Create Circuit with Optimized Parameters
optimized_parameters = optimization_object.x
qc_res = create_qaoa_circuit(graph, optimized_parameters)
qc_res.draw(output="mpl")

# Run simulation with optimised parameters
counts = backend.run(qc_res, seed_simulator=10).result().get_counts()
print(counts)

# Plot Histogram
plot_histogram(counts)

plt.show()
