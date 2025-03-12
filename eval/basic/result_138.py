from qiskit.quantum_info import mutual_information, random_density_matrix
def mutual_information_dataset(ε):
    """ Return a list of density matrices whose mutual information is greater than the given tolerance.
    """
    dataset = []
    while len(dataset) < 1000:
        rho = random_density_matrix(2)
        mi = mutual_information(rho)
        if mi > ε:
            dataset.append(rho)
    return dataset

dataset = mutual_information_dataset(0.5)

from qiskit.circuit.library import RealAmplitudes
from qiskit.primitives import Estimator
from qiskit.algorithms import VQE
from qiskit.algorithms.optimizers import COBYLA
from qiskit.utils import QuantumInstance
from qiskit.quantum_info import Statevector
from qiskit.providers.aer import AerSimulator
from qiskit.utils import algorithm_globals

algorithm_globals.random_seed = 1234

backend = AerSimulator()
quantum_instance = QuantumInstance(backend)

ansatz = RealAmplitudes(num_qubits=2, reps=1)
estimator = Estimator()
vqe = VQE(ansatz, estimator, COBYLA(maxiter=100))

def vqe_