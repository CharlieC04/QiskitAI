import matplotlib.pyplot as plt
import networkx as nx
import qiskit
import HERR
from qiskit.transpiler import CouplingMap
from qiskit.transpiler.passes.routing import BasicSwap
from qiskit import QuantumCircuit, execute, Aer, IBMQ
from qiskit.dagcircuit import DAGCircuit
from qiskit.converters import circuit_to_dag
from qiskit.converters import dag_to_circuit
from math import pi
from qiskit.compiler import transpile, assemble
from qiskit.providers.aer.noise import NoiseModel
import qiskit.providers.aer.noise as noise
from qiskit.tools.visualization import dag_drawer
import random
from qiskit.circuit.instruction import Instruction
from qiskit.transpiler.passes.routing import *
import time


def countTwoQubitGates(transpiledCircuit):
    num = 0
    for gate in transpiledCircuit.data:
        # print(type(gate[0]))
        if issubclass(type(gate[0]), Instruction):
            if gate[0].name == "cx":
                num += 1
    return num

couplingList = list()
for i in range(3):
    for j in range(3):
        if i is not j:
            couplingList.append([i, j])

squareCouplingList = list()
for i in range(4):
    for j in range(4):
        if i is not j:
            if abs(i-j) == 1:
                squareCouplingList.append([i, j])
squareCouplingList.append(([0, 3]))
squareCouplingList.append(([3, 0]))
provider = IBMQ.load_account()
backend = provider.get_backend('ibmq_lima')

basis_gates = backend.configuration().basis_gates

squareCouplingMap = CouplingMap(squareCouplingList)
couplingMap = CouplingMap(couplingList)

qcHERR = QuantumCircuit(4)
qcHERR.x(0)
qcHERR.x(1)
qcHERR.ccx(0, 1, 2)
qcHERR.measure_all()
qcHERR = qcHERR.decompose()
nonHERR = QuantumCircuit(4)
nonHERR.x(0)
nonHERR.x(1)
nonHERR.ccx(0, 1, 2)
nonHERR.measure_all()
circDag = circuit_to_dag(qcHERR)

targetCouplingMap = squareCouplingMap

bSwap = BasicSwap(targetCouplingMap)
baseTime = time.perf_counter()
bSwap.run(circDag)
bSwapTime = time.perf_counter() - baseTime

sabreSwap = SabreSwap(targetCouplingMap)
baseTime = time.perf_counter()
sabreSwap.run(circDag)
sabreSwapTime = time.perf_counter() - baseTime

stochasticSwap = StochasticSwap(targetCouplingMap)
baseTime = time.perf_counter()
stochasticSwap.run(circDag)
stochasticSwapTime = time.perf_counter() - baseTime

lookAheadSwap = LookaheadSwap(targetCouplingMap)
baseTime = time.perf_counter()
lookAheadSwap.run(circDag)
lookAheadSwapTime = time.perf_counter() - baseTime


for i in range(200):

    # Create a noise model for the simulations
    noise_model = noise.NoiseModel()
    errorRates = list()
    qiskitErrors = list()

    for i in range(len(squareCouplingList)//2):
        errorRates.append(random.randrange(1, 10, 1)/100.0)
        qiskitErrors.append(noise.depolarizing_error(errorRates[i], 2))

    edges = targetCouplingMap.get_edges()
    uniqueEdges = set()
    for edge in edges:
        uniqueEdges.add(tuple(sorted(edge)))
    
    noiseGraph = nx.Graph()
    noiseGraph.add_nodes_from([0, 7])

    errorIdex = 0
    for edge in uniqueEdges:
        noise_model.add_quantum_error(qiskitErrors[errorIdex], ['cx'], edge)
        noiseGraph.add_edge(edge[0], edge[1], weight=1-errorRates[errorIdex])
        errorIdex += 1

    herr = HERR.HERR(targetCouplingMap, noiseGraph)
    basSwap = BasicSwap(targetCouplingMap)

    #print(gridCouplingMap)
    # Run HERR
    baseTime = time.perf_counter()
    HERRRes = herr.run(circDag)
    HERRSwapTime = time.perf_counter() - baseTime
    updatedCirc = dag_to_circuit(HERRRes)

    
    print(str(HERRSwapTime) + " " + str(bSwapTime) + " " + str(sabreSwapTime) + " " + str(stochasticSwapTime) + " " + str(lookAheadSwapTime))






