from qiskit import QuantumRegister, ClassicalRegister
from qiskit import QuantumCircuit, execute
from qiskit import Aer
import numpy as np
import sys

N=int(sys.argv[1])
filename = sys.argv[2]
backend = Aer.get_backend('unitary_simulator')

def GHZ(n):
    if n<=0:
        return None
    circ = QuantumCircuit(n)
    # Put your code below
    # ----------------------------
 
    circ.h(0)
    for x in range(1,n):
        circ.cx(x-1,x)

   
    # ----------------------------
    return circ

circuit = GHZ(N)
job = execute(circuit, backend, shots=8192)
result = job.result()
array = result.get_unitary(circuit,3)
np.savetxt(filename, array, delimiter=",", fmt = "%0.3f")

