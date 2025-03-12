from qiskit import QuantumCircuit
def create_quantum_circuit_based_h0_cs01_h1_csdg10():
    """ Build a Quantum Circuit composed by the gates H in Quantum register 0, Controlled-S gate in quantum register 0 1, H gate in quantum register 1 and Controlled-S dagger gate in quantum register 1 0.
    """
    circuit = QuantumCircuit(2)
    circuit.h(0)
    circuit.cs(0, 1)
    circuit.h(1)
    circuit.csdg(1, 0)
    return circuit

circuit = create_quantum_circuit_based_h0_cs01_h1_csdg10()
circuit.draw()