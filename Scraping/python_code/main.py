
import numpy as np
import networkx as nx

import qiskit
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, execute, Aer, assemble
from qiskit.quantum_info import Statevector
from qiskit.aqua.algorithms import NumPyEigensolver
from qiskit.quantum_info import Pauli
from qiskit.aqua.operators import op_converter
from qiskit.aqua.operators import WeightedPauliOperator
from qiskit.visualization import plot_histogram
from qiskit.providers.aer.extensions.snapshot_statevector import *

from thirdParty.classical import rand_graph, classical, bitstring_to_path, calc_cost
from utils import mapeo_grafo
from collections import defaultdict
from operator import itemgetter
from scipy.optimize import minimize
import matplotlib.pyplot as plt

LAMBDA = 10
SEED = 10
SHOTS = 10000

# returns the bit index for an alpha and j
def bit(i_city, l_time, num_cities):
    return i_city * num_cities + l_time 

# e^(cZZ) 
def append_zz_term(qc, q_i, q_j, gamma, constant_term):
    qc.cx(q_i, q_j)
    qc.rz(2*gamma*constant_term,q_j)
    qc.cx(q_i, q_j)


# e^(cZ)
def append_z_term(qc, q_i, gamma, constant_term):
    qc.rz(2*gamma*constant_term, q_i)

# e^(cX)
def append_x_term(qc,qi,beta):
    qc.rx(-2*beta, qi)

def get_not_edge_in(G):
    N = G.number_of_nodes()
    not_edge = []
    for i in range(N):
        for j in range(N):
            if i != j:
                buffer_tupla = (i,j)
                in_edges = False
                for edge_i, edge_j in G.edges():             
                    if ( buffer_tupla == (edge_i, edge_j) or buffer_tupla == (edge_j, edge_i)):
                        in_edges = True
                if in_edges == False:
                    not_edge.append((i, j))
    return not_edge

def get_classical_simplified_z_term(G, _lambda):
    
    # recorrer la formula Z con datos grafo se va guardando en diccionario que acumula si coinciden los terminos
    N = G.number_of_nodes()
    E = G.edges()

    #  z term #

    z_classic_term = [0] * N**2

    # first term
    for l in range(N):
        for i in range(N):
            z_il_index =  bit(i, l, N)
            z_classic_term[z_il_index] += -1 * _lambda

    # second term
    for l in range(N):
        for j in range(N):
            for i in range(N):
                if i < j:
                    # z_il
                    z_il_index =  bit(i, l, N)
                    z_classic_term[z_il_index] +=  _lambda / 2
                    # z_jl
                    z_jl_index =  bit(j, l, N)
                    z_classic_term[z_jl_index] +=  _lambda / 2 

    # third term
    for i in range(N):
        for l in range(N):
            for j in range(N):
                if l < j:
                    # z_il
                    z_il_index =  bit(i, l, N)
                    z_classic_term[z_il_index] +=  _lambda / 2
                    # z_ij
                    z_ij_index =  bit(i, j, N)
                    z_classic_term[z_ij_index] +=  _lambda / 2

    # fourth term
    not_edge = get_not_edge_in(G) # include order tuples ej = (1,0), (0,1)
    for edge in not_edge:
        for l in range(N):
            i = edge[0]
            j = edge[1]
            # z_il
            z_il_index =  bit(i, l, N)
            z_classic_term[z_il_index] +=  _lambda / 4
            # z_j(l+1)
            l_plus = (l+1) % N
            z_jlplus_index =  bit(j, l_plus, N)
            z_classic_term[z_jlplus_index] +=  _lambda / 4
    
    # fifthy term
    weights = nx.get_edge_attributes(G,'weight')
    for edge_i, edge_j in G.edges(): 
        weight_ij = weights.get((edge_i,edge_j))
        weight_ji = weight_ij
        for l in range(N):

            # z_il
            z_il_index =  bit(edge_i, l, N)
            z_classic_term[z_il_index] +=  weight_ij / 4

            # z_jlplus
            l_plus = (l+1) % N
            z_jlplus_index =  bit(edge_j, l_plus, N)
            z_classic_term[z_jlplus_index] +=  weight_ij / 4

            # add order term because G.edges() do not include order tuples #
            # z_i'l
            z_il_index =  bit(edge_j, l, N)
            z_classic_term[z_il_index] +=  weight_ji / 4

            # z_j'lplus
            l_plus = (l+1) % N
            z_jlplus_index =  bit(edge_i, l_plus, N)
            z_classic_term[z_jlplus_index] +=  weight_ji / 4

    return z_classic_term

def tsp_obj_2(x, G,_lambda):
    # obtenemos el valor evaluado en f(x_1, x_2,... x_n)
    not_edge = get_not_edge_in(G)
    N = G.number_of_nodes()
    
    tsp_cost=0
    #Distancia
    weights = nx.get_edge_attributes(G,'weight')
    for edge_i, edge_j in G.edges(): 
        weight_ij = weights.get((edge_i,edge_j))
        weight_ji = weight_ij
        for l in range(N):

            # x_il
            x_il_index = bit(edge_i, l, N)

            # x_jlplus
            l_plus = (l+1) % N
            x_jlplus_index = bit(edge_j, l_plus, N)
            tsp_cost+= int(x[x_il_index]) * int(x[x_jlplus_index]) * weight_ij

            # add order term because G.edges() do not include order tuples #
            # x_i'l
            x_il_index =  bit(edge_j, l, N)

            # x_j'lplus
            x_jlplus_index =  bit(edge_i, l_plus, N)
            tsp_cost += int(x[x_il_index]) * int(x[x_jlplus_index]) * weight_ji

    #Constraint 1
    for l in range(N):
        penal1 = 1
        for i in range(N):
            x_il_index = bit(i, l, N)
            penal1 -= int(x[x_il_index])
    
        tsp_cost += _lambda * penal1**2
        
    #Contstraint 2
    for i in range(N):
        penal2 = 1
        for l in range(N):
            x_il_index = bit(i, l, N)

            penal2 -= int(x[x_il_index])
    
        tsp_cost += _lambda*penal2**2
    
    #Constraint 3    
        
    for edge in not_edge:
        for l in range(N):
            i = edge[0]
            j = edge[1]
            # x_il
            x_il_index =  bit(i, l, N)
            # x_j(l+1)
            l_plus = (l+1) % N
            x_jlplus_index = bit(j, l_plus, N)
            tsp_cost += int(x[x_il_index]) * int(x[x_jlplus_index]) * _lambda

    return tsp_cost

def get_classical_simplified_zz_term(G, _lambda):

    # recorrer la formula Z con datos grafo se va guardando en diccionario que acumula si coinciden los terminos
    N = G.number_of_nodes()
    E = G.edges()

    # zz term #
    zz_classic_term = [[0] * N**2 for i in range(N**2) ]
     
    # first term
    for l in range(N):
        for j in range(N):
            for i in range(N):
                if i < j:
                    # z_il
                    z_il_index =  bit(i, l, N)
                    # z_jl
                    z_jl_index =  bit(j, l, N)
                    zz_classic_term[z_il_index][z_jl_index] +=  _lambda / 2 

    # second term
    for i in range(N):
        for l in range(N):
            for j in range(N):
                if l < j:
                    # z_il
                    z_il_index =  bit(i, l, N)
                    # z_ij
                    z_ij_index =  bit(i, j, N)
                    zz_classic_term[z_il_index][z_ij_index] +=  _lambda / 2 
    
    # third term
    not_edge = get_not_edge_in(G)
    for edge in not_edge:
        for l in range(N):
            i = edge[0]
            j = edge[1]
            # z_il
            z_il_index =  bit(i, l, N)
            # z_j(l+1)
            l_plus = (l+1) % N
            z_jlplus_index =  bit(j, l_plus, N)
            zz_classic_term[z_il_index][z_jlplus_index] +=  _lambda / 4
    
    # fourth term
    weights = nx.get_edge_attributes(G,'weight')
    for edge_i, edge_j in G.edges(): 
        weight_ij = weights.get((edge_i,edge_j))
        weight_ji = weight_ij
        for l in range(N):

            # z_il
            z_il_index =  bit(edge_i, l, N)

            # z_jlplus
            l_plus = (l+1) % N
            z_jlplus_index =  bit(edge_j, l_plus, N)
            zz_classic_term[z_il_index][z_jlplus_index] +=  weight_ij / 4

            # add order term because G.edges() do not include order tuples #
            # z_i'l
            z_il_index =  bit(edge_j, l, N)

            # z_j'lplus
            l_plus = (l+1) % N
            z_jlplus_index =  bit(edge_i, l_plus, N)
            zz_classic_term[z_il_index][z_jlplus_index] +=  weight_ji / 4
    
    return zz_classic_term

def get_classical_simplified_hamiltonian(G, _lambda):    
    
    # z term #
    z_classic_term = get_classical_simplified_z_term(G, _lambda)
    # zz term #
    zz_classic_term = get_classical_simplified_zz_term(G, _lambda)

    return z_classic_term, zz_classic_term

def get_cost_circuit(G, gamma, _lambda):

    N =  G.number_of_nodes()
    N_square = N**2

    qc = QuantumCircuit(N_square,N_square)
      
    z_classic_term, zz_classic_term = get_classical_simplified_hamiltonian(G, _lambda)      
    
    # z term
    for i in range(N_square):
        if z_classic_term[i] != 0:
            append_z_term(qc, i, gamma, z_classic_term[i])
    
    # zz term
    for i in range(N_square):
        for j in range(N_square):
            if zz_classic_term[i][j] != 0:
                append_zz_term(qc, i, j, gamma, zz_classic_term[i][j])
    
    return qc
    
def get_mixer_operator(G,beta):
    
    N = G.number_of_nodes()
    qc = QuantumCircuit(N**2,N**2)
    
    for n in range(N**2):
        append_x_term(qc, n, beta)

    return qc

def get_QAOA_circuit(G, beta, gamma, _lambda):
    
    assert(len(beta)==len(gamma))
    
    N = G.number_of_nodes()
    qc = QuantumCircuit(N**2,N**2)
    # init min mix state
    qc.h(range(N**2))
    p = len(beta)
    
    for i in range(p):
        qc = qc.compose(get_cost_circuit(G, gamma[i], _lambda))
        qc = qc.compose(get_mixer_operator(G, beta[i]))
        qc.barrier(range(N**2))

    qc.snapshot_statevector("final_state")
    
    qc.measure(range(N**2),range(N**2))
    
    return qc
    

def invert_counts(counts):
    return {k[::-1] :v for k,v in counts.items()}

    # Sample expectation value
def compute_tsp_energy_2(counts, G):
    energy = 0
    get_counts = 0
    total_counts = 0
    for meas, meas_count in counts.items():
        obj_for_meas = tsp_obj_2(meas, G, LAMBDA)
        energy += obj_for_meas*meas_count
        total_counts += meas_count
    mean = energy/total_counts
    return mean


def get_black_box_objective_2(G,p):
    backend = Aer.get_backend('qasm_simulator')
    sim = Aer.get_backend('aer_simulator')
    # function f costo
    def f(theta):
        beta = theta[:p]
        gamma = theta[p:]
        # Anzats
        qc = get_QAOA_circuit(G, beta, gamma, LAMBDA)
        result = execute(qc, backend, seed_simulator=SEED, shots= SHOTS).result()
        final_state_vector = result.data()["snapshots"]["statevector"]["final_state"][0]
        
        state_vector = Statevector(final_state_vector)
        probabilities = state_vector.probabilities()
        probabilities_states = invert_counts(state_vector.probabilities_dict())
        expected_value = 0
        for state,probability in probabilities_states.items():
            cost = tsp_obj_2(state, G, LAMBDA)
            expected_value += cost*probability
        counts = result.get_counts()

        mean = compute_tsp_energy_2(invert_counts(counts),G)
        return mean
    return f

def crear_grafo(cantidad_ciudades):
    pesos, conexiones = None, None
    mejor_camino = None

    while not mejor_camino:
        pesos, conexiones = rand_graph(cantidad_ciudades)
        mejor_costo, mejor_camino = classical(pesos, conexiones, loop=False)

    G = mapeo_grafo(conexiones, pesos)
    return G, mejor_costo, mejor_camino

def run_QAOA(p,ciudades, grafo):

    if grafo == None:
        G, mejor_costo, mejor_camino = crear_grafo(ciudades)

        print("Mejor Costo")
        print(mejor_costo)
        print("Mejor Camino")
        print(mejor_camino)
        print("Bordes del grafo")
        print(G.edges())
        print("Nodos")
        print(G.nodes())
        print("Pesos")
        labels = nx.get_edge_attributes(G,'weight')
        print(labels)
    else:
        G = grafo
    
    intial_random = []

    # beta, mixer Hammiltonian
    for i in range(p):
        intial_random.append(np.random.uniform(0,np.pi))
    
    # gamma, cost Hammiltonian
    for i in range(p):
        intial_random.append(np.random.uniform(0,2*np.pi))

    init_point = np.array(intial_random)

    obj = get_black_box_objective_2(G,p)
    res_sample = minimize(obj, init_point,method="COBYLA",options={"maxiter":2500,"disp":True})
    
    print(res_sample)

if __name__ == '__main__':

    # Run QAOA parametros: profundidad p,  numero d ciudades, 
    run_QAOA(5, 3, None)
    
    
