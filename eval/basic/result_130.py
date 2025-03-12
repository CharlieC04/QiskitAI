from qiskit.circuit import QuantumCircuit
def inv_circuit(n):
    """ Create a quantum circuit with 'n' qubits. Apply Hadamard gates to the second and third qubits.
    Then apply CNOT gates between the second and fourth qubits, and between the third and fifth qubits.
    Finally give the inverse of the quantum circuit.
    """
    qc = QuantumCircuit(n)
    qc.h(1)
    qc.h(2)
    qc.cx(1,3)
    qc.cx(2,4)
    qc.inverse()
    return qc

qc = inv_circuit(5)
qc.draw()

from qiskit.quantum_info import Statevector
from qiskit.visualization import plot_bloch_multivector

# Create a quantum circuit with 5 qubits.
qc = QuantumCircuit(5)

# Apply Hadamard gates to the second and third qubits.
qc.h(1)
qc.h(2)

# Apply CNOT gates between the second and fourth qubits, and between the third and fifth qubits.
qc.cx(1,3)
qc.cx(2,4)

# Create a statevector from the quantum circuit.
statevector = Statevector.from_instruction(qc)

# Plot the statevector on the Bloch sphere.
plot_bloch_multivector(statevector)

from qiskit.