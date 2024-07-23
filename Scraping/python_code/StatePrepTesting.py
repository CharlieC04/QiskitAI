from Image_Reader import ImageReader
from DCT_Classic import DCT
import Quantum_Subroutines
import os
import Image_Compression
import cv2
import matplotlib.pyplot as plt
import numpy as np
from qiskit import QuantumCircuit, Aer, transpile
from qiskit_aer.backends.aerbackend import AerBackend
from qiskit.providers.fake_provider import FakeSydneyV2
from qiskit_aer import AerSimulator
from qiskit.quantum_info import random_statevector
import csv
from CustomStatePrep import StatePreparation


qc = QuantumCircuit(4)

state = np.random.randint(-100, 100, size=16)
state = state / np.linalg.norm(state)

state = [
    -0.28672064,
    0.09159132,
    -0.33052518,
    0.29866733,
    -0.39025865,
    -0.21504048,
    -0.09557355,
    0.07566239,
    0.03982231,
    0.23495164,
    0.10353801,
    -0.37432972,
    0.37432972,
    -0.02787562,
    -0.28273841,
    -0.26282725,
]

# state = [1] * 16

# state[0] = -1
# state[1] = 0

# # state[4] = 1
# # state[5] = 1

# # state[9] = 0
# # state[14] = -1

# state[14] = -1
# state[15] = -1

print(np.array(state).reshape(4, 4))

basis = ["cx", "ry", "x", "rz"]

statePrepCircuit = StatePreparation(state, normalize=True)

qc.append(statePrepCircuit, range(0, 4))

print(qc.decompose(reps=3))


sim = Aer.get_backend("aer_simulator")
circ = transpile(qc, sim, basis_gates=basis)
depth = circ.depth()
gates = sum(dict(circ.count_ops()).values())
circ.save_statevector()
result = sim.run(circ).result()
out_vector = result.get_statevector().data

print(out_vector)
