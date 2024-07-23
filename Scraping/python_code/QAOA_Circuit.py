from qiskit import QuantumCircuit
from QAOA_Mixer import Mixer
from QAOA_Cost_Hamiltonian import CostHamiltonian
from QAOA_Initialization  import QAOAInit
from Helper_Functions import groverDiffuser

class QAOACircuit:
    circuit = None
    parameters = []

    def __init__(self, numQubits, layers=1, mixerType='classic', problem='maxcut', problemType=None, initType='x_high_eigenstate'):
        self.numQubits = numQubits
        self.problem = problem
        self.problemType = problemType
        self.initType = initType
        self.mixerType = mixerType
        self.layers = layers

    def build(self):
        self.circuit = None
        self.parameters = []
        qc = QuantumCircuit(self.numQubits)
        parameters = []

        init = QAOAInit(self.numQubits, 1, self.initType)
        init.build()

        mixer = Mixer(self.numQubits, self.layers, self.mixerType)
        mixer.build()

        problem = CostHamiltonian(self.numQubits, self.layers, self.problemType, self.problem)
        problem.build()


        (initCirc, initParams) = init.getCircuitAtLayer(0)
        qc.append(initCirc, list(range(0, self.numQubits)))
        parameters += initParams

        for l in range(0, self.layers):

            (problemCirc, problemParams) = problem.getCircuitAtLayer(l)
            qc.append(problemCirc, list(range(0, self.numQubits)))
            parameters += problemParams

            (mixerCirc, mixerParams) = mixer.getCircuitAtLayer(l)
            qc.append(mixerCirc, list(range(0, self.numQubits)))
            parameters += mixerParams


            

            

        # diff = groverDiffuser(self.numQubits)

        # qc.append(diff, list(range(0, self.numQubits)))

        # qc.h(range(0, self.numQubits))

        qc.measure_all()

        self.circuit = qc
        self.parameters = parameters

    def getCircuitWithParameters(self, parameterValues):
        qc = self.circuit
        parameters = self.parameters

        parameterMap = {}
        for i in range(0, len(parameters)):
            parameterMap[parameters[i]] = parameterValues[i]

        return qc.assign_parameters(parameterMap)
    
    def getNumberOfParameters(self):
        return len(self.parameters)
