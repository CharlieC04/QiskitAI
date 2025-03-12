from qiskit.converters import circuit_to_gate
def circ_to_gate(circ):
    """ Given a QuantumCircuit, convert it into a gate equivalent to the action of the input circuit and return it.
    """
    return circuit_to_gate(circ)

def gate_to_circ(gate):
    """ Given a Gate, convert it into a QuantumCircuit equivalent to the action of the input gate and return it.
    """
    return gate_to_circuit(gate)