from qiskit import  QuantumCircuit
def remove_gate_in_position(circuit: QuantumCircuit, position: int):
    """ Remove the gate in the input position for the given Quantum Circuit.
    """
    circuit.remove_gate(circuit.data[position][0])
