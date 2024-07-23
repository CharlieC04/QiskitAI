from Image_Reader import ImageReader
from DCT_Classic import DCT
import Quantum_Subroutines
import os
import Image_Compression
import cv2
import matplotlib.pyplot as plt
import numpy as np
from qiskit import QuantumCircuit, Aer, transpile
from CustomStatePrep import StatePreparation
from qiskit_aer.backends.aerbackend import AerBackend
from qiskit.providers.fake_provider import FakeSydneyV2
from qiskit_aer import AerSimulator
from qiskit.circuit.library import Isometry
import csv
import CustomUnitaryDecomp
import scipy

max = 256
np.set_printoptions(precision=3, suppress=True)
path = "StateCompression/images/camera.png"
image = ImageReader.getImage(path)

image = cv2.resize(image, (max, max)).astype(int)

basis_gates = ['u1', 'u2', 'u3', 'cx', 'id']
basis_gates = ['u3', 'cx', 'id']

# image = image / np.linalg.norm(image)


maxCompression = 8

for comp in range(maxCompression, -1, -1):
    [U, D, V] = np.linalg.svd(image)

    compression = comp

    n = max // 2**compression

    D = D[:n]

    dNorm = np.linalg.norm(D)

    D = D / dNorm

    D = D.transpose()

    def prepareDState(D, totalQubits):
        qubits = int(np.log2(len(D)))
        qc = QuantumCircuit(totalQubits)
        qc.initialize(D, range(0, qubits))
        for i in range(0, qubits):
            qc.cx(i, totalQubits//2)
        return qc

    # qubits = int(2 * np.log2(max))
    # qc = QuantumCircuit(qubits)

    # if (n != 1):
    #     statePrep = prepareDState(D, qubits)
    #     statePrep.name = "S"
    #     qc.append(statePrep, range(0, qubits))
    

    # print(U.shape)
    # print(V.shape)

    V = V.transpose()

    U = U[:, :n]
    V = V[:, :n]

    # print(U)

    # uIsometry = Isometry(U, num_ancillas_dirty=0, num_ancillas_zero=0)
    # uIsometry.name = "U"
    # vIsometry = Isometry(V, num_ancillas_dirty=0, num_ancillas_zero=0)
    # vIsometry.name = "V"

    # qc.append(vIsometry, range(0, qubits//2))
    # qc.append(uIsometry, range(qubits//2, qubits))

    # # print(qc)

    # sim = Aer.get_backend('aer_simulator')
    # circ = transpile(qc, sim, basis_gates=basis_gates)
    # depth = circ.depth()
    # gates = sum(dict(circ.count_ops()).values())
    # # print(depth, gates)

    # # circ.save_statevector()

    # # result = sim.run(circ, nshots=1).result()
    # # out_vector = result.get_statevector().data

    # # imageData = out_vector.real.reshape((max, max))
    # # # imageData = imageData

    V = V.transpose()

    for i in range(0, len(D)):
        V[i, :] *= D[i]

    classicalCompressed = np.matmul(U, V) * dNorm

    # inner = np.inner(classicalCompressed.flatten(), image.flatten() / np.linalg.norm(image))

    # print(V)
    # print(D)
    # for i in range(0, len(D)):
    #     V[i, :] *= D[i]
    # print(V)
    # print(np.matmul(U, V))

    # print(imageData)

    # quantumImage = (imageData * dNorm)

    # psnr = cv2.PSNR(image.astype(int), classicalCompressed.astype(int))
    # print(comp, gates, depth, psnr)
    # print(comp, inner**2)

    plt.imsave("svd_cameraX" + str(comp) + ".png", classicalCompressed, cmap='gray')
    # plt.show()
