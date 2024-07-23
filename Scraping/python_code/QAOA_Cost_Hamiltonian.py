from qiskit import QuantumCircuit
from qiskit.circuit import Parameter
import numpy as np
import random

class CostHamiltonian:

    circuit = {}

    def __init__(self, numQubits, layers=1, costType='maxcut', problem=None):
        self.numQubits = numQubits
        self.costType = costType
        self.layers = layers
        self.problem = problem

    def build(self):
        self.circuit = {}

        for l in range(0, self.layers):
            if (self.costType == 'rz_maxcut'):
                circuitDetails = self.__buildMaxcutLayer(self.problem, l)
                self.circuit[l] = circuitDetails

            elif (self.costType == 'ma_rz_maxcut'):
                circuitDetails = self.__buildMAMaxcutLayer(self.problem, l)
                self.circuit[l] = circuitDetails

            elif (self.costType == 'two_local_real_maxcut'):
                circuitDetails = self.__buildTwoLocalRealMaxcutLayer(self.problem, l)
                self.circuit[l] = circuitDetails

            elif (self.costType == "constant_maxcut"):
                circuitDetails = self.__buildMaxcutConstantLayer(self.problem, l)
                self.circuit[l] = circuitDetails

            elif (self.costType == "ry_maxcut"):
                circuitDetails = self.__buildRYMaxcutLayer(self.problem, l)
                self.circuit[l] = circuitDetails

            elif (self.costType == "ma_ry_maxcut"):
                circuitDetails = self.__buildMARYMaxcutLayer(self.problem, l)
                self.circuit[l] = circuitDetails
            
            elif (self.costType == "rx_maxcut"):
                circuitDetails = self.__buildRXMaxcutLayer(self.problem, l)
                self.circuit[l] = circuitDetails

            elif (self.costType == "ma_rx_maxcut"):
                circuitDetails = self.__buildMARXMaxcutLayer(self.problem, l)
                self.circuit[l] = circuitDetails

            elif (self.costType == "cx_ry_maxcut"):
                circuitDetails = self.__buildCXRYMaxcutLayer(self.problem, l)
                self.circuit[l] = circuitDetails

            elif (self.costType == "none"):
                circuitDetails = self.__buildNoCircuit()
                self.circuit[l] = circuitDetails

            elif (self.costType == "3SAT"):
                circuitDetails = self.__build3SATLayer(None, l)
                self.circuit[l] = circuitDetails
            elif (self.costType == "test_rz_maxcut"):
                circuitDetails = self.__buildTestMaxcutLayer(self.problem, l)
                self.circuit[l] = circuitDetails

            

        return True
    
    def getCircuitAtLayer(self, l):
        return self.circuit[l]
    
    def getAllCircuits(self):
        return self.circuit
    

    def __buildMaxcutConstantLayer(self, graph, l):
        # theta = Parameter('cost_maxcut_' + str(l))

        qc = QuantumCircuit(self.numQubits)
        for edge in graph.edges():
            qc.rzz(np.pi/len(graph.edges()), edge[0], edge[1])
        return (qc, [])
    
    def __buildMaxcutLayer(self, graph, l):
        theta = Parameter('cost_maxcut_' + str(l))

        qc = QuantumCircuit(self.numQubits)
        for edge in graph.edges():
            qc.rzz(theta, edge[0], edge[1])
        return (qc, [theta])
    
    
    def __buildMAMaxcutLayer(self, graph, l):
        theta = [Parameter('cost_maxcut_' + str(l) + "_" + str(i)) for i in range(0, len(graph.edges()))]

        qc = QuantumCircuit(self.numQubits)
        i = 0
        for edge in graph.edges():
            qc.rzz(theta[i], edge[0], edge[1])
            i+=1
        return (qc, theta)
    
    def __buildNoCircuit(self):

        qc = QuantumCircuit(self.numQubits)

        return (qc, [])
    
    def __buildTwoLocalRealMaxcutLayer(self, graph, l):

        theta = [Parameter('cost_maxcut_' + str(l) + "_" + str(i)) for i in range(0, 3*len(graph.edges()))]

        qc = QuantumCircuit(self.numQubits)
        i = 0
        for edge in graph.edges():
            qc.ry(theta[i], edge[0])
            i+=1
            qc.cx(edge[0], edge[1])
            qc.ry(theta[i], edge[0])
            i+=1
            qc.ry(theta[i], edge[1])
            i+=1

            
        return (qc, theta)
    
    def __buildRYMaxcutLayer(self, graph, l):

        theta = Parameter('cost_maxcut_' + str(l))

        
    
        qc = QuantumCircuit(self.numQubits)
        i = 0

        edges = list(graph.edges())
        v = len(graph.nodes)
        orderedEdges = []
        rightEdges = []

        # j = list(range(1, v))

        for e in edges:
            e1 = e[0]
            e2 = e[1]
            if (e1 > e2):
                rightEdges.append((e2, e1))
            else:
                rightEdges.append(e)

        for e in rightEdges:
            e1 = e[0]
            e2 = e[1]
            orderedEdges.append((v - 1 - e2, v - 1 - e1))

        orderedEdges = rightEdges
        orderedEdges.sort(key=lambda x:x[0], reverse=False)
        orderedEdges.sort(key=lambda x:x[1], reverse=False)
        
        print(orderedEdges)

        counts = [0] * v
        for e in orderedEdges:
            counts[e[1]] += 1
        print(counts)

        for edge in orderedEdges:
            qc.cx(edge[0], edge[1])
            qc.ry(theta,edge[1])
            qc.cx(edge[0], edge[1])
        return (qc, [theta])
    
    def __buildMARYMaxcutLayer(self, graph, l):
        theta = [Parameter('cost_maxcut_' + str(l) + "_" + str(i)) for i in range(0, len(graph.edges()))]

        qc = QuantumCircuit(self.numQubits)
        i = 0

        edges = list(graph.edges())
        v = len(graph.nodes)
        orderedEdges = []
        rightEdges = []

        # j = list(range(1, v))

        for e in edges:
            e1 = e[0]
            e2 = e[1]
            if (e1 > e2):
                rightEdges.append((e2, e1))
            else:
                rightEdges.append(e)

        for e in rightEdges:
            e1 = e[0]
            e2 = e[1]
            orderedEdges.append((v - 1 - e2, v - 1 - e1))

        orderedEdges = rightEdges

       



       

        # for e in rightEdges.copy():
        #     # print(e)
        #     e1 = e[0]
        #     e2 = e[1]
        #     if (e2 in j):
        #         rightEdges.remove(e)
        #         orderedEdges.append(e)
        #         j.remove(e2)

        # # print(len(orderedEdges))

        # orderedEdges.sort(key=lambda x:x[1], reverse=False)


        # orderedEdges = orderedEdges + rightEdges
        # # print(orderedEdges)
        
        # print(orderedEdges)
        orderedEdges.sort(key=lambda x:x[0], reverse=False)
        orderedEdges.sort(key=lambda x:x[1], reverse=False)
        
        print(orderedEdges)

        counts = [0] * v
        for e in orderedEdges:
            counts[e[1]] += 1
        print(counts)

        

        




        # qc.cx(0, 1)
        # qc.ry(np.pi/2,1)
        # qc.cx(0, 1)

        # qc.cx(0, 2)
        # qc.ry(-np.pi/2,2)
        # qc.cx(0, 2)

        for edge in orderedEdges:
            qc.cx(edge[0], edge[1])
            qc.ry(theta[i],edge[1])
            qc.cx(edge[0], edge[1])
            
            i+=1
        return (qc, theta)
    
    def __buildRXMaxcutLayer(self, graph, l):

        theta = Parameter('cost_maxcut_' + str(l))

        qc = QuantumCircuit(self.numQubits)
        for edge in graph.edges():
            qc.rxx(theta, edge[0], edge[1])
        return (qc, [theta])
    
    def __buildMARXMaxcutLayer(self, graph, l):
        theta = [Parameter('cost_maxcut_' + str(l) + "_" + str(i)) for i in range(0, len(graph.edges()))]

        qc = QuantumCircuit(self.numQubits)
        i = 0
        for edge in graph.edges():
            qc.rxx(theta[i], edge[0], edge[1])
            i+=1
        return (qc, theta)
    
    def __buildCXRYMaxcutLayer(self, graph, l):

        theta = Parameter('cost_maxcut_' + str(l))
        i = 0
        qc = QuantumCircuit(self.numQubits)
        for edge in graph.edges():
            qc.cx(edge[0], edge[1])
            qc.ry(theta, edge[1])
            qc.cx(edge[0], edge[1])
            i+=1
        return (qc, [theta])
    
    def __buildMACXRYMaxcutLayer(self, graph, l):

        theta = [Parameter('cost_maxcut_' + str(l) + "_" + str(i)) for i in range(0, len(graph.edges()))]
        i = 0
        qc = QuantumCircuit(self.numQubits)
        for edge in graph.edges():
            qc.cx(edge[0], edge[1])
            qc.ry(theta[i], edge[1])
            qc.cx(edge[0], edge[1])
            i+=1
        return (qc, theta)
    

    
    def __build3SATLayer(self, clauses, l):
        theta = Parameter('cost_maxcut_' + str(l))

        qc = QuantumCircuit(self.numQubits)

        qc.h([0, 1, 2])
    
        
        # clause 1
        qc.x([0, 1, 2])
        qc.mct([0, 1, 2], 3)
        qc.rz(theta, 3)
        qc.mct([0, 1, 2], 3)
        qc.x([0, 1, 2])

        # clause 2
        qc.x([1])
        qc.mct([0, 1, 2], 3)
        qc.rz(theta, 3)
        qc.mct([0, 1, 2], 3)
        qc.x([1])

        # clause 3
        qc.x([2])
        qc.mct([0, 1, 2], 3)
        qc.rz(theta, 3)
        qc.mct([0, 1, 2], 3)
        qc.x([2])

        # clause 4
        qc.x([2, 3])
        qc.mct([0, 1, 2], 3)
        qc.rz(theta, 3)
        qc.mct([0, 1, 2], 3)
        qc.x([2, 3])

        # clause 5
        qc.x([3])
        qc.mct([0, 1, 2], 3)
        qc.rz(theta, 3)
        qc.mct([0, 1, 2], 3)
        qc.x([3])

        # # clause 6
        # qc.x([1, 2])
        # qc.mct([0, 1, 2], 3)
        # qc.rz(theta, 3)
        # qc.mct([0, 1, 2], 3)
        # qc.x([1, 2])

        # clause 7
        qc.mct([0, 1, 2], 3)
        qc.rz(theta, 3)
        qc.mct([0, 1, 2], 3)

        return (qc, [theta])
    

    def __buildTestMaxcutLayer(self, graph, l):
        theta1 = Parameter('cost_maxcut_1_' + str(l))
        theta2 = Parameter('cost_maxcut_2_' + str(l))
        qc = QuantumCircuit(self.numQubits)
        for edge in graph.edges():
            qc.rz(theta2, edge[0])
            qc.rz(theta2, edge[1])
            qc.rzz(theta1, edge[0], edge[1])
        return (qc, [theta1, theta2])