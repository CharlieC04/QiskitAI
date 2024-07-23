import numpy as np
from matplotlib import pyplot as plt
from qiskit import QuantumCircuit
from qiskit.providers.aer import StatevectorSimulator
from qiskit.visualization import plot_histogram
from qiskit_nature.operators.second_quantization import SpinOp

from VehicleRouting.standard.concretization.CircuitPlotter import MPLCircuitPlotter
from VehicleRouting.standard.concretization.Qaoa import Qaoa
from VehicleRouting.standard.concretization.QaoaMinimizer import QaoaMinimizerImpl
from VehicleRouting.standard.factories.MaxCutFactories import TwoConnectedMaxCutFactory
from VehicleRouting.standard.factories.QaoaFactory import ExactMaxCutQaoaFactory
from VehicleRouting.standard.plotter.BarPlotter import BarPlotter
from VehicleRouting.standard.plotter.GraphPlotter import GraphPlotter
from VehicleRouting.standard.plotter.SurfacePlotter import SurfacePlotter
from VehicleRouting.standard.problems.MaxCutProblem import MaxCutProblem

# Problem
factory = TwoConnectedMaxCutFactory()
problem = MaxCutProblem(factory)
plotter = GraphPlotter(problem)
plotter.plot_problem()

# Qaoa
qaoa_factory = ExactMaxCutQaoaFactory(problem)
qaoa = Qaoa(qaoa_factory)

# Minimizer
qaoaMinimizer = QaoaMinimizerImpl(qaoa)
result, optimal_parameters, optimal_circuit = qaoaMinimizer.minimize()
print(optimal_parameters) #[1.14403197, 0.99879625]

# Plot Circuit
circuit_plotter = MPLCircuitPlotter()
circuit_plotter.plot(optimal_circuit)

# Simulate Optimized Parameters
result, counts, expectation = qaoa.simulate(optimal_parameters)

# Bar Plot
barPlotter = BarPlotter()
barPlotter.plot(counts)

# Find Surface Plot
plotter = SurfacePlotter()
plotter.plot(qaoa.get_execute_circuit())

plt.show()
