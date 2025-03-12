from qiskit.circuit import QuantumCircuit, Parameter
def rx_gate(value=None):
    """ Return a 1-qubit QuantumCircuit with a parametrized Rx gate and parameter "theta". If value is not None, return the circuit with value assigned to theta.
    """
    qc = QuantumCircuit(1)
    theta = Parameter('theta')
    qc.rx(theta, 0)
    if value is not None:
        qc.assign_parameters({theta: value}, inplace=True)
    return qc

qc = rx_gate(value=np.pi/2)
qc.draw()

qc = rx_gate()
qc.draw()

qc = rx_gate(value=np.pi/2)
qc.draw()

qc = rx_gate(value=np.pi/2)
qc.assign_parameters({theta: np.pi/4}, inplace=True)
qc.draw()

qc = rx_gate(value=np.pi/2)
qc.assign_parameters({theta: np.pi/4}, inplace=True)
qc.measure_all()
qc.draw()

qc = rx_gate(value=np.pi/2)
qc.assign_parameters({theta: np.pi/4}, inplace=True)
qc.measure_all()
qc.draw(output='mpl')

qc = rx_gate(