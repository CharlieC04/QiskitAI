from qiskit import *
import numpy as np
import networkx as nx
import random as ran
from qiskit.visualization import *

def ranCircCXD(G, circ, cnots, depth, barrier, cc, dd, num_V, MI, V, L):
    if (2*cnots + 1 < depth):
        print("Impossible circuit parameters: number of CNOTs is too low to reach the desired depth. Try again with different parameters.")
    elif (depth*len(MI) < cnots):
        print("Impossible circuit parameters: depth is too low to fit all the required CNOTs into the given graph. Try again with different parameters.")
    else:
        print("Constructing circuit with ", cnots, " CNOTs and ", depth," depth...")

        #preconstruction:
        for j in V:
            for d in range(depth):
                cc[j].append(0)
        print('Preconstruction...')
        
        k = 0
        sparse = True
        contin = True

        #adding CNOT gates:
        while (sparse):
            n = 0
            cc = []
            for j in V:
                cc.append([])
            for j in V:
                for d in range(depth):
                    cc[j].append(0)
            #print('new attempt:', k)
            if (k > 100*cnots*depth*depth):
                print("Sorry, unable to construct the circuit after ", k, " attempts. Try again with different parameters.")
                contin = False
                break
            while (n < cnots):
                k +=1
                if (k > 100*cnots*depth*depth):
                    break
                edge = ran.sample(G.edges(),1)[0]
                node1 = edge[0]
                node2 = edge[1]
                d = ran.randint(0,depth-1)
                
                if (cc[node1][d] == 0 and cc[node2][d] == 0):
                    if ran.choice([0,1]):                   
                        cc[node1][d] = ['C', node2]
                        cc[node2][d] = 'X'
                    else:
                        cc[node2][d] = ['C', node1]
                        cc[node1][d] = 'X'
                    n +=1
            
            #check if circuit is too sparse
            unsparse = False
            for j in V:
                sparsehere = False
                for d in range(depth-1):
                    if (cc[j][d] == 0 and cc[j][d+1] == 0):
                        sparsehere = True
                        break
                if not(sparsehere):
                    unsparse = True
            if (unsparse):
                sparse = False
            
        #print('cc looks like this:')
        #print(cc)
        #actual construction:
        if (contin):
            print('Successful at attempt ', k)
            print('Constructing circuit...')
            for j in V:
                if (isinstance(cc[j][0],list)):
                    if (cc[j][0][0] == 'C'):
                        if (cc[cc[j][0][1]][0] == 'X'):
                            circ.cx(j,cc[j][0][1])
                elif (cc[j][0] == 0):
                    theta = ran.uniform(0.0, 2*np.pi)
                    phi = ran.uniform(0.0, 2*np.pi)
                    lam = ran.uniform(0.0, 2*np.pi)
                    circ.u3(theta, phi, lam, j)
                    
            for d in range(1,depth):
                if(barrier):
                    circ.barrier()
                for j in V:
                    if (isinstance(cc[j][d],list)):
                        if (cc[j][d][0] == 'C'):
                            if (cc[cc[j][d][1]][d] == 'X'):
                                circ.cx(j,cc[j][d][1])
                    elif ((cc[j][d] == 0) and (cc[j][d-1] != 0)):
                        theta = ran.uniform(0.0, 2*np.pi)
                        phi = ran.uniform(0.0, 2*np.pi)
                        lam = ran.uniform(0.0, 2*np.pi)
                        circ.u3(theta, phi, lam, j)
                            
def ranCircCX(G, circ, cnots, barrier, cc, num_V):
    print("Constructing circuit with ", cnots, " CNOTs and arbitrary depth...")
    n = 0
    while (n < cnots):
        gate=ran.choice(['CX','U3']) #choose randomly between CNOT and U3
        if (gate == 'U3'):
            node = ran.choice(range(num_V))
            if (not(cc[node]) or (cc[node][-1] != 'U3')):
                theta = ran.uniform(0.0, 2*np.pi)
                phi = ran.uniform(0.0, 2*np.pi)
                lam = ran.uniform(0.0, 2*np.pi)
                circ.u3(theta, phi, lam, node)
                cc[node].append('U3')
        else:
            n += 1
            edge = ran.sample(G.edges(),1)[0]
            node1 = edge[0]
            node2 = edge[1]
            if ran.choice([0,1]):
                circ.cx(node1,node2)
                cc[node1].append('C')
                cc[node2].append('X')
            else:
                circ.cx(node2,node1)
                cc[node2].append('C')
                cc[node1].append('X')

def ranCircD(G, circ, depth, barrier, cc, dd, num_V):
    print("Constructing circuit with arbitrarly many CNOTs and ", depth," depth...")
    d = 0
    while(d < depth):
        if(barrier):
            circ.barrier()
        gate=ran.choice(['CX','U3']) #choose randomly between CNOT and U3
        if (gate == 'U3'):
            node = ran.choice(range(num_V))
            if (not(cc[node]) or (cc[node][-1] != 'U3')):
                theta = ran.uniform(0.0, 2*np.pi)
                phi = ran.uniform(0.0, 2*np.pi)
                lam = ran.uniform(0.0, 2*np.pi)
                circ.u3(theta, phi, lam, node)
                cc[node].append('U3')
                dd[node] += 1
        else:
            edge = ran.sample(G.edges(),1)[0]
            node1 = edge[0]
            node2 = edge[1]
            if ran.choice([0,1]):
                circ.cx(node1,node2)
                cc[node1].append('C')
                cc[node2].append('X')
            else:
                circ.cx(node2,node1)
                cc[node2].append('C')
                cc[node1].append('X')
            dd[node1] += 1
            dd[node2] += 1
            dd[node1] = max(dd[node1],dd[node2])
            dd[node2] = dd[node1]
        d = max(dd)
        #print(d)


def createGraph(backend, n_qubits=0):
    if backend.configuration().simulator:
        if n_qubits <= 0:
            raise ValueError("Please specify number of qubits for a simulator.")
        G=nx.complete_graph(n_qubits)
    else:
        n_qubits=backend.configuration().n_qubits
        G=nx.Graph()
        G.add_nodes_from(np.arange(n_qubits))
        G.add_edges_from(backend.configuration().coupling_map)
    return G

def randomCircuit(G, cnots=0, depth=0, barrier=False): #Either cnots or depth can be zero, which means "unspecified".
    V = list(G.nodes)
    num_V = len(V)
    L = nx.line_graph(G)
    MI = nx.maximal_independent_set(L)
    
    q = QuantumRegister(num_V)
    c = ClassicalRegister(num_V)
    circ = QuantumCircuit(q,c)
    circ.barrier()
    ran.seed()
    #copy of circuit for internal tracing:
    cc = []
    for j in V:
        cc.append([])
    dd = []
    for j in V:
        dd.append(0)

    #begin construction:
    if (cnots and depth):
        ranCircCXD(G, circ, cnots, depth, barrier, cc, dd, num_V, MI, V, L)

    elif (cnots and not(depth)):
        ranCircCX(G, circ, cnots, barrier, cc, num_V)
                    
    elif (not(cnots) and depth):
        ranCircD(G, circ, depth, barrier, cc, dd, num_V)
    else:
        print("This will only return an empty circuit.")
    circ.barrier()
    print('Depth is: ', circ.depth())
    circ.measure(q,c)
    return circ

