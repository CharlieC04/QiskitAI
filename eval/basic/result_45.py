from qiskit.quantum_info.random import random_clifford
def get_random_clifford(n_qubits):
    """ Generate a random clifford circuit using the input n_qubit as number of qubits.
    """
    clifford = random_clifford(n_qubits)
    return clifford

def get_random_clifford_gate(n_qubits):
    """ Generate a random clifford gate using the input n_qubit as number of qubits.
    """
    clifford = get_random_clifford(n_qubits)
    clifford_gate = clifford.to_gate()
    return clifford_gate

def get_random_clifford_circuit(n_qubits, n_layers):
    """ Generate a random clifford circuit using the input n_qubit as number of qubits and n_layers as number of layers.
    """
    clifford_circuit = QuantumCircuit(n_qubits)
    for _ in range(n_layers):
        clifford_gate = get_random_clifford_gate(n_qubits)
        clifford_circuit.append(clifford_gate, range(n_qubits))
    return clifford_circuit

def get_random_clifford_circuit_with_measurements(n_qubits