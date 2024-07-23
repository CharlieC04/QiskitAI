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


N = 256
dct = DCT.normal1D(N)

path = os.path.abspath("StateCompression/images/camera.png")

paths = ["camera",  "peppers", "bird"]
paths = [paths[0]]


# image = ImageReader.chopUpImage(image, N)['pieces'][0]

basis_gates = ['u1', 'u2', 'u3', 'cx', 'id']
basis_gates = ['u3', 'cx', 'id']

rC = 2
cC = 1

comp = [(2, 1), (2, 2), (4, 2), (4, 4), (8, 4), (8, 8), (16, 8), (16, 16)]#, (32, 16), (32, 32)]
comp.reverse()
# comp = [comp[1]]

# comp = [(8, 8)]

# open the file in the write mode
f = open('compression_results_5.csv', 'w')

# create the csv writer
writer = csv.writer(f)

headings = ["image", "compression", "psnr", "depth", "gates", "inner_product"]
writer.writerow(headings)

# write a row to the csv file
for im in paths:
    image = ImageReader.getImage(os.path.abspath("StateCompression/images/" + im + ".png"), N)
    # print(image)

    imageNorm = np.linalg.norm(image)
    normalizedImage = image / imageNorm

    for c in comp:
        # print(c)
        rC = c[0]
        cC = c[1]
        compressedImage = Image_Compression.naiveDCTCompression(image, N, rC, cC)


        norm = np.linalg.norm(compressedImage)
        normData = compressedImage / norm
        remade = DCT.remakeImage(normData, dct)

        inner = np.inner(remade.flatten(), normalizedImage.flatten())
        # print("C:", c, "F:", inner**2)
        nQubits = int(np.log2(N*N))

        aQubits = int(nQubits/2)-1
        # aQubits = 0

        totalQubits = nQubits + aQubits

        qc = QuantumCircuit(totalQubits)

        statePrep = Quantum_Subroutines.buildCompressedState(compressedImage, rC, cC)

        # qc.initialize(normalizedImage.flatten(), range(0, nQubits))

        qc.append(statePrep, range(0, nQubits))


        qdct = Quantum_Subroutines.QDCT(int(nQubits/2), mctMode="v-chain")

        qc.append(qdct.inverse(), list(range(0, int(nQubits/2))) + list(range(nQubits, totalQubits)))
        qc.append(qdct.inverse(), list(range(int(nQubits/2), int(nQubits))) + list(range(nQubits, totalQubits)))
        

        sim = Aer.get_backend('aer_simulator')
        # print("Before")
        circ = transpile(qc, sim, basis_gates=basis_gates)
        # circ = transpile(qc, sim)
        # print("After")
        depth = circ.depth()
        gates = sum(dict(circ.count_ops()).values())
        
        circ.save_statevector()

        result = sim.run(circ).result()
        out_vector = result.get_statevector().data[0:N*N]

        imageData = out_vector.real.reshape((N, N))
        # imageData = imageData


        quantumImage = (imageData * imageNorm)
        # print(quantumImage)
        psnr = cv2.PSNR(image.astype(int), quantumImage.astype(int))

        print("C:", c, "P:", psnr, "D:", depth, "G:", gates, "I:", inner**2)
        # print("C:", c, "D:", depth, "G:", gates)

        # row = [im, c[0] * c[1], psnr, depth, gates, inner**2]

        # # writer.writerow(row)

        # # plt.title("PSNR: " + str(psnr))
        # # plt.imshow(quantumImage, cmap='gray')
        # # plt.show()

# print(image1)
# print(image2)




# ImageReader.displayImage(image1.astype(np.uint8), "PSNR: " + str(int(psnr)))



# ImageReader.displayImage(image2, "Quantum Compressed")






# block = np.array([[144, 99, 94, 90],
#          [148, 99, 94, 90],
#          [148, 99, 94, 90],
#          [148, 99, 94, 90]]).transpose()

# # print(block)

# dct2 = DCT.normal1D(4)

# convert = DCT.convertImage2D(block, dct2).astype(int)
# print(convert)
# convert[0,1] = -12

# convert[1,1] = -15
# convert[2,1] = -4
# convert[3,1] = 4


# print(convert)
# remade = DCT.remakeImage(convert, dct2).astype(int)
# print(remade)
# np.set_printoptions(precision=2)
# np.set_printoptions(suppress=True)
# convert2 = DCT.convertImage2D(remade, dct2)
# convert2[:,2] = 0
# convert2[:,3] = 0

# print(np.linalg.norm(convert2))