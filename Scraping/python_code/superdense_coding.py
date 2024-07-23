import qiskit

from .common_gates import *

import random

def superdense_coding_circuit(msg):
    qc = qiskit.QuantumCircuit(2)

    phi_plus = phi_plus_gate()
    qc.append(phi_plus, [0, 1])

    qc.barrier() 

    if msg[1] == '1':
        qc.z(0)

    if msg[0] == '1':
        qc.x(0)

    qc.barrier()

    qc.append(phi_plus.inverse(), [0, 1])
    qc.name = "SC"
    return qc

def superdense_coding_example():
    msg = random.choice(["00", "01", "10", "11"])

    qc = qiskit.QuantumCircuit(2, 2)

    sc_qc = superdense_coding_circuit(msg)

    qc.append(sc_qc, [0, 1])

    if msg[0] == '1':
        qc.x(1)

    if msg[1] == '1':
        qc.x(0)

    qc.measure([0, 1], [0, 1])
    print(msg)
    print(qc.draw(output="text"))

    return qc
