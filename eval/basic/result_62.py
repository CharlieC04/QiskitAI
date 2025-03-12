from qiskit import QuantumCircuit
def bb84_senders_circuit(state: [int], basis: [int])->QuantumCircuit:
    """ Construct a BB84 protocol circuit for the sender, inputting both the states and the measured bases.
    """
    circuit = QuantumCircuit(1)
    circuit.h(0)
    circuit.barrier()
    for i in range(len(state)):
        if state[i] == 1:
            circuit.x(0)
        if basis[i] == 1:
            circuit.h(0)
    circuit.barrier()
    return circuit

def bb84_receiver_circuit(basis: [int])->QuantumCircuit:
    """ Construct a BB84 protocol circuit for the receiver, inputting the measured bases.
    """
    circuit = QuantumCircuit(1)
    circuit.barrier()
    for i in range(len(basis)):
        if basis[i] == 1:
            circuit.h(0)
    circuit.barrier()
    return circuit

def bb84_circuit(state: [int], basis: [int])->QuantumCircuit:
    """ Construct a BB84 protocol circuit for both the sender and the receiver, inputting both the states and the measured bases.
    """
    circuit = bb84_senders_circuit(state, basis)
    circuit.append(bb84_receiver_circuit(basis), [0])
    return circuit

state = [0