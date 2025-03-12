from qiskit import QuantumCircuit
def create_quantum_circuit(n_qubits):
    """ Generate a Quantum Circuit for the given int 'n_qubits' and return it.
    """
    # Create a Quantum Circuit with 'n_qubits' qubits
    circuit = QuantumCircuit(n_qubits)
    
    # Add a H gate on each qubit
    for qubit in range(n_qubits):
        circuit.h(qubit)
    
    # Return the circuit
    return circuit

n_qubits = 3
circuit = create_quantum_circuit(n_qubits)
circuit.draw()