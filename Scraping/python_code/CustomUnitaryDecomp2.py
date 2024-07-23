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
import csv
import CustomUnitaryDecomp


np.set_printoptions(precision=3, suppress=True)
max = 16
path = "StateCompression/images/camera.png"
image = ImageReader.getImage(path)
image = cv2.resize(image, (max, max))

basis_gates = ['u1', 'u2', 'u3', 'cx', 'id']
basis_gates = ['u3', 'cx', 'id']

[U, D, V] = np.linalg.svd(image)



U[max-1, 0] *= -1

print(U)

thetas = []

for i in range(0, max-1):
    val = U[i, 0]
    print(val)
    for theta in thetas:
        val /= np.sin(theta)
    print(val)
    print()
    thetas.append(np.arccos(val))


# print(thetas)

# print(np.cos(thetas[0]))
print("")

for i in range(0, max-1):
    val = np.cos(thetas[i])
    for j in range(i-1, -1, -1):
        # print(j)
        val *= np.sin(thetas[j])

    print(val)

val = 1

for i in range(0, max-1):
    val *= np.sin(thetas[i])


print(val)
