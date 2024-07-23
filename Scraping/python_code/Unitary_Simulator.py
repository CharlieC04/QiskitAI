import matplotlib.pyplot as plt
import numpy as np
from math import pi

from qiskit import QuantumCircuit ,QuantumRegister ,ClassicalRegister, execute
from qiskit.tools.visualization import circuit_drawer
from qiskit.quantum_info import state_fidelity
from qiskit import BasicAer

backend = BasicAer.get_backend('unitary_simulator')

q = QuantumRegister(1)
qc = QuantumCircuit(q)
qc.u3(pi/2 ,pi/2 ,pi/2 ,q)
qc.draw()

job = execute(qc, backend)
job.result().get_unitary(qc, decimals=3)

