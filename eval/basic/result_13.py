from qiskit import QuantumCircuit
import numpy as np
def custom_rotation_gate() -> QuantumCircuit:
    """ Create a quantum circuit that carries out a custom single-qubit rotation gate (U gate) with angles theta, phi and lambda all equal to pi/2.
    """
    qc = QuantumCircuit(1)
    qc.rx(np.pi/2, 0)
    qc.rz(np.pi/2, 0)
    qc.ry(np.pi/2, 0)
    return qc

qc = custom_rotation_gate()
qc.draw()

from qiskit import QuantumCircuit
import numpy as np
def custom_rotation_gate() -> QuantumCircuit:
    """ Create a quantum circuit that carries out a custom single-qubit rotation gate (U gate) with angles theta, phi and lambda all equal to pi/2.
    """
    qc = QuantumCircuit(1)
    qc.rx(np.pi/2, 0)
    qc.rz(np.pi/2, 0)
    qc.ry(np.pi/2, 0)
    return qc

qc = custom_rotation_gate()
qc.draw()

from qiskit import QuantumCircuit
import numpy as np
def custom_rotation_gate() -> QuantumCircuit:
    """ Create a quantum circuit that carries