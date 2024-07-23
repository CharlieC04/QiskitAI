
# Do the necessary imports
import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit import Aer
from qiskit.extensions import Initialize

from qiskit.quantum_info import random_statevector, Statevector,partial_trace

def trace01(out_vector):
    return Statevector([sum([out_vector[i] for i in range(0,4)]), sum([out_vector[i] for i in range(4,8)])])

def teleportation():
    # Create random 1-qubit state
    psi = random_statevector(2)
    print(psi)

    init_gate = Initialize(psi)
    init_gate.label = "init"

    ## SETUP
    qr = QuantumRegister(3, name="q")   # Protocol uses 3 qubits
    crz = ClassicalRegister(1, name="crz") # and 2 classical registers
    crx = ClassicalRegister(1, name="crx")
    qc = QuantumCircuit(qr, crz, crx)

    # Don't modify the code above
    ## Put your code below
    # ----------------------------

    qc.initialize(psi, qr[0])
    
    qc.h(qr[1])
    qc.cx(qr[1],qr[2])

    qc.cx(qr[0],qr[1])
    qc.h(qr[0])

    qc.measure(qr[0],crz[0])
    qc.measure(qr[1],crx[0])

   

    qc.x(qr[2]).c_if(crx[0], 1)
    qc.z(qr[2]).c_if(crz[0], 1)




    # ----------------------------
    # Don't modify the code below

    sim = Aer.get_backend('aer_simulator')
    qc.save_statevector()
    out_vector = sim.run(qc).result().get_statevector()
    result = trace01(out_vector)
    return psi, result
# (psi,res) = teleportation()

# print(psi)
# print(res)
# if psi == res:
#     print('1')
# else:
#     print('0')