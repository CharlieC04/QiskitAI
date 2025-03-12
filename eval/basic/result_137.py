from qiskit.quantum_info import random_density_matrix, entanglement_of_formation
def entanglement_dataset(ε):
    """ Return a dataset of density matrices whose 2-qubit entanglement of formation is within given tolerance.
    """
    dataset = []
    for _ in range(1000):
        rho = random_density_matrix(2)
        ent = entanglement_of_formation(rho)
        if ent < ε:
            dataset.append(rho)
    return dataset

dataset = entanglement_dataset(0.01)

from qiskit.circuit.library import RealAmplitudes

ansatz = RealAmplitudes(2, reps=2)

from qiskit.algorithms import VQE
from qiskit.algorithms.optimizers import COBYLA

vqe = VQE(ansatz, COBYLA(maxiter=100))

from qiskit.primitives import Estimator

estimator = Estimator()

from qiskit.utils import algorithm_globals

algorithm_globals.random_seed = 1234

from qiskit.utils import QuantumInstance

quantum_instance = QuantumInstance(
    estimator,
    shots=1000,
    seed_simulator=algorithm_globals.random_seed,
    seed_transpiler=algorithm_globals.random_seed,
