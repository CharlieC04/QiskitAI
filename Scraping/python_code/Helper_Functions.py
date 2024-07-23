from qiskit import QuantumCircuit
from qiskit.circuit.library import HGate
import networkx as nx
import random
import numpy as np

def getBestMaxcut(costFunction, v):
    bestCut = 0
    bestPartition = []
    for i in range(0, 2**v):
        partition = bin(i)
        partition = partition[2:]
        partition = "0" * (v - len(partition)) + partition
        cut = costFunction.getCost(partition)
        if (cut < bestCut):
            bestPartition = [partition]
            bestCut = cut
        elif (cut == bestCut):
            bestPartition.append(partition)
            
    return bestCut, bestPartition

def groverDiffuser(n):
    qc = QuantumCircuit(n)

    # Apply transformation |s> -> |00..0> (H-gates)
    qc.h(range(n))

    # Apply transformation |00..0> -> |11..1> (X-gates)
    qc.x(range(n))

    # Do multi-controlled-Z gate
    qc.h(n-1)
    qc.mct(list(range(n-1)), n-1)  # multi-controlled-toffoli
    qc.h(n-1)

    # Apply transformation |11..1> -> |00..0>
    for qubit in range(n):
        qc.x(qubit)

    # Apply transformation |00..0> -> |s>
    qc.h(range(n))

    # We will return the diffuser as a gate
    gate = qc.to_gate()
    gate.name = "diffuser"

    return gate

def qaoaCompressor(graph):
    nodes = list(graph.nodes)
    edges = list(graph.edges)

    # print(nodes)
    # print(edges)

    start = min(nodes, key=lambda node: sum(node in edge for edge in edges))
    # print(start)

    currentNodes = [start]
    nodes.remove(start)
    maxLen = 0

    deadNodes = []
    addedEdges = []

    while (len(nodes) > 0):
        current = min(currentNodes, key=lambda node: sum(node in edge for edge in edges))
        connectingEdges = [edge for edge in edges if current in edge]

        if (len(connectingEdges) == 0):
            currentNodes.remove(current)
            deadNodes.append(current)
        
        else:
            nextEdge = connectingEdges[0]

            for ver in nextEdge:
                if (ver != current):
                    nextNode = ver

            currentNodes.append(nextNode)
            nodes.remove(nextNode)
            connectingEdges = [edge for edge in edges if nextNode in edge]

            
        for edge in connectingEdges:
                if ((edge[0] in currentNodes or edge[0] in deadNodes) and (edge[1] in currentNodes or edge[1] in deadNodes)):
                    edges.remove(edge)
                    addedEdges.append(edge)
                
        if (len(currentNodes) > maxLen):
            maxLen = len(currentNodes)

        # print(currentNodes, current, nextNode)
        # print(edges)

    
def custom_graphs():
    graph = nx.Graph()
    n = 3
    graph.add_nodes_from(list(range(0, n)))
    graph.add_edges_from([(0, 1), (1, 2)])

    return graph


def ry_simulator(params, runs = 1000):
    def sim_ry(param):
        prob = random.random()
        if (prob > np.cos(param/2)**2):
            return "1"
        return "0"
        
    counts = {}  
    for i in range(0, runs):
        string = ""
        for param in params:
            string += sim_ry(param)

        if string in counts:
            counts[string] += 1
        else:
            counts[string] = 1

    # print("Epoch")

    return counts

def greedyMaxcutSolver(graph, costFunction):
    v = len(graph.nodes)
    guess = ["0"] * v
    bestCost = 0
    
    indices = list(range(0, v))

    while len(indices) > 0:
        bestIndex = -1
        for i in indices:
            currentGuess = guess.copy()
            currentGuess[i] = "1"
            cost = costFunction.getCost("".join(currentGuess)[::-1])
            # print("".join(currentGuess)[::-1])
            # print(cost)
            if (cost < bestCost):
                bestCost = cost
                bestIndex = i
                print(cost)
        if (bestIndex == -1):
            break
        guess[bestIndex] = "1"
        indices.remove(bestIndex)

    

    return (bestCost)


def customSATSolverCircuit(graph):
    v = len(graph.nodes)
    qc = QuantumCircuit(2*v, v)
    qc.h(range(0, v))
    for i in range(0, v):
        qc.cx(i, v+i)

    qc.barrier()

    hGate = HGate().control(2)


    for edge in graph.edges():
        v1 = edge[0]
        v2 = edge[1]
        
        qc.append(hGate, ([v1, v2, v + v1]))
        qc.append(hGate, ([v1, v2, v + v2]))

        qc.barrier()

        qc.x(v1)
        qc.x(v2)

        qc.append(hGate, ([v1, v2, v + v1]))
        qc.append(hGate, ([v1, v2, v + v2]))

        qc.x(v1)
        qc.x(v2)

        qc.barrier()

    
    qc.measure(range(v, 2*v), range(0, v))
    return qc

def customSATSolverCircuit(graph):
    v = len(graph.nodes)
    qc = QuantumCircuit(2*v, v)
    qc.h(range(0, v))
    for i in range(0, v):
        qc.cx(i, v+i)

    qc.barrier()

    # hGate = HGate().control(2)

    i = 0

    order = [1, 0, 0, 0, 0, 0, 0, 0]




    for edge in graph.edges():
        v1 = edge[0]
        v2 = edge[1]

        o = order[i]
        if (o):
            vC = v2
        else:
            vC = v1
        
        qc.toffoli(v1, v2, v + vC)

        qc.barrier()

        qc.x(v1)
        qc.x(v2)

        qc.toffoli(v1, v2, v + vC)

        qc.x(v1)
        qc.x(v2)

        qc.barrier()
        i+=1

    
    qc.measure(range(v, 2*v), range(0, v))
    return qc




    