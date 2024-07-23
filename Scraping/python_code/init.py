from qiskit import *

def init(qc, n):
    """Prepares qubits for algorithm"""
    qc.x(n)
    qc.barrier()
    qc.h(range(n+1))
    qc.barrier()
    