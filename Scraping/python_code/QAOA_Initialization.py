from qiskit import QuantumCircuit
import numpy as np

from qiskit.circuit import Parameter


class QAOAInit:

    circuit = {}

    def __init__(self, numQubits, layers=1, initType='x_high_eigenstate'):
        self.numQubits = numQubits
        self.initType = initType
        self.layers = layers

    def build(self):
        self.circuit = {}

        for l in range(0, self.layers):
            if (self.initType == 'x_low_eigenstate'):
                circuitDetails = self.__buildXLowEigenstate(l)
                self.circuit[l] = circuitDetails
            elif (self.initType == 'x_high_eigenstate'):
                circuitDetails = self.__buildXHighEigenstate(l)
                self.circuit[l] = circuitDetails
            elif (self.initType == 'y_low_eigenstate'):
                circuitDetails = self.__buildYLowEigenstate(l)
                self.circuit[l] = circuitDetails
            elif (self.initType == 'y_high_eigenstate'):
                circuitDetails = self.__buildYHighEigenstate(l)
                self.circuit[l] = circuitDetails
            elif (self.initType == 'z_low_eigenstate'):
                circuitDetails = self.__buildZLowEigenstate(l)
                self.circuit[l] = circuitDetails
            elif (self.initType == 'z_high_eigenstate'):
                circuitDetails = self.__buildZHighEigenstate(l)
                self.circuit[l] = circuitDetails
            elif (self.initType == 'rx_mixer'):
                circuitDetails = self.__buildRXMixer(l)
                self.circuit[l] = circuitDetails
            elif (self.initType == 'ry_mixer'):
                circuitDetails = self.__buildRYMixer(l)
                self.circuit[l] = circuitDetails
            elif (self.initType == "none"):
                circuitDetails = self.__buildNoCircuit()
                self.circuit[l] = circuitDetails

        return True
    
    def getCircuitAtLayer(self, l):
        return self.circuit[l]
    
    def getAllCircuits(self):
        return self.circuit

    
    def __buildXLowEigenstate(self, l):

        qc = QuantumCircuit(self.numQubits)
        qc.x(range(0, self.numQubits))
        qc.h(range(0, self.numQubits))

        return (qc, [])
    
    def __buildXHighEigenstate(self, l):

        qc = QuantumCircuit(self.numQubits)
        qc.h(range(0, self.numQubits))

        return (qc, [])
    
    def __buildYLowEigenstate(self, l):

        qc = QuantumCircuit(self.numQubits)
        qc.h(range(0, self.numQubits))
        qc.sdg(range(0, self.numQubits))
        qc.rz(np.pi, range(0, self.numQubits))

        return (qc, [])
    
    def __buildYHighEigenstate(self, l):

        qc = QuantumCircuit(self.numQubits)
        qc.h(range(0, self.numQubits))
        qc.sdg(range(0, self.numQubits))
        qc.rz(-np.pi, range(0, self.numQubits))
        qc.z(range(0, self.numQubits))

        return (qc, [])
    
    def __buildZLowEigenstate(self, l):

        qc = QuantumCircuit(self.numQubits)
        qc.x(range(0, self.numQubits))

        return (qc, [])
    
    def __buildZHighEigenstate(self, l):

        qc = QuantumCircuit(self.numQubits)

        return (qc, [])
    
    def __buildRXMixer(self, l):
        theta = Parameter('init_cl_' + str(l))

        qc = QuantumCircuit(self.numQubits)
        for qubit in range(0, self.numQubits):
            qc.rx(theta, qubit)

        return (qc, [theta])
    
    def __buildRYMixer(self, l):
        theta = Parameter('init_cl_' + str(l))

        qc = QuantumCircuit(self.numQubits)
        for qubit in range(0, self.numQubits):
            qc.ry(theta, qubit)

        return (qc, [theta])
    
    def __buildNoCircuit(self):

        qc = QuantumCircuit(self.numQubits)

        return (qc, [])

