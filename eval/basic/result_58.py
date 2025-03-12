from qiskit import QuantumCircuit
from numpy import pi
def create_ch_gate()->QuantumCircuit:
    """ Design a CH gate using CX and RY gates.
    """
    qc = QuantumCircuit(2)
    qc.cx(0,1)
    qc.ry(pi/2,1)
    qc.cx(0,1)
    return qc

qc = create_ch_gate()
qc.draw()

from qiskit import QuantumCircuit
from numpy import pi
def create_ch_gate()->QuantumCircuit:
    """ Design a CH gate using CX and RY gates.
    """
    qc = QuantumCircuit(2)
    qc.ry(pi/2,1)
    qc.cx(0,1)
    qc.ry(-pi/2,1)
    return qc

qc = create_ch_gate()
qc.draw()

from qiskit import QuantumCircuit
from numpy import pi
def create_ch_gate()->QuantumCircuit:
    """ Design a CH gate using CX and RY gates.
    """
    qc = QuantumCircuit(2)
    qc.ry(pi/2,1)
    qc.cx(0,1)
    qc.ry(pi/2,1)
    return qc