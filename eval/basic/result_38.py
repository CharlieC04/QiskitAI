from qiskit import QuantumCircuit
def create_quantum_circuit_based_h0_crz01_h1_cry10(theta):
    """ Build a 2-qubit Quantum Circuit composed by H gate in Quantum register 0, Controlled-RZ gate in quantum register 0 1 with given input theta value, H gate in quantum register 1 and Controlled-RY gate in quantum register 1 0 with given input theta value.
    """
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.crz(theta, 0, 1)
    qc.h(1)
    qc.cry(theta, 1, 0)
    return qc

qc = create_quantum_circuit_based_h0_crz01_h1_cry10(0.5)
qc.draw()

from qiskit import QuantumCircuit
def create_quantum_circuit_based_h0_crz01_h1_cry10(theta):
    """ Build a 2-qubit Quantum Circuit composed by H gate in Quantum register 0, Controlled-RZ gate in quantum register 0 1 with given input theta value, H gate in quantum register 1 and Controlled-RY gate in quantum register 1 0 with given input theta value.
    """
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.crz(theta, 0, 1)
    qc.h(1)
    qc.cry(theta, 1, 0