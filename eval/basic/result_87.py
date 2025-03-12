from qiskit import QuantumCircuit
def quantum_circuit_with_delay():
    """ Create a one-qubit quantum circuit, apply hadamard gate, then add a delay of 100 and then again apply hadamard gate and return the circuit.
    """
    qc = QuantumCircuit(1)
    qc.h(0)
    qc.delay(100)
    qc.h(0)
    return qc
qc = quantum_circuit_with_delay()
qc.draw()
qc.draw('mpl')
qc.draw('latex')
qc.draw('text')
qc.draw('mpl', style='iqx')
qc.draw('latex', style='iqx')
qc.draw('text', style='iqx')
qc.draw('mpl', style='iqx', initial_state=True)
qc.draw('latex', style='iqx', initial_state=True)
qc.draw('text', style='iqx', initial_state=True)
qc.draw('mpl', style='iqx', initial_state=True, output='mpl')
qc.draw('latex', style='iqx', initial_state=True, output='latex')
qc.draw('text', style='iqx', initial_state=True, output='text')
qc.draw('mpl', style='iqx', initial_state=True, output='mpl', reverse