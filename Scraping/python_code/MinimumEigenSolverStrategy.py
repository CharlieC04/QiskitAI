from qiskit import QuantumCircuit
from qiskit.algorithms import NumPyMinimumEigensolver
from qiskit_optimization.algorithms import MinimumEigenOptimizer

from VehicleRouting.framework.interfaces.MinimumEigenSolver import MinimumEigenSolver


class QAOAMinimumEigenSolver(MinimumEigenSolver):
    def __init__(self, factory):
        self.qaoa = factory.create_qaoa()
        self.optimizer = MinimumEigenOptimizer(self.qaoa)

    def solve(self, quadratic_program):
        return self.optimizer.solve(quadratic_program)

    def get_optimal_circuit(self) -> QuantumCircuit:
        return self.qaoa.get_optimal_circuit()

    def get_optimal_vector(self):
        return self.qaoa.get_optimal_vector()

    def get_optimal_cost(self):
        return self.qaoa.get_optimal_cost()

    def get_probabilities(self):
        return self.qaoa.get_probabilities_for_counts()

    def get_optimizer(self):
        return self.optimizer

    def get_qaoa(self):
        return self.qaoa


class ExactMinimumEigenSolver(MinimumEigenSolver):
    def __init__(self):
        self.exact_minimum_eigen_solver = NumPyMinimumEigensolver()
        self.optimizer = MinimumEigenOptimizer(self.exact_minimum_eigen_solver)

    def solve(self, quadratic_program):
        return self.optimizer.solve(quadratic_program)

    def get_optimizer(self):
        return self.optimizer

    def get_exact_minimum_eigen_solver(self):
        return self.exact_minimum_eigen_solver
