#!/usr/bin/env python
# coding: utf-8

import numpy as np
from qiskit import *
get_ipython().run_line_magic('matplotlib', 'inline')

num_of_bits = 64
recorded_response = np.zeros(num_of_bits)

for i in range(num_of_bits):
    q = QuantumRegister(1)
    c = ClassicalRegister(1)
    qc = QuantumCircuit(q, c)

    qc.h(q[0])
    qc.measure(q, c)
    
    backend = BasicAer.get_backend('statevector_simulator')
    job_sim = execute(qc, backend, shots=1)
    sim_result = job_sim.result()
    outputstate = sim_result.get_statevector(qc)
    recorded_response[i] = int(outputstate[0].real)
    
print((recorded_response))

res = int("".join(str(int(x)) for x in recorded_response), 2) 
print(res)
