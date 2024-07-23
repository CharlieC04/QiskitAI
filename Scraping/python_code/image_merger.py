from PIL import Image
from numpy import*
import matplotlib.cm as cm
import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.append("../../qiskit-sdk-py/")
import math
from qiskit import (
    QuantumCircuit,
    execute, QuantumRegister, ClassicalRegister, Aer)
from qiskit import IBMQ

# Loading your IBM Q account(s)
provider = IBMQ.load_account()

def pixelate(first_file, second_file, size):
    im1 = Image.open(first_file)
    im2 = Image.open(second_file)

    im1 = im1.resize((size, size), Image.BILINEAR)
    im2 = im2.resize((size, size), Image.BILINEAR)

    A1 = (im1)
    A2 = (im2)

    return A1, A2

# Run the quantum script

def run_quantum(file1, file2):
    file_1 = file1
    file_2 = file2
    size = 16
    A1, A2 = pixelate(file_1, file_2, size)
    plt.imsave('filename2.jpeg',A2, cmap=cm.gray)

    img = np.asarray(A1)
    new_img = img.reshape(32, 32)
    # new_img = img.reshape((img.shape[0]*img.shape[1]), img.shape[2])
    new_img = new_img.transpose()

    print(len(new_img[0]))

    img1 = np.asarray(A2)
    new_img1 = img1.reshape(32, 32)
    # new_img1 = img1.reshape((img1.shape[0]*img1.shape[1]), img1.shape[2])
    new_img1 = new_img1.transpose()

    print(len(new_img1))

    # set up registers and program
    qr = QuantumRegister(15, 'qr')
    cr = ClassicalRegister(15,'cr')
    qc = QuantumCircuit(qr, cr)

    # rightmost eight (qu)bits have ')' = 00101001
    double = np.zeros((16,16)) # final double array

    print("Quantum Circuit Complete. Determining Pixel Values...")

    for p in range(16):
        for k in range(16):
            num_1 = bin(new_img[p][k])
            num_2 = bin(new_img1[p][k])

            for i in range(len(str(num_1))):
                if num_1[i] == str(1):
                    qc.x(qr[i])

            qc.h(qr[7]) # create superposition on 9
            qc.cx(qr[7],qr[8]) # spread it to 8 with a cnot

            for i in range(len(str(num_2))):
                        if num_2[i] == str(1):
                            qc.x(qr[i+5])

            for j in range(15):
                qc.measure(qr[j], cr[j])

            simulator = Aer.get_backend('qasm_simulator')
            job = execute(qc, simulator, shots=1)
            results = job.result()
            stats = results.get_counts(qc)
            register_value = stats.keys()

            for x in register_value:
                split = x[0:7]
                split2 = x[7:15]
                total = abs(int(split,2)-int(split2,2))
                double[p][k] = total

    # img = plt.imshow(double) # final image
    plt.imsave('result.jpeg',double)


