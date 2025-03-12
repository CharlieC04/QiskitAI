from qiskit.circuit import QuantumCircuit, Parameter
def circuit():
    """ Return an ansatz to create a quantum dataset of pure states distributed equally across the bloch sphere. Use minimum number of gates in the ansatz.
    """
    # YOUR CODE HERE
    qc = QuantumCircuit(1)
    qc.ry(Parameter('theta'), 0)
    return qc

qc = circuit()
qc.draw()