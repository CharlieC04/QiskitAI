from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import Sampler
def or_gate(a: int, b: int)->dict:
    """ Given two 3-bit integers a and b, design a quantum circuit that acts as a classical OR gate. Simulate the circuit using Qiskit Sampler with the Aer simulator as backend and return the counts of the result.
    """
    qc = QuantumCircuit(3)
    qc.x(2)
    qc.ccx(0, 1, 2)
    qc.x(2)
    qc.measure_all()
    backend = AerSimulator()
    sampler = Sampler()
    counts = sampler.run(qc, backend).result().get_counts()
    return counts
or_gate(1, 1)
or_gate(0, 1)
or_gate(1, 0)
or_gate(0, 0)

def and_gate(a: int, b: int)->dict:
    """ Given two 3-bit integers a and b, design a quantum circuit that acts as a classical AND gate. Simulate the circuit using Qiskit Sampler with the Aer simulator as backend and return the counts of the result.
    """
    qc = QuantumCircuit(3)
    qc.x(1)
    qc.ccx(0, 1, 2)
    qc.x(1)
    qc.measure_all()
    backend = AerSimulator()
    sampler = Sampler()
    counts = sampler.