from qiskit import QuantumCircuit
from numpy import pi
def QFT(n: int)->QuantumCircuit:
    """ Design a Quantum Fourier Transform circuit for n qubits using basic Quantum gates.
    """
    qc = QuantumCircuit(n)
    for qubit in range(n):
        for j in range(qubit):
            qc.cp(pi/float(2**(j-qubit)), j, qubit)
        qc.h(qubit)
    return qc

qc = QFT(3)
qc.draw()

from qiskit import QuantumCircuit
from numpy import pi
def QFT(n: int)->QuantumCircuit:
    """ Design a Quantum Fourier Transform circuit for n qubits using basic Quantum gates.
    """
    qc = QuantumCircuit(n)
    for qubit in range(n):
        for j in range(qubit):
            qc.cp(pi/float(2**(j-qubit)), j, qubit)
        qc.h(qubit)
    return qc

qc = QFT(3)
qc.draw()

from qiskit import QuantumCircuit
from numpy import pi
def QFT(n: int)->QuantumCircuit:
    """ Design a Quantum Fourier Transform circuit for n qubits using basic Quantum gates.
    """
    q