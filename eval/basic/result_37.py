from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import Sampler
from qiskit.primitives.containers.primitive_result import PrimitiveResult
def bv_algorithm(s: str) -> [list, PrimitiveResult]:
    """ Illustrate a Bernstein-Vazirani algorithm routine on Qiskit and run it using Qiskit Sampler with Aer simulator as backend for a string of 0s and 1s. Return the bit strings of the result and the result itself.
    """
    # Create a quantum circuit with n qubits and n+1 classical bits
    n = len(s)
    qc = QuantumCircuit(n, n+1)

    # Apply Hadamard gates to all qubits
    qc.h(range(n))

    # Apply barrier
    qc.barrier()

    # Apply controlled-U gates
    for i in range(n):
        qc.cu1(2*float(s[i]), i, n)

    # Apply barrier
    qc.barrier()

    # Apply Hadamard gates to all qubits
    qc.h(range(n))

    # Measure all qubits
    qc.measure(range(n), range(n))

    # Run the circuit on the Aer simulator
    backend = AerSimulator()
    result = backend.run(qc).result()

    # Get the counts
    counts = result.get_counts()

    # Get the most likely bit string
    bit_string = max(counts, key=counts.get)

    # Return the bit string and the result
    return [bit_string, result]
bv_algorithm('101')
bv_algorithm('01