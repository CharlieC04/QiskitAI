from qiskit import QuantumCircuit
from qiskit.circuit import Parameter

class Mixer:

    circuit = {}

    def __init__(self, numQubits, layers=1, mixerType='classic'):
        self.numQubits = numQubits
        self.mixerType = mixerType
        self.layers = layers

    def build(self):
        self.circuit = {}

        for l in range(0, self.layers):
            if (self.mixerType == 'rx_mixer'):
                circuitDetails = self.__buildClassic(l)
                self.circuit[l] = circuitDetails
            elif (self.mixerType == "ma_rx_mixer"):
                circuitDetails = self.__buildMAClassic(l)
                self.circuit[l] = circuitDetails
            elif (self.mixerType == "ry_mixer"):
                circuitDetails = self.__buildRYMixer(l)
                self.circuit[l] = circuitDetails
            elif (self.mixerType == "ma_ry_mixer"):
                circuitDetails = self.__buildMARYMixer(l)
                self.circuit[l] = circuitDetails
            elif (self.mixerType == "rz_mixer"):
                circuitDetails = self.__buildRZMixer(l)
                self.circuit[l] = circuitDetails
            elif (self.mixerType == "ma_rz_mixer"):
                circuitDetails = self.__buildMARZMixer(l)
                self.circuit[l] = circuitDetails
            elif (self.mixerType == "none"):
                circuitDetails = self.__buildNoCircuit()
                self.circuit[l] = circuitDetails

        return True
    
    def getCircuitAtLayer(self, l):
        return self.circuit[l]
    
    def getAllCircuits(self):
        return self.circuit

    
    def __buildClassic(self, l):
        theta = Parameter('mix_cl_' + str(l))

        qc = QuantumCircuit(self.numQubits)
        for qubit in range(0, self.numQubits):
            qc.rx(theta, qubit)

        return (qc, [theta])
    
    def __buildMAClassic(self, l):
        theta = [Parameter('mix_cl_' + str(l) + "_" + str(i)) for i in range(0, self.numQubits)]

        qc = QuantumCircuit(self.numQubits)
        for qubit in range(0, self.numQubits):
            qc.rx(theta[qubit], qubit)

        return (qc, theta)
    
    def __buildRYMixer(self, l):
        theta = Parameter('mix_cl_' + str(l))

        qc = QuantumCircuit(self.numQubits)
        for qubit in range(0, self.numQubits):
            qc.ry(theta, qubit)

        return (qc, [theta])
    
    def __buildMARYMixer(self, l):
        theta = [Parameter('mix_cl_' + str(l) + "_" + str(i)) for i in range(0, self.numQubits)]

        qc = QuantumCircuit(self.numQubits)
        for qubit in range(0, self.numQubits):
            qc.ry(theta[qubit], qubit)

        return (qc, theta)
    
    def __buildRZMixer(self, l):
        theta = Parameter('mix_cl_' + str(l))

        qc = QuantumCircuit(self.numQubits)
        for qubit in range(0, self.numQubits):
            qc.rz(theta, qubit)

        return (qc, [theta])
    
    def __buildMARZMixer(self, l):
        theta = [Parameter('mix_cl_' + str(l) + "_" + str(i)) for i in range(0, self.numQubits)]

        qc = QuantumCircuit(self.numQubits)
        for qubit in range(0, self.numQubits):
            qc.rz(theta[qubit], qubit)

        return (qc, theta)
    
    def __buildNoCircuit(self):

        qc = QuantumCircuit(self.numQubits)

        return (qc, [])


    