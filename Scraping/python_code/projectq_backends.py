# -*- coding: utf-8 -*-

# Copyright 2018, IBM.
#
# This source code is licensed under the Apache License, Version 2.0 found in
# the LICENSE.txt file in the root directory of this source tree.
"""
Example use of the ProjectQ based simulators
"""

import os
from qiskit_addon_projectq import ProjectQProvider
from qiskit import execute, QuantumCircuit, QuantumRegister, ClassicalRegister


def use_projectq_backends():

    ProjectQ = ProjectQProvider()
    qasm_sim = ProjectQ.get_backend('projectq_qasm_simulator')
    sv_sim = ProjectQ.get_backend('projectq_statevector_simulator')

    qr = QuantumRegister(2, 'qr')
    cr = ClassicalRegister(2, 'cr')
    qc = QuantumCircuit(qr, cr)
    qc.h(qr[0])
    qc.cx(qr[0], qr[1])

    # ProjectQ statevector simulator
    result = execute(qc, backend=sv_sim).result()
    print("final quantum amplitude vector: ")
    print(result.get_statevector(qc))

    qc.measure(qr, cr)
   
    # ProjectQ simulator
    result = execute(qc, backend=qasm_sim, shots=100).result()
    print("counts: ")
    print(result.get_counts(qc))
    

if __name__ == "__main__":
    use_projectq_backends()
