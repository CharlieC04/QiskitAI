from qiskit.quantum_info.operators import Operator, Pauli
def combine_op() -> Operator:
    """ Combine the following three operators XX YY ZZ as: 0.5 * (XX + YY - 3 * ZZ).
    """
    return 0.5 * (Operator(Pauli("XX")) + Operator(Pauli("YY")) - 3 * Operator(Pauli("ZZ")))
combine_op()
