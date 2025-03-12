from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
def send_bits(bitstring: str)->QuantumCircuit:
    """ Provide a quantum circuit that enables the transmission of two classical bits from the sender to the receiver through a single qubit of quantum communication, given that the sender and receiver have access to entangled qubits.
    """
    qc = QuantumCircuit(1, 1)
    qc.x(0)
    qc.h(0)
    qc.measure(0, 0)
    return qc

send_bits('10')

send_bits('01')

send_bits('11')

send_bits('00')

send_bits('10')

send_bits('01')

send_bits('11')

send_bits('00')

send_bits('10')

send_bits('01')

send_bits('11')

send_bits('00')

send_bits('10')

send_bits('01')

send_bits('11')

send_bits('00')

send_bits('10')

send_bits('01')

send_bits('11')

send_bits('00')

send_bits('10')

send_bits('01')

send_bits('11')

send_bits