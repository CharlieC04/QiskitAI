from qiskit import *

def oracle(n, target_binary):
    """Creates an oracle based on the implementation here: https://github.com/SaashaJoshi/grovers-algorithm"""
    circuit = QuantumCircuit(n + 1)

    for index, value in reversed(list(enumerate(target_binary))):
        if value == '0':
            circuit.x(n-1-index)

    cbits = []
    for i in range(n):
        cbits.append(i)

    circuit.mct(cbits, n, n)

    for index, value in enumerate(target_binary):
        if value == '0':
            circuit.x(n-1-index)

    gate = circuit.to_gate()
    gate.name = 'Oracle'
    return gate