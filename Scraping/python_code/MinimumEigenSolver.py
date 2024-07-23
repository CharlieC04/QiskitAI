from abc import abstractmethod, ABC

from qiskit import Aer
from qiskit.algorithms import NumPyMinimumEigensolver, QAOA
from qiskit.algorithms.optimizers import optimizer, COBYLA
from qiskit_optimization.algorithms import MinimumEigenOptimizer
from qiskit_optimization.problems import quadratic_program


class MinimumEigenSolver(ABC):
    @abstractmethod
    def solve(self, quadratic_program):
        pass


