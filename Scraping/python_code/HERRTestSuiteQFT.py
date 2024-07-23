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



couplingList = list()
for i in range(4):
    for j in range(4):
        if i is not j:
            couplingList.append([i, j])


provider = IBMQ.load_account()
backend = provider.get_backend('ibmq_lima')

basis_gates = backend.configuration().basis_gates

couplingMap = CouplingMap(couplingList)

squareCouplingList = list()
for i in range(4):
    for j in range(4):
        if i is not j:
            if abs(i-j) == 1:
                squareCouplingList.append([i, j])
squareCouplingList.append(([0, 3]))
squareCouplingList.append(([3, 0]))
squareCouplingMap = CouplingMap(squareCouplingList)

gridCouplingList = list()
for i in range(4):
    for j in range(4):
        if i is not j:
            if abs(i-j) == 1:
                gridCouplingList.append([i, j])
for i in range(4,8):
    for j in range(4,8):
        if i is not j:
            if abs(i-j) == 1:
                gridCouplingList.append([i, j])

gridCouplingList.append(([0, 4]))
gridCouplingList.append(([4, 0]))
gridCouplingList.append(([1, 5]))
gridCouplingList.append(([5, 1]))
gridCouplingList.append(([2, 6]))
gridCouplingList.append(([6, 2]))
gridCouplingList.append(([3, 7]))
gridCouplingList.append(([7, 3]))
gridCouplingMap = CouplingMap(gridCouplingList)

jakatraCouplingList = [[0, 1], [1, 0], [1, 2], [2, 1], [1, 3], [3, 1], [3,5], [5,3], [4,5], [5,4], [6,5], [5,6]]
jakatraCouplingMap = CouplingMap(jakatraCouplingList)

def qft_rotations(circuit, n):
    """Performs qft on the first n qubits in circuit (without swaps)"""
    if n == 0:
        return circuit
    n -= 1
    circuit.h(n)
    for qubit in range(n):
        circuit.cp(pi/2**(n-qubit), qubit, n)
    # At the end of our function, we call the same function again on
    # the next qubits (we reduced n by one earlier in the function)
    qft_rotations(circuit, n)


def swap_registers(circuit, n):
    for qubit in range(n//2):
        circuit.swap(qubit, n-qubit-1)
    return circuit


def qft(circuit, n):
    """QFT on the first n qubits in circuit"""
    qft_rotations(circuit, n)
    swap_registers(circuit, n)
    return circuit


def inverse_qft(circuit, n):
    """Does the inverse QFT on the first n qubits in circuit"""
    # First we create a QFT circuit of the correct size:
    qft_circ = qft(QuantumCircuit(n), n)
    # Then we take the inverse of this circuit
    invqft_circ = qft_circ.inverse()
    # And add it to the first n qubits in our existing circuit
    circuit.append(invqft_circ, circuit.qubits[:n])
    return circuit.decompose()  # .decompose() allows us to see the individual gates

def countTwoQubitGates(transpiledCircuit):
    num = 0
    for gate in transpiledCircuit.data:
        # print(type(gate[0]))
        if issubclass(type(gate[0]), Instruction):
            if gate[0].name == "cx":
                num += 1
    return num

s = '1011011'
n = len(s)
# Let's see how it looks:
circuit = QuantumCircuit(n)

for ii, yesno in enumerate(reversed(s)):
    if yesno == '1':
        circuit.x(ii)


qft(circuit, n)
circuit = inverse_qft(circuit, n)
circuit.measure_all()

circDag = circuit_to_dag(circuit)

targetCouplingMap = jakatraCouplingMap
    # Transpile non HERR
transpiledBasic = transpile(circuit, Aer.get_backend('qasm_simulator'),
                                coupling_map=targetCouplingMap,
                                basis_gates=basis_gates,
                                routing_method='basic',
                                layout_method='trivial')
transpiledSabre = transpile(circuit, Aer.get_backend('qasm_simulator'),
                                coupling_map=targetCouplingMap,
                                basis_gates=basis_gates,
                                routing_method='sabre',
                                layout_method='trivial')
transpiledStochastic = transpile(circuit, Aer.get_backend('qasm_simulator'),
                                coupling_map=targetCouplingMap,
                                basis_gates=basis_gates,
                                routing_method='stochastic',
                                layout_method='trivial')
transpiledLookahead = transpile(circuit, Aer.get_backend('qasm_simulator'),
                                coupling_map=targetCouplingMap,
                                basis_gates=basis_gates,
                                routing_method='lookahead',
                                layout_method='trivial')
for i in range(200):

    # Create a noise model for the simulations
    noise_model = noise.NoiseModel()
    errorRates = list()
    qiskitErrors = list()

    for i in range(len(jakatraCouplingList)//2):
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
        noiseGraph.add_edge(edge[0], edge[1], weight=errorRates[errorIdex])
        errorIdex += 1

    herr = HERR.HERR(targetCouplingMap, noiseGraph)
    basSwap = BasicSwap(targetCouplingMap)

    #print(gridCouplingMap)
    # Run HERR
    HERRRes = herr.run(circDag)
    updatedCirc = dag_to_circuit(HERRRes)

    bSwapRes = basSwap.run(circDag)
    bSwapCirc = dag_to_circuit(bSwapRes)

    # Transpile HERR
    transpiledHERR = transpile(updatedCirc, Aer.get_backend('qasm_simulator'),
                                 coupling_map=targetCouplingMap,
                                 basis_gates=basis_gates,
                                 routing_method='basic',
                                 layout_method='trivial')

    # if transpiledNormal != transpiledHERR:
    #     fName = "HERRQFTCouplingOutputs/HERRCirc" + str(i) + ".png"
    #     fName2 = "HERRQFTCouplingOutputs/NonCirc" + str(i) + ".png"
    #     transpiledHERR.draw(output='mpl', filename=fName)
    #     transpiledNormal.draw(output='mpl', filename=fName2)
    #     break
    # HERRCnotGateNum = countTwoQubitGates(transpiledHERR)
    # normalCnotGateNum  = countTwoQubitGates(transpiledNormal)
    # print(str(HERRCnotGateNum) + " " + str(normalCnotGateNum))
    sim = Aer.get_backend('qasm_simulator')

    simResultHERR = sim.run(transpiledHERR, noise_model=noise_model).result()
    simResultBasic = sim.run(transpiledBasic, noise_model=noise_model).result()
    simResultSabre = sim.run(transpiledSabre, noise_model=noise_model).result()
    simResultLookahead = sim.run(transpiledLookahead, noise_model=noise_model).result()
    simResultStochastic = sim.run(transpiledStochastic, noise_model=noise_model).result()

    # Output file and print results
    fName = "HERRQFTCouplingOutputs/HERRCirc" + str(i) + ".png"
    fName2 = "HERRQFTCouplingOutputs/NonCirc" + str(i) + ".png"
    #updatedCirc.draw(output='mpl', filename=fName)
    #bSwapCirc.draw(output='mpl', filename=fName2)
    #if transpiledNormal != transpiledHERR:
        #print("CIRCUIT CHANGED")
        #updatedCirc.draw(output='mpl', filename=fName)
        #bSwapCirc.draw(output='mpl', filename=fName2)
        #print("Iter: " + str(i) + " ErrorRate of edges (0,1) (1, 2), (0, 2), (1, 3), (2, 3), (0, 3) counts for HERR/nonHERR:")
        #print(str(err1Rate) + " " + str(err2Rate) + " " + str(err3Rate) + " " + str(err4Rate) + " " + str(err5Rate) + " " + str(err6Rate))
    if s in simResultHERR.get_counts() and s in simResultBasic.get_counts() and s in simResultSabre.get_counts() and s in simResultLookahead.get_counts() and s in simResultStochastic.get_counts():
        print(str(simResultHERR.get_counts()[s]/1024.0) + " " + str(simResultBasic.get_counts()[s]/1024.0) + " " + str(simResultSabre.get_counts()[s]/1024.0) + " " + str(simResultLookahead.get_counts()[s]/1024.0) + " " + str(simResultStochastic.get_counts()[s]/1024.0))
    else:
        print("Key error! Oops!")
        #print("----------------------")



