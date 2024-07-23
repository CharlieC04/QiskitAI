
### WRITE YOUR CODE BETWEEN THESE LINES - START
    
# import libraries that are used in the function below.
from qiskit import QuantumCircuit
import numpy as np
    
### WRITE YOUR CODE BETWEEN THESE LINES - END

def build_state():
    
    # create a quantum circuit on two qubits
    circuit = QuantumCircuit(2)
    
    qc = QuantumCircuit(2,2) 

    qc.h(0)
    qc.x(1)
    qc.cx(0, 1)
    qc.z(0)
    return qc
    return circuit
