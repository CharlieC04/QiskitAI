from qiskit import QuantumCircuit
from qiskit.circuit.library import QFT
import numpy as np
from CustomStatePrep import StatePreparation
from qiskit.circuit.library import Isometry

def QDCT(n, mctMode="v-chain"):

    if mctMode == "v-chain":
        ancillaQubits = list(range(n+1, 2*n-1))
        qubits = 2*n-1
    elif mctMode == "noancilla":
        ancillaQubits = []
        qubits = n+2
    elif mctMode == "recursion":
        ancillaQubits = [n+1]
        qubits = n+2
    
    qc = QuantumCircuit(qubits)

    for i in range(n, 0, -1):
        qc.swap(i, i-1)

    qc.x(0)
    qc.h(n+1)
    
    for i in range(0, n):
        qc.cx(n+1, n-i)

    
    

    qft = QFT(n+2, inverse=False, do_swaps=True)

    # for i in range(0, int(n/2)+1):
    #     qc.swap(i, n+1-i)

    qc.append(qft, range(0, n+2))

    qc.barrier()

    qc.z(n+1)
    qc.h(n+1)

    for i in range(0, n):
        qc.cx(n, i)

    qc.barrier()

    for i in range(n-1, 0, -1):
        qc.mct(list(range(0, i)) + [n], i, ancilla_qubits=ancillaQubits, mode=mctMode)

    qc.cx(n, 0)

    qc.z(n)
    qc.h(n)

    for i in range(0, n):
        qc.x(i)

    qc.ry(np.pi/4, n)
    qc.mct(list(range(0, n)), n, ancilla_qubits=ancillaQubits, mode=mctMode)
    qc.ry(-np.pi/4, n)

    for i in range(0, n):
        qc.x(i)

    qc.name = "QDCT"

    return qc


def permutationCircuit(mat, N, M, N_c, M_c):
    num_qubits = int(np.log2(N*M))
    num_qubits_c = int(np.log2(N_c*M_c))
    qc = QuantumCircuit(num_qubits)
    
    n = int(np.log2(N))
    m = int(np.log2(M))
    n_c = int(np.log2(N_c))
    m_c = int(np.log2(M_c))
    
    f = mat.flatten()
    f_c = f
    # qubit_list = list(range(0, m_c)) + list(range(m, m+n_c))
    # qubit_list = list(range(0, m_c+n_c))
    qc2 = QuantumCircuit(num_qubits_c)
    statePrep = Isometry(f_c, num_ancillas_zero=0, num_ancillas_dirty=0)
    qc.append(statePrep, range(0, num_qubits_c))
    # qc.initialize(f_c, range(0, num_qubits_c))
    # print(qc2.decompose(reps=2))
    for i in range(n_c-1, -1, -1):
        if (m_c != m):
            qc.swap(m + i, m_c + i)
        
    qc.name = "PERM" 
     
    return qc

def buildCompressedState(comp, rC, cC):
    normalCompState = comp / np.linalg.norm(comp)

    
    r = int(comp.shape[0] / rC)
    c = int(comp.shape[1] / cC)
    state = normalCompState[:r, :c]

    qubits = int(np.log2(comp.size))
    qc = QuantumCircuit(qubits)
    permCirc = permutationCircuit(state, comp.shape[0], comp.shape[1], r, c)
    qc.append(permCirc, range(0, qubits))

    qc.name = "C_S_P"

    return qc







