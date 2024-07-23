from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister

# https://github.com/Qiskit/qiskit-community-tutorials/blob/master/algorithms/bernstein_vazirani.ipynb


def get_circuit(**kwargs):
    number_of_qubits = kwargs["number_of_qubits"]
    a = kwargs["a"]
    a = a % 2**(number_of_qubits) # a = a mod 2^(number_of_qubits)
    print(a)

    qr = QuantumRegister(number_of_qubits)
    cr = ClassicalRegister(number_of_qubits)

    qc = QuantumCircuit(qr, cr)

    # hadamard gates
    for i in range(number_of_qubits):
        qc.h(qr[i])

    qc.barrier()

    # inner product oracle
    for i in range(number_of_qubits):
        if (a & (1 << i)):  #if bin(a)[i] = 1 then use Z gate
            qc.z(qr[i])
        else:
            qc.iden(qr[i])  # else (=0) use identity

    qc.barrier()

    # hadamard gates
    for i in range(number_of_qubits):
        qc.h(qr[i])

    # measurement
    qc.barrier(qr)
    qc.measure(qr, cr)

    return qc
