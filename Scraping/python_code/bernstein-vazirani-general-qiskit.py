from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister

# https://github.com/Qiskit/qiskit-community-tutorials/blob/master/algorithms/bernstein_vazirani.ipynb
# https://doi.org/10.1073/pnas.1618020114

def get_circuit(**kwargs):
    number_of_qubits = kwargs["number_of_qubits"]
    s = kwargs["s"]
    s = s % 2 ** (number_of_qubits)  # a = a mod 2^(number_of_qubits)
    print(s)

    qr = QuantumRegister(number_of_qubits + 1)
    cr = ClassicalRegister(number_of_qubits)

    qc = QuantumCircuit(qr, cr)

    # hadamard gates
    for i in range(number_of_qubits + 1):
        qc.h(qr[i])
    
    qc.z(qr[number_of_qubits])

    # inner product oracle
    for i in range(number_of_qubits):
        if (s & (1 << i)):  # if bin(s)[i] = 1 then use cnot with ancilla
            qc.cx(qr[i], qr[number_of_qubits])

    # hadamard gates
    for i in range(number_of_qubits):
        qc.h(qr[i])

    # measurement
    for i in range(number_of_qubits):
        qc.measure(qr[i], cr[i])

    return qc
