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

transpiledBasic = transpile(qcHERR, Aer.get_backend('qasm_simulator'),
                                coupling_map=squareCouplingMap,
                                basis_gates=basis_gates,
                                routing_method='basic',
                                layout_method='trivial')
transpiledSabre = transpile(qcHERR, Aer.get_backend('qasm_simulator'),
                                coupling_map=squareCouplingMap,
                                basis_gates=basis_gates,
                                routing_method='sabre',
                                layout_method='trivial')
transpiledStochastic = transpile(qcHERR, Aer.get_backend('qasm_simulator'),
                                coupling_map=squareCouplingMap,
                                basis_gates=basis_gates,
                                routing_method='stochastic',
                                layout_method='trivial')
transpiledLookahead = transpile(qcHERR, Aer.get_backend('qasm_simulator'),
                                coupling_map=squareCouplingMap,
                                basis_gates=basis_gates,
                                routing_method='lookahead',
                                layout_method='trivial')

s = '0111'
for i in range(100):

    # Create a noise model for the simulations
    noise_model = noise.NoiseModel()
    err1Rate, err2Rate, err3Rate, err4Rate = random.randrange(1, 20, 1)/100.0, random.randrange(1, 20, 1)/100.0, random.randrange(1, 20, 1)/100.0,\
         random.randrange(1, 10, 1)/100.0
    error_1 = noise.depolarizing_error(err1Rate, 2)
    error_2 = noise.depolarizing_error(err2Rate, 2)
    error_3 = noise.depolarizing_error(err3Rate, 2)
    error_4 = noise.depolarizing_error(err4Rate, 2)
    noise_model.add_quantum_error(error_1, ['cx'], [0, 1])
    noise_model.add_quantum_error(error_2, ['cx'], [1, 2])
    noise_model.add_quantum_error(error_3, ['cx'], [2, 3])
    noise_model.add_quantum_error(error_4, ['cx'], [0, 3])

    # Generate a noise graph to pass into HERR
    noiseGraph = nx.Graph()
    noiseGraph.add_nodes_from([0, 2])
    noiseGraph.add_edge(0, 1, weight=1.0-err1Rate)
    noiseGraph.add_edge(1, 2, weight=1.0-err2Rate)
    noiseGraph.add_edge(2, 3, weight=1.0-err3Rate)
    noiseGraph.add_edge(0, 3, weight=1.0-err4Rate)

    herr = HERR.HERR(squareCouplingMap, noiseGraph)
    basSwap = BasicSwap(squareCouplingMap)

    #print(squareCouplingMap)
    # Run HERR
    HERRRes = herr.run(circDag)
    updatedCirc = dag_to_circuit(HERRRes)

    bSwapRes = basSwap.run(circDag)
    bSwapCirc = dag_to_circuit(bSwapRes)

    # Transpile HERR
    transpiledHERR = transpile(updatedCirc, Aer.get_backend('qasm_simulator'),
                                 coupling_map=squareCouplingMap,
                                 basis_gates=basis_gates,
                                 routing_method='basic',
                                 layout_method='trivial')

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
    print(str(simResultHERR.get_counts()[s]/1024.0) + " " + str(simResultBasic.get_counts()[s]/1024.0) + " " + str(simResultSabre.get_counts()[s]/1024.0) + " " + str(simResultLookahead.get_counts()[s]/1024.0) + " " + str(simResultStochastic.get_counts()[s]/1024.0))





