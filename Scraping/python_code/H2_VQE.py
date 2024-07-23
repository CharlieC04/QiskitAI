import os
from qiskit import (QuantumCircuit, 
                    QuantumRegister,
                    ClassicalRegister, 
                    execute,
                    BasicAer)
from scipy.optimize import minimize
import matplotlib.pyplot as plt
from matplotlib.pyplot import plot, draw, show
import numpy as np 

os.environ["QT_QPA_PLATFORM"] = "xcb"

def ansatz_H(theta):
    qc = QuantumCircuit(2,2)
    qc.x(0)
    qc.ry(theta[0],0)
    qc.rx(theta[0]+2*np.pi,1)
    qc.cx(0,1)
    qc.rz(theta[1],0)
    qc.cx(0,1)
    qc.ry(theta[0]+2*np.pi,0)
    qc.rx(theta[0],1)
    return qc

def expectation_H(theta):
    # See DOI: 10.1103/PhysRevX.6.031007
    # Here, we use parameters given for H2 at R=0.75A
    g0 = -0.4804
    g1 = +0.3435
    g2 = -0.4347
    g3 = +0.5716
    g4 = +0.0910
    g5 = +0.0910
    

    energy = g0 
    qc = ansatz_H(theta)
    qc.measure(0,0)
    qc.measure(1,1)
    backend = BasicAer.get_backend('qasm_simulator')
    shots = 1024
    results = execute(qc, backend=backend, shots=shots).result()
    counts = results.get_counts()
    for key in counts.keys():
        if(key[0]=='0'):
            energy += g1*counts[key]/shots
        else:
            energy += -g1*counts[key]/shots
        if(key[1]=='0'):
            energy += g2*counts[key]/shots
        else:
            energy += -g2*counts[key]/shots
        if(key[0]==key[1]):
            energy += g3*counts[key]/shots
        else:
            energy += -g3*counts[key]/shots
    qc = ansatz_H(theta)
    qc.h(0)
    qc.h(1)
    qc.s(0)
    qc.s(1)
    qc.measure(0,0)
    qc.measure(1,1)
    results = execute(qc, backend=backend, shots=shots).result()
    counts = results.get_counts()
    for key in counts.keys():
        if(key[0]==key[1]):
            energy += g4*counts[key]/shots
        else:
            energy += -g4*counts[key]/shots
    qc = ansatz_H(theta)
    qc.h(0)
    qc.h(1)
    qc.measure(0,0)
    qc.measure(1,1)
    results = execute(qc, backend=backend, shots=shots).result()
    counts = results.get_counts()
    for key in counts.keys():
        if(key[0]==key[1]):
            energy += g5*counts[key]/shots
        else:
            energy += -g5*counts[key]/shots
    return energy

nuclear_repulsion = 0.7055696146
theta  = [4*np.pi*np.random.uniform(), 4*np.pi*np.random.uniform()]
result = minimize(expectation_H,theta, method='Nelder-Mead')
theta  = result.x
val    = result.fun


print("VQE: ")
print("  [+] theta1:  {:+2.8} rad, theta2:  {:+2.8} rad".format(theta[0],theta[1]))
print("  [+] energy: {:+2.8} Eh".format(val + nuclear_repulsion))

'''
import numpy as np
from scipy.linalg import block_diag
from scipy.optimize import minimize

np.set_printoptions(precision=4,suppress=True)


# Pauli matrices
I  = np.array([[ 1, 0],
               [ 0, 1]])
Sx = np.array([[ 0, 1],
               [ 1, 0]])
Sy = np.array([[ 0,-1j],
               [1j, 0]])
Sz = np.array([[ 1, 0],
               [ 0,-1]])

# Hadamard matrix
H = (1/np.sqrt(2))*np.array([[ 1, 1],
                             [ 1,-1]])

# Phase matrix
S = np.array([[ 1, 0],
              [ 0,1j]])

# single qubit basis states |0> and |1>
q0 = np.array([[1],
               [0]])
q1 = np.array([[0],
               [1]])

# Projection matrices |0><0| and |1><1|
P0  = np.dot(q0,q0.conj().T)
P1  = np.dot(q1,q1.conj().T)


# Rotation matrices as a function of theta, e.g. Rx(theta), etc.
Rx = lambda theta : np.array([[    np.cos(theta/2),-1j*np.sin(theta/2)],
                              [-1j*np.sin(theta/2),    np.cos(theta/2)]])
Ry = lambda theta : np.array([[    np.cos(theta/2),   -np.sin(theta/2)],
                              [    np.sin(theta/2),    np.cos(theta/2)]])
Rz = lambda theta : np.array([[np.exp(-1j*theta/2),                0.0],
                              [                0.0, np.exp(1j*theta/2)]])

# CNOTij, where i is control qubit and j is target qubit
CNOT10 = np.kron(P0,I) + np.kron(P1,Sx) # control -> q1, target -> q0
CNOT01 = np.kron(I,P0) + np.kron(Sx,P1) # control -> q0, target -> q1

SWAP   = block_diag(1,Sx,1)

# See DOI: 10.1103/PhysRevX.6.031007
# Here, we use parameters given for H2 at R=0.75A
g0 = -0.4804
g1 = +0.3435
g2 = -0.4347
g3 = +0.5716
g4 = +0.0910
g5 = +0.0910

nuclear_repulsion = 0.7055696146

Hmol = (g0 * np.kron( I, I) + # g0 * I
        g1 * np.kron( I,Sz) + # g1 * Z0
        g2 * np.kron(Sz, I) + # g2 * Z1
        g3 * np.kron(Sz,Sz) + # g3 * Z0Z1
        g4 * np.kron(Sy,Sy) + # g4 * Y0Y1
        g5 * np.kron(Sx,Sx))  # g5 * X0X1

electronic_energy = np.linalg.eigvalsh(Hmol)[0] # take the lowest value
print("Classical diagonalization: {:+2.8} Eh".format(electronic_energy + nuclear_repulsion))
print("Exact (from G16):          {:+2.8} Eh".format(-1.1457416808))

# initial basis, put in |01> state with Sx operator on q0
psi0 = np.zeros((4,1))
psi0[0] = 1
psi0 = np.dot(np.kron(I,Sx),psi0)


# read right-to-left (bottom-to-top?)
ansatz = lambda theta: (np.dot(np.dot(np.kron(-Ry(np.pi/2),Rx(np.pi/2)),
                        np.dot(CNOT10, 
                        np.dot(np.kron(I,Rz(theta)),
                               CNOT10))),
                               np.kron(Ry(np.pi/2),-Rx(np.pi/2))))

def projective_expected(theta,ansatz,psi0):
    # this will depend on the hard-coded Hamiltonian + coefficients
    circuit = ansatz(theta[0])
    psi = np.dot(circuit,psi0)
    
    # for 2 qubits, assume we can only take Pauli Sz measurements (Sz \otimes I)
    # we just apply the right unitary for the desired Pauli measurement
    measureZ = lambda U: np.dot(np.conj(U).T,np.dot(np.kron(Sz,I),U))
    
    energy = 0.0
    
    # although the paper indexes the hamiltonian left-to-right (0-to-1) 
    # qubit-1 is always the top qubit for us, so the tensor pdt changes
    # e.g. compare with the "exact Hamiltonian" we explicitly diagonalized
    
    # <I1 I0> 
    energy += g0 # it is a constant

    # <I1 Sz0>
    U = SWAP
    energy += g1*np.dot(psi.conj().T,np.dot(measureZ(U),psi))

    # <Sz1 I0>
    U = np.kron(I,I)
    energy += g2*np.dot(psi.conj().T,np.dot(measureZ(U),psi))

    # <Sz1 Sz0>
    U = CNOT01
    energy += g3*np.dot(psi.conj().T,np.dot(measureZ(U),psi))

    # <Sx1 Sx0>
    U = np.dot(CNOT01,np.kron(H,H))
    energy += g4*np.dot(psi.conj().T,np.dot(measureZ(U),psi))

    # <Sy1 Sy0>
    U = np.dot(CNOT01,np.kron(np.dot(H,S.conj().T),np.dot(H,S.conj().T)))
    energy += g5*np.dot(psi.conj().T,np.dot(measureZ(U),psi))

    return np.real(energy)[0,0]

theta  = [0.0]
result = minimize(projective_expected,theta,args=(ansatz,psi0))
theta  = result.x[0]
val    = result.fun

# check it works...
#assert np.allclose(val + nuclear_repulsion,-1.1456295)

print("VQE: ")
print("  [+] theta:  {:+2.8} deg".format(theta))
print("  [+] energy: {:+2.8} Eh".format(val + nuclear_repulsion))
'''