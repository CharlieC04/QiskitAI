from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
def simons_algorithm(s: str)->QuantumCircuit:
    """ Write a function that takes the bitstring's' as the input and builds a Quantum Circuit such that the output when xor-ed with the input's' is same as the's'. When building the quantum circuit make sure the classical registers is named 'c'.
    """
    qc = QuantumCircuit(QuantumRegister(len(s)+1), ClassicalRegister(len(s)))
    qc.x(len(s))
    qc.h(len(s))
    for i in range(len(s)):
        if s[i] == '1':
            qc.cx(i, len(s))
    qc.h(len(s))
    for i in range(len(s)):
        qc.cx(i, len(s))
    qc.h(len(s))
    for i in range(len(s)):
        if s[i] == '1':
            qc.cx(i, len(s))
    qc.h(len(s))
    for i in range(len(s)):
        qc.cx(i, len(s))
    qc.h(len(s))
    for i in range(len(s)):
        if s[i] == '1':
            qc.cx(i, len(s))
    qc.h(len(s))
    for i in range(len(s)):
        qc.cx(i, len(s