from qiskit import QuantumCircuit
def create_unitary_from_matrix():
    """ Write the function that converts the matrix [[0, 0, 0, 1],[0, 0, 1, 0],[1, 0, 0, 0],[0, 1, 0, 0]] into a unitary gate and apply it to a Quantum Circuit. Then return the circuit.
    """
    # Write your code here
    return QuantumCircuit(2)

qc = create_unitary_from_matrix()
qc.draw()