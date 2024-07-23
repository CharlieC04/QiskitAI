from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, execute, BasicAer

from qiskit.visualization import plot_histogram


def multi_toffoli_q(qc, q_controls, q_target, q_ancillas=None):
    """
    N = number of qubits
    controls = control qubits
    target = target qubit
    ancillas = ancilla qubits, len(ancillas) = len(controls) - 2
    """
    # q_controls = register_to_list(q_controls)
    # q_ancillas = register_to_list(q_ancillas)
    if len(q_controls) == 1:
        qc.cx(q_controls[0], q_target)
    elif len(q_controls) == 2:
        qc.ccx(q_controls[0], q_controls[1], q_target)
    elif len(q_controls) > 2 and (q_ancillas is None or len(q_ancillas) < len(q_controls) - 2):
        raise Exception('ERROR: need more ancillas for multi_toffoli!')
    else:
        multi_toffoli_q(qc, q_controls[:-1], q_ancillas[-1], q_ancillas[:-1])
        qc.ccx(q_controls[-1], q_ancillas[-1], q_target)
        multi_toffoli_q(qc, q_controls[:-1], q_ancillas[-1], q_ancillas[:-1])

n = 7
q1 = QuantumRegister(n)
q2 = QuantumRegister(n)
q3 = QuantumRegister(1)
q4 = QuantumRegister(n)
cr = ClassicalRegister(n)

def m_gate_for_special_case(q1,q2,q4, hamiltonian):
    circuit = QuantumCircuit(qr, cr)

def gate_aza(q1,q2,q3,q4):
    #circuit = QuantumCircuit(q1,q2,q3,q4)
    matrix = [[1, 0, 0, 0], [0, 1/math.sqrt(2), 1/math.sqrt(2), 0], [0, 1/math.sqrt(2), -1/math.sqrt(2), 0], [0,0,0,1]]
    for i in range(n):
        circuit.unitary(matrix,[q1[i],q2[i]])
    circuit.barrier()
    for i in range(n):
        circuit.x(q2[i])
        circuit.ccx(q1[i],q2[i],q3)
        circuit.x(q2[i])
    circuit.barrier()
    #hogehoge
    circuit.x(q3)
    for i in range(n):
        circuit.cu1(-2**i, q3, q4[i])
    circuit.x(q3)
    for i in range(n):
        circuit.cu1(2**i, q3, q4[i])
    circuit.barrier()
    for i in range(n):
        circuit.x(q2[i])
        circuit.ccx(q1[i],q2[i],q3)
        circuit.x(q2[i])
    circuit.barrier()
    for i in range(n):
        circuit.unitary(matrix,[q1[i],q2[i]])
