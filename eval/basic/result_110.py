from qiskit import QuantumCircuit
from qiskit.quantum_info import random_clifford, Operator
def equivalent_clifford_circuit(circuit: QuantumCircuit,n: int)->list:
    """ Given a clifford circuit return a list of n random clifford circuits which are equivalent to the given circuit up to a relative and absolute tolerance of 0.4.
    """
    clifford_list = []
    for i in range(n):
        clifford_list.append(random_clifford(n))
    return clifford_list

def equivalent_clifford_operator(circuit: QuantumCircuit,n: int)->list:
    """ Given a clifford circuit return a list of n random clifford operators which are equivalent to the given circuit up to a relative and absolute tolerance of 0.4.
    """
    clifford_list = []
    for i in range(n):
        clifford_list.append(Operator(circuit))
    return clifford_list

def equivalent_clifford_circuit_and_operator(circuit: QuantumCircuit,n: int)->list:
    """ Given a clifford circuit return a list of n random clifford circuits and operators which are equivalent to the given circuit up to a relative and absolute tolerance of 0.4.
    """
    clifford_list = []
    for i in range(n):
        clifford_list.append((random_clifford(n),Operator(circuit)))
    return clifford_list