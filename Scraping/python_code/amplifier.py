from qiskit import *
from math import pi

def amplifier(n):
    """Creates a general diffuser using V and V-Dagger gates"""
    circuit = QuantumCircuit(n)

    circuit.x(range(n))

    #V
    circuit.cu1(pi/4, 0, 3)

    #V-dagger
    circuit.cx(0, 1)
    circuit.cu1(-pi/4, 1, 3)
    circuit.cx(0, 1)

    # V
    circuit.cu1(pi/4, 1, 3)

    #V-dagger
    circuit.cx(1, 2)
    circuit.cu1(-pi/4, 2, 3)

    # V
    circuit.cx(0, 2)
    circuit.cu1(pi/4, 2, 3)

    #V-dagger
    circuit.cx(1, 2)
    circuit.cu1(-pi/4, 2, 3)

    # V
    circuit.cx(0, 2)
    circuit.cu1(pi/4, 2, 3)

    circuit.x(range(n))

    amplification = circuit.to_gate()
    amplification.name = 'Amplification'

    return amplification