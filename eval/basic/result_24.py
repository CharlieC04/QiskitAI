from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler
from numpy import isclose
def dj_algorithm(oracle: QuantumCircuit) -> bool:
    """ Given a Deutsch-Jozsa oracle in which the final qubit is the "output" qubit, return True if the oracle is constant or False otherwise.
    """
    # Create a quantum circuit with 3 qubits and 3 classical bits
    circuit = QuantumCircuit(3, 3)

    # Apply Hadamard gates to the first two qubits
    circuit.h(0)
    circuit.h(1)

    # Apply the oracle
    circuit.append(oracle, circuit.qubits)

    # Apply Hadamard gates to the first two qubits
    circuit.h(0)
    circuit.h(1)

    # Measure the first two qubits
    circuit.measure(0, 0)
    circuit.measure(1, 1)

    # Run the circuit on a statevector simulator
    sampler = StatevectorSampler()
    result = sampler.run(circuit).result()

    # Get the counts of the measurements
    counts = result.get_counts()

    # Check if the output is 00 or 11
    if '00' in counts and '11' in counts:
        return True
    else:
        return False

# Example usage
oracle = QuantumCircuit(3)
oracle.x(2)
oracle.cz(0, 2)
oracle.cz(1, 2)
