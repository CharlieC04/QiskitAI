from qiskit import QuantumCircuit
def create_cz_gate()->QuantumCircuit:
    """ Design a CZ gate using only H and CNOT gates and return the quantum circuit.
    """
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0,1)
    qc.h(0)
    return qc

qc = create_cz_gate()
qc.draw()