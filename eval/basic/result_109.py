from qiskit.circuit import QuantumCircuit, Parameter
def circuit()-> QuantumCircuit:
    """ Create a parameterized quantum circuit using minimum resources whose statevector output cover the equatorial plane of the surface of the bloch sphere.
    """
    qc = QuantumCircuit(1)
    qc.ry(Parameter('theta'), 0)
    return qc

qc = circuit()
qc.draw()

from qiskit.visualization import plot_bloch_multivector

theta = Parameter('θ')
qc = QuantumCircuit(1)
qc.ry(theta, 0)
plot_bloch_multivector(qc)

theta = Parameter('θ')
qc = QuantumCircuit(1)
qc.ry(theta, 0)
plot_bloch_multivector(qc, title="Bloch Sphere")

theta = Parameter('θ')
qc = QuantumCircuit(1)
qc.ry(theta, 0)
plot_bloch_multivector(qc, title="Bloch Sphere", show_state_labels=True)

theta = Parameter('θ')
qc = QuantumCircuit(1)
qc.ry(theta, 0)
plot_bloch_multivector(qc, title="Bloch Sphere", show_state_labels=True, show_state_populations=True