from qiskit import QuantumCircuit
from qiskit.quantum_info import DensityMatrix, concurrence
def calculate_bell_state_properties():
    """ Construct a Phi plus Bell state quantum circuit, compute its Density Matrix and Concurrence, and return these results in a tuple in the same order.
    """
    # Create a quantum circuit with two qubits
    qc = QuantumCircuit(2)

    # Add a Hadamard gate to the first qubit
    qc.h(0)

    # Add a CNOT gate between the first and second qubits
    qc.cx(0, 1)

    # Compute the density matrix of the quantum circuit
    density_matrix = DensityMatrix(qc)

    # Compute the concurrence of the quantum circuit
    concurrence_value = concurrence(density_matrix)

    return density_matrix, concurrence_value

calculate_bell_state_properties()