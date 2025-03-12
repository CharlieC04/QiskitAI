from qiskit.quantum_info.operators import Operator, Pauli
import numpy as np
def compose_op() -> Operator:
    """ Compose XZ with a 3-qubit identity operator using the Operator and the Pauli 'YX' class in Qiskit. Return the operator instance.
    """
    # Create the identity operator on 3 qubits
    I = Operator.from_label('I')
    # Create the Pauli 'YX' operator
    YX = Pauli('YX')
    # Compose the identity operator with the Pauli 'YX' operator
    op = I.compose(YX)
    return op

# Test the function
op = compose_op()
print(op)

# Convert the operator to a matrix
matrix = op.data
print(matrix)

# Convert the operator to a list of Pauli strings
pauli_list = op.to_pauli_list()
print(pauli_list)

# Convert the operator to a list of tuples (pauli, coefficient)
pauli_tuple_list = op.to_pauli_tuple_list()
print(pauli_tuple_list)

# Convert the operator to a list of tuples (qubit, pauli, coefficient)
qubit_pauli_tuple_list = op.to_qubit_pauli_tuple_list()
print(qubit_pauli_tuple_list)

# Convert the operator to a list of tuples