from qiskit import QuantumCircuit


def create_state_prep(num_qubits):
    """ Return a QuantumCircuit that prepares the state |1> on an n-qubit register.
    """
    qc = QuantumCircuit(num_qubits)
    qc.x(num_qubits - 1)
    return qc


def create_oracle(num_qubits, oracle_function):
    """ Return a QuantumCircuit that implements the oracle function.
    """
    qc = QuantumCircuit(num_qubits)
    for i in range(num_qubits):
        qc.x(i)
    qc.barrier()
    qc.append(oracle_function, range(num_qubits))
    qc.barrier()
    for i in range(num_qubits):
        qc.x(i)
    return qc


def create_diffusion_operator(num_qubits):
    """ Return a QuantumCircuit that implements the diffusion operator.
    """
    qc = QuantumCircuit(num_qubits)
    qc.h(range(num_qubits))
    qc.barrier()
    qc.x(range(num_qubits))
    qc.h(num_qubits - 1)
    qc.mct(range(num_qubits - 1), num_q