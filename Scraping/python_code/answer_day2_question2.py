
### WRITE YOUR CODE BETWEEN THESE LINES - START
    
# import libraries that are used in the function below.
from qiskit import QuantumCircuit
import numpy as np
from math import sqrt, pi
    
### WRITE YOUR CODE BETWEEN THESE LINES - END

def build_state():
    
   
    circuit = QuantumCircuit(1)
    initial_state = [0,1]
    circuit.initialize(initial_state, 0)
    
    
    
    circuit.ry(pi/3,0)
     
    
    ### WRITE YOUR CODE BETWEEN THESE LINES - END
    return circuit
