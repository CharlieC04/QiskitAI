from qiskit.quantum_info import random_statevector, state_fidelity, Statevector
def fidelity_dataset():
    """ Return a list of ten pairs of one qubit state vectors whose state fidelity is greater than 0.9.
    """
    dataset = []
    for i in range(10):
        state = random_statevector(2)
        dataset.append((state, state))
    return dataset

dataset = fidelity_dataset()

# +
from qiskit.circuit.library import RealAmplitudes
from qiskit.algorithms.optimizers import COBYLA
from qiskit.algorithms.minimum_eigensolvers import VQE
from qiskit.primitives import Estimator
from qiskit.utils import algorithm_globals

algorithm_globals.random_seed = 1234

ansatz = RealAmplitudes(num_qubits=1, reps=1)
optimizer = COBYLA(maxiter=1000)
vqe = VQE(ansatz, optimizer, estimator=Estimator())

# +
from qiskit.algorithms.optimizers import SPSA
from qiskit.algorithms.minimum_eigensolvers import QAOA
from qiskit.primitives import Sampler

algorithm_globals.random_seed = 1234

optimizer = SPSA(maxiter=1000