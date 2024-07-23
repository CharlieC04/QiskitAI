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
from qiskit.circuit.library import Isometry, StatePreparation
import csv
import CustomUnitaryDecomp
import scipy

max = 8
blockSize = 4
np.set_printoptions(precision=3, suppress=True)
path = "StateCompression/images/camera.png"
image = ImageReader.getImage(path)

image = cv2.resize(image, (max, max)).astype(int)

basis_gates = ['u1', 'u2', 'u3', 'cx', 'id']
basis_gates = ['u3', 'cx', 'id']

state = image.flatten() / np.linalg.norm(image)
qubits = int(np.log2(max**2))

qc = QuantumCircuit(qubits+1)

numOfBlocks = int((max / blockSize)**2)
indexQubits = int(np.log2(numOfBlocks))

# qc.initialize(state, range(0, qubits))

def recursiveBuildCircuit(state, qc, maxSize, controlQubit, currentQubit, allLeft, indexQubits, allRight):
    if (len(state) == maxSize**2):
        
        statePrep = StatePreparation(state).control(1)
        qubitsForState = int(np.log2(maxSize**2))

        # if (allLeft):
        # qc.mcx(list(range(qubitsForState, qubitsForState + indexQubits)), controlQubit)

        qubits = [controlQubit] + list(range(0, qubitsForState))
        # qc.append(statePrep, qubits)

        # if (allLeft):
        #     qc.mcx(list(range(qubitsForState, qubitsForState + indexQubits)), controlQubit)
        # qc.mcx(list(range(qubitsForState, qubitsForState + indexQubits)), controlQubit)
        
        return qc
    else:
        left = state[:len(state)//2]
        right = state[len(state)//2:]
        leftNorm = np.linalg.norm(left)
        rightNorm = np.linalg.norm(right)

        theta = 2 * np.arccos(rightNorm)
        if (allLeft):
            qc.ry(theta, currentQubit)

        qc = recursiveBuildCircuit(left / leftNorm, qc, maxSize, controlQubit, currentQubit-1, allLeft*True, indexQubits, False)
        # print(left / leftNorm)
        # print(right / rightNorm)
        
        # qc.x(currentQubit)
        # qc.cx(currentQubit, controlQubit)
        # if (currentQubit != 3):
        qc = recursiveBuildCircuit(right / rightNorm, qc, maxSize, controlQubit, currentQubit-1, False, indexQubits, allRight * True)
        
        # qc.x(currentQubit)
        

        return qc
    

# qc = recursiveBuildCircuit(state, qc, blockSize, qubits, qubits-1, True, indexQubits, True)

# print(qc)

norms = []

for i in range(0, numOfBlocks):
    print(state[i*blockSize**2:(i+1)*blockSize**2])
    norms.append(np.linalg.norm(state[i*blockSize**2:(i+1)*blockSize**2]))

print(np.inner(norms, norms))

# qc.initialize(norms, range(qubits-indexQubits, qubits))


# for i in range(0, 1):
#     currState = state[i*blockSize**2:(i+1)*blockSize**2]
#     stateToPrepare = currState / np.linalg.norm(currState)
#     stateCirc = StatePreparation(stateToPrepare).control(1)
#     qc.x(list(range(qubits-indexQubits, qubits)))
#     qc.mcx(list(range(qubits-indexQubits, qubits)), qubits)
#     statePrepQubits = [qubits] + list(range(0, int(np.log2(blockSize**2))))
#     qc.append(stateCirc, statePrepQubits)
    
#     qc.mcx(list(range(qubits-indexQubits, qubits)), qubits)
#     qc.x(list(range(qubits-indexQubits, qubits)))
qc.initialize(state, range(0, qubits))

# half1 = state[:max**2//2]
# half2 = state[max**2//2:]

# half1Norm = np.linalg.norm(half1)
# half2Norm = np.linalg.norm(half2)

# print(half1Norm, half2Norm)

# statePrep1 = StatePreparation(half1/half1Norm).control(1)
# statePrep2 = StatePreparation(half2/half2Norm).control(1)

# q = [qubits-1] + list(range(0, qubits-1))

# theta = 2 * np.arccos(half2Norm)

# qc.ry(theta, qubits-1)

# qc.append(statePrep1, q)
# qc.x(qubits-1)
# qc.append(statePrep2, q)
# qc.x(qubits-1)
# qc.x(qubits-1)

# print(qc)

sim = Aer.get_backend('aer_simulator')
circ = transpile(qc, sim, basis_gates=basis_gates)
depth = circ.depth()
gates = sum(dict(circ.count_ops()).values())
print(depth, gates)

circ.save_statevector()

result = sim.run(circ).result()
out_vector = result.get_statevector().data[0:max*max]

imageData = out_vector.real.reshape((max, max))

print(imageData)
# print(np.linalg.norm(imageData))
# print(state.reshape((max, max)))






