
### WRITE YOUR CODE BETWEEN THESE LINES - START
    
# import libraries that are used in the function below.
from qiskit import QuantumCircuit
import numpy as np
    
### WRITE YOUR CODE BETWEEN THESE LINES - END

def build_state():
    
    # initialize a 3 qubit circuit
    qc = QuantumCircuit(3)
    qc.h(0)
    qc.cx(0,1)
    qc.cx(1,2)
    return qc
    
    
    ### WRITE YOUR CODE BETWEEN THESE LINES - START
    
    # apply necessary gates
    
    ### WRITE YOUR CODE BETWEEN THESE LINES - END
    return circuit
