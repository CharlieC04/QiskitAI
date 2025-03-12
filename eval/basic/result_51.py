from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
from qiskit.circuit import Instruction
def quantum_teleportation_circuit(data: [Instruction])->QuantumCircuit:
    """ Write a function to build a quantum teleportation circuit that takes a list of instructions as an argument to transfer the data from the sender to the receiver while taking advantage of dynamic circuits.
    """
    qc = QuantumCircuit(3, 1)
    qc.h(0)
    qc.cx(0, 1)
    qc.barrier()
    qc.append(data, [0, 1])
    qc.barrier()
    qc.cx(1, 2)
    qc.h(1)
    qc.measure(2, 0)
    return qc

qc = quantum_teleportation_circuit([Instruction('cx', [0, 1]), Instruction('cx', [1, 2])])
qc.draw('mpl')

from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
from qiskit.circuit import Instruction
def quantum_teleportation_circuit(data: [Instruction])->QuantumCircuit:
    """ Write a function to build a quantum teleportation circuit that takes a list of instructions as an argument to transfer the data from the sender to the receiver while taking advantage of dynamic circuits.
    """
    qc = QuantumCircuit(3, 1)
    qc.h(0)
    qc.cx(0, 1)
    qc.barrier