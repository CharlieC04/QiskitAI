from qiskit.circuit.library import Diagonal
from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator
def create_diagonal_circuit(diag: list) -> QuantumCircuit:
    """ Create a QuantumCircuit with a Diagonal gate applied to the qubits.
    The diagonal elements are provided in the list 'diag'.
    """
    # Create a QuantumCircuit with the same number of qubits as the diagonal elements.
    circuit = QuantumCircuit(len(diag))

    # Apply the Diagonal gate to the qubits.
    circuit.diagonal(diag, range(len(diag)))

    return circuit

# Create a diagonal circuit with the diagonal elements [1, 2, 3].
circuit = create_diagonal_circuit([1, 2, 3])

# Print the circuit.
print(circuit)

# Create a diagonal circuit with the diagonal elements [1, 2, 3].
circuit = create_diagonal_circuit([1, 2, 3])

# Print the circuit.
print(circuit)

# Create a diagonal circuit with the diagonal elements [1, 2, 3].
circuit = create_diagonal_circuit([1, 2, 3])

# Print the circuit.
print(circuit)

# Create a diagonal circuit with the diagonal elements [1, 2, 3].
circuit = create_diagonal_circuit([1, 2, 3])

# Print the circuit.
print(circuit)

