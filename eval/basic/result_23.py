from qiskit import QuantumCircuit
def dj_constant_oracle() -> QuantumCircuit:
    """ Create a constant oracle for use in a Deutsch-Jozsa experiment. The oracle takes two input bits (qubits 0 and 1) and writes to one output bit (qubit 2).
    """
    oracle = QuantumCircuit(3)
    oracle.x(2)
    oracle.cz(0, 2)
    oracle.cz(1, 2)
    oracle.x(2)
    return oracle

dj_constant_oracle().draw()