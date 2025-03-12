from qiskit.quantum_info import anti_commutator, SparsePauliOp
from qiskit.quantum_info import random_pauli
import numpy as np
def anticommutators(pauli: SparsePauliOp):
    """ Return a list of ten anticommutators for the given pauli.
    """
    anticommutators = []
    for i in range(10):
        anticommutators.append(anti_commutator(pauli, pauli))
    return anticommutators

pauli = random_pauli(2)
anticommutators(pauli)

pauli = SparsePauliOp.from_list([('II', 1), ('IZ', 1), ('ZI', 1), ('ZZ', 1)])
anticommutators(pauli)

pauli = SparsePauliOp.from_list([('II', 1), ('IZ', 1), ('ZI', 1), ('ZZ', 1)])
anticommutators(pauli)

pauli = SparsePauliOp.from_list([('II', 1), ('IZ', 1), ('ZI', 1), ('ZZ', 1)])
anticommutators(pauli)

pauli = SparsePauliOp.from_list([('II', 1), ('IZ', 1), ('ZI', 1), ('ZZ', 1)])
anticommutators(pauli)

pauli =