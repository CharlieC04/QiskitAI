'''
This program implements Shor's algorithm which determines 
a number's prime factors. [unfinished]
'''

from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit,\
                    execute, IBMQ, Aer
from qiskit.visualization import circuit_drawer as drawer
from qiskit.tools.visualization import plot_histogram
import numpy as np
from matplotlib.pyplot import plot, draw, show

M = 15
a = 3
e = 8

print("a**2 mod M = ", (a**2)%M)


def NQbitCircuit(p, w, c):
    circuit = QuantumCircuit(w, p, c)

    # prepare initial state 1 in primary register
    circuit.x(p[0])
    circuit.barrier(p)
    circuit.barrier(w)

    # add a Hadamard gate to the working register
    for qubit in w:
        circuit.h(qubit)

    # add additional multiplication by 'a' to the primary register
    circuit.cx(w[0], p[1])
    circuit.cx(w[0], p[3])

    return(circuit)

def NBitQFT(q, c, n):
    circuit = QuantumCircuit(q, c)

    # Start with the most significant bit
    for k in range(n):
        j = n-k
        
        # add Hadamard to qubit j-1
        circuit.h(q[j-1])

        # there is one conditional rotation 
        # for each qubit with lower significance
        for i in reversed(range(j-1)):
            circuit.cp(2*np.pi/2**(j-i), q[i], q[j-1])
    
    # swap qubits
    for i in range(n//2):
        circuit.swap(q[i], q[n-i-1])
    
    return circuit

def Shor_Algorithm(a, n):
    # create registers and circuit
    p = QuantumRegister(4, 'p')
    w = QuantumRegister(n, 'w')
    c = ClassicalRegister(n, "c")
    circuit = QuantumCircuit(w, p, c)

    # add Hadamard gates to working registers
    for qubit in w:
        circuit.h(qubit)
    
    # add multiplication by 'a' to primary register
    
    circuit.cx(w[0], p[1])
    circuit.cx(w[0], p[3])

    # build the QFT part starting with the most significant bit
    for k in range(n):
        j = n - k
        # add Hadamard to qubit j-1
        if(j-1) != 2:
            circuit.h(w[j-1])
        
        # there is one conditional rotation 
        # for each qubit with lower significance
        for i in reversed(range(j-1)):
            circuit.cp(2*np.pi/2**(j-i), w[i], w[j-1])

        
        # add the measurements
        circuit.barrier(w)
        for i in range(len(w)):
            circuit.measure(w[i], c[len(w)-1-i])
        return circuit        
     

p = QuantumRegister(4, 'p')
w = QuantumRegister(3, 'w')
c = ClassicalRegister(len(w), 'c')
qc = NQbitCircuit(p, w, c)

drawer(qc, output='mpl')
draw()
show(block=True)

backend = Aer.get_backend('statevector_simulator')
job = execute(qc, backend)
state = np.around(job.result().get_statevector(), 2)

print('Non-zero states:')
for i in range(2**(len(p)+len(w))):
    if(state[i] != 0):
        print("|",i,"> --->", state[i])

print('Expected amplitudes up to normalisation:')
for s in range(2**(len(w))):
    x = a**s % M
    print("|", x*e + s, "> = |", x, ">|", s, ">")

# // is the floor division
print('Non-zero states and their decomposition: |s> = |s // e> |s mod e> :')
for i in range(2**(len(w)+len(p))):
    if(state[i] != 0):
        # // is the floor division
        print("|", i, "> = |", i // e, ">|", i % e, "> ---> ", state[i])

qc = QuantumCircuit.compose(qc, NBitQFT(w, c,3))
qc.barrier(w)
qc.measure(w, c)
drawer(qc, output='mpl')
draw()
show(block=True)

backend = Aer.get_backend('qasm_simulator')
job = execute(qc, backend)
counts = job.result().get_counts()
plt = plot_histogram(counts)
draw()
show(block=True)

qc = Shor_Algorithm(a,3)
backend = Aer.get_backend('qasm_simulator')
job = execute(qc, backend)
counts = job.result().get_counts()
plt = plot_histogram(counts)
draw()
show(block=True)