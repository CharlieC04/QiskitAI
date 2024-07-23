#By Filipe Chagas
#2022

import qiskit
from math import *

def qft(n: int) -> qiskit.circuit.Gate:
    """Returns a QFT gate for n qubits.

    :param n: Number of target qubits.
    :type n: int
    :return: QFT gate.
    :rtype: qiskit.circuit.Gate
    """
    def rotations(my_circuit: qiskit.circuit.Gate, m: int):
        if m == 0:
            return my_circuit
        else:
            my_circuit.h(m-1) #Add a Haddamard gate to the most significant qubit
        
            for i in range(m-1):
                my_circuit.crz(pi/(2**(m-1-i)), i, m-1)

            rotations(my_circuit, m-1) 
    
    my_circuit = qiskit.QuantumCircuit(n, name='QFT')
    
    rotations(my_circuit, n)

    for m in range(n//2):
        my_circuit.swap(m, n-m-1)

    return my_circuit.to_gate()