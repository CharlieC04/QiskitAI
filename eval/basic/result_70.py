from qiskit import QuantumCircuit
def create_quantum_circuit_based_h0_cswap012_h1_csdg10():
    """ Build a Quantum Circuit composed by the gates H in Quantum register 0, Controlled-SWAP gate, also known as the Fredkin gate in quantum register 0 1 2, H gate in quantum register 1 and Controlled-S dagger gate in quantum register 1 0.
    """
    qc = QuantumCircuit(3)
    qc.h(0)
    qc.cswap(0, 1, 2)
    qc.h(1)
    qc.csdg(1, 0)
    return qc

qc = create_quantum_circuit_based_h0_cswap012_h1_csdg10()
qc.draw()