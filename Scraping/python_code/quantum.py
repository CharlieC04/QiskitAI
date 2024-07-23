import sys
import numpy as np
from matplotlib import pyplot as plt
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, execute, Aer, visualization
from random import randint


def to_binary(N,n_bit):
    
    Nbin = np.zeros(n_bit, dtype=bool)
    for i in range(1,n_bit+1):
        bit_state = (N % (2**i) != 0)
        if bit_state:
            N -= 2**(i-1)
        
        Nbin[n_bit-i] = bit_state
        
    return Nbin


    
def modular_multiplication(qc,a,N):
    """
    applies the unitary operator that implements 
    modular multiplication function x -> a*x(modN)

    Only works for the particular case x -> 7*x(mod15)!
    """
    for i in range(0,3): 
        qc.x(i)
        
    qc.cx(2,1)
    qc.cx(1,2)
    qc.cx(2,1)
    
    qc.cx(1,0)
    qc.cx(0,1)
    qc.cx(1,0)
    
    qc.cx(3,0)
    qc.cx(0,1)
    qc.cx(1,0)
    
    
def quantum_period(a, N, n_bit):
    # Quantum part
    print("  Searching the period for N =", N, "and a =", a)
    qr = QuantumRegister(n_bit)    
    cr = ClassicalRegister(n_bit)
    qc = QuantumCircuit(qr,cr)
    simulator = Aer.get_backend('qasm_simulator')
        
  
    s0 = randint(1, N-1)            # Chooses random int
    sbin = to_binary(s0,n_bit)      # Turns to binary
    print("\n      Starting at \n      s =", s0, "=", "{0:b}".format(s0), "(bin)")
    
    # Quantum register is initialized with s (in binary)
    for i in range(0,n_bit):        
        if sbin[n_bit-i-1]:
            qc.x(i)
                
    s = s0  
    r=-1    # makes while loop run at least 2 times

    # Applies modular multiplication transformation until we come back to initial number s
    while s != s0 or r <= 0:
        
        r+=1
        # sets up circuit structure
        qc.measure(qr, cr)
        modular_multiplication(qc,a,N)

        qc.draw('mpl')
        # runs circuit and processes data
        job = execute(qc,simulator, shots=10)
        
        result_counts = job.result().get_counts(qc) 
        result_histogram_key = list(result_counts)[0] # https://qiskit.org/documentation/stubs/qiskit.result.Result.get_counts.html#qiskit.result.Result.get_counts

        s = int(result_histogram_key, 2)    
        print("         ", result_counts)
    plt.show()   

    print("\n      Found period r =", r)
    return r
       


if __name__ == '__main__':
    
    a = 7
    N = 15
    n_bit=5
    r = quantum_period(a, N, n_bit)