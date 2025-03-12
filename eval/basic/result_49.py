from qiskit import QuantumCircuit
def simple_elitzur_vaidman()->QuantumCircuit:
    """ Return a simple Elitzur Vaidman bomb tester circuit.
    """
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure_all()
    return qc

simple_elitzur_vaidman()