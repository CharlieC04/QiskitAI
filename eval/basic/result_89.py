from qiskit.circuit.library import HGate
from qiskit import QuantumCircuit, QuantumRegister
def create_controlled_hgate()->QuantumCircuit:
    """ Construct a quantum circuit with a three-qubit controlled-Hadamard gate, using qubit 0 and qubit 1 as the control bits and qubit 2 as the target bit. Return the circuit.
    """
    qr = QuantumRegister(3)
    qc = QuantumCircuit(qr)
    qc.h(qr[2])
    qc.cx(qr[0], qr[2])
    qc.cx(qr[1], qr[2])
    qc.h(qr[2])
    return qc

qc = create_controlled_hgate()
qc.draw()

from qiskit.circuit.library import HGate
from qiskit import QuantumCircuit, QuantumRegister
def create_controlled_hgate()->QuantumCircuit:
    """ Construct a quantum circuit with a three-qubit controlled-Hadamard gate, using qubit 0 and qubit 1 as the control bits and qubit 2 as the target bit. Return the circuit.
    """
    qr = QuantumRegister(3)
    qc = QuantumCircuit(qr)
    qc.h(qr[2])
    qc.cx(qr[0], qr[2])
    qc.cx(qr[1], qr[2])
    qc.h(qr[2])
    return qc

qc = create_controlled_hgate()