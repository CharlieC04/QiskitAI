from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import Sampler
from qiskit_ibm_runtime.options import SamplerOptions
def init_random_3qubit(desired_vector: [complex])-> dict:
    """ Initialize a non-trivial 3-qubit state for a given desired vector state and return counts after running it using Qiskit Sampler with the Aer simulator as backend and ser=t seed as 42.
    """
    # Initialize a 3-qubit quantum circuit
    qc = QuantumCircuit(3)
    # Apply Hadamard gates to the first two qubits
    qc.h(0)
    qc.h(1)
    # Apply a single-qubit rotation to the third qubit
    qc.rz(desired_vector[0], 2)
    # Apply a controlled-Z gate between the first and second qubits
    qc.cz(0, 1)
    # Apply a controlled-Y gate between the first and third qubits
    qc.cy(0, 2)
    # Apply a controlled-Z gate between the second and third qubits
    qc.cz(1, 2)
    # Apply a single-qubit rotation to the third qubit
    qc.rz(desired_vector[1], 2)
    # Apply a controlled-Y gate between the first and third qubits
    qc.cy(0, 2)
    # Apply a controlled-Z gate between the first and second qubits
    qc.cz(0, 1)
    # Apply a single-qubit rotation to the third qubit
    qc