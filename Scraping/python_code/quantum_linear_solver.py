'''
This program uses quantum computing to solve a linear system of equations 
'''

import numpy as np
from qiskit import *
from qiskit.tools.visualization import plot_histogram
from matplotlib.pyplot import plot, draw, show

circuit_name = 'solve_linear_system'

backend = Aer.get_backend('qasm_simulator')
qr = QuantumRegister(4, 'q')
cr = ClassicalRegister(4, 'c')
qc = QuantumCircuit(qr, cr, name=circuit_name)

# initilise times that we get the result vector 
# and duration T of the manipulation
n0 = 0
n1 = 0
T = 10
for i in range(T):
    # set the input |b> state
    qc.x(qr[2])

    # set the phase estimation circuit
    qc.h(qr[0])
    qc.h(qr[1])
    qc.p(np.pi, qr[0])
    qc.p(np.pi/2, qr[1])
    qc.cx(qr[1], qr[2])

    # The qunatum inverse Fourier transform
    qc.h(qr[0])
    qc.cp(-np.pi/2, qr[0], qr[1])
    qc.h(qr[1])

    # R (lambda^-1) rotation
    qc.x(qr[1])
    qc.cu3(np.pi/16, 0, 0, qr[0], qr[3])
    qc.cu3(np.pi/8, 0, 0, qr[1], qr[3])
    
    # uncompuation
    qc.x(qr[1])
    qc.h(qr[1])
    qc.cp(np.pi/2, qr[0], qr[1])
    qc.h(qr[0])

    qc.cx(qr[1], qr[2])
    qc.p(-np.pi/2, qr[1])
    qc.p(-np.pi, qr[0])

    qc.h(qr[1])
    qc.h(qr[0])

    # measure the whole quantum register    
    qc.measure(qr, cr)

    job = execute(qc, backend=backend, shots=8192,)
    result = job.result()

    # get the sum of all results
    n0 += result.get_counts(circuit_name)['1000']
    n1 += result.get_counts(circuit_name)['1100']

    #plot_histogram(result.get_counts())
    #draw()
    #show(block=True)
    
    # reset the circuit
    qc.reset(qr)

    # calculate the scale of the elements in result vector and print it
    p = n0/n1
    print('n0 = ', n0, '\t','n1 = ', n1, '\t','p = ', p)