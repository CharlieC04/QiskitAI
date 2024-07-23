
from thirdParty.classical import rand_graph, classical, bitstring_to_path, calc_cost
from utils import mapeo_grafo

import qiskit
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict
from operator import itemgetter
from scipy.optimize import minimize
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, execute, Aer, assemble
from qiskit.quantum_info import Statevector
from qiskit.aqua.algorithms import NumPyEigensolver
from qiskit.quantum_info import Pauli
from qiskit.aqua.operators import op_converter
from qiskit.aqua.operators import WeightedPauliOperator
from qiskit.visualization import plot_histogram
from qiskit.providers.aer.extensions.snapshot_statevector import *
import json
import csv


# Gloabal _lambda variable
_LAMBDA = 10
_SHOTS = 10000
_UNIFORM_CONVERGENCE_SAMPLE = []


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

def invert_counts(counts):
    return {k[::-1] :v for k,v in counts.items()}

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

def tsp_obj(x, G):
    # obtenemos el valor evaluado en f(x_1, x_2,... x_n)
    z_classic_term, zz_classic_term = get_classical_simplified_hamiltonian(G, _LAMBDA)
    cost = 0

    # z term 
    for index in range(len(x)):
        z = (int(x[index]) * 2 ) -1
        cost += z_classic_term[index] * z

    ## zz term
    for i in range(len(x)):
        z_1 = (int(x[i]) * 2 ) -1
        for j in range(len(x)):
            z_2 = (int(x[j]) * 2 ) -1
            cost += zz_classic_term[i][j] * z_1 * z_1
    
    return cost


# Sample expectation value
def compute_tsp_energy(counts, G):
    energy = 0
    get_counts = 0
    total_counts = 0
    for meas, meas_count in counts.items():
        obj_for_meas = tsp_obj(meas, G)
        energy += obj_for_meas*meas_count
        total_counts += meas_count
    return energy/total_counts

# Sample expectation value
def compute_tsp_energy_2(counts, G):
    energy = 0
    get_counts = 0
    total_counts = 0
    for meas, meas_count in counts.items():
        obj_for_meas = tsp_obj_2(meas, G, _LAMBDA)
        energy += obj_for_meas*meas_count
        total_counts += meas_count
    mean = energy/total_counts
    return mean

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

def get_black_box_objective(G,p):
    backend = Aer.get_backend('qasm_simulator')
    def f(theta):
        beta = theta[:p]
        gamma = theta[p:]
        _lambda = _LAMBDA # get global _lambda 
        qc = get_QAOA_circuit(G, beta, gamma, _LAMBDA)
        counts = execute(qc, backend, seed_simulator=10, shots=_SHOTS).result().get_counts()
        return compute_tsp_energy(invert_counts(counts),G)
    return f

def get_black_box_objective_2(G,p):
    backend = Aer.get_backend('qasm_simulator')
    sim = Aer.get_backend('aer_simulator')
    def f(theta):
        beta = theta[:p]
        gamma = theta[p:]
        #print(beta)
        _lambda = _LAMBDA # get global _lambda 
        qc = get_QAOA_circuit(G, beta, gamma, _LAMBDA)
        #print(beta)
        result = execute(qc, backend, seed_simulator=10, shots=_SHOTS).result()
        
        final_state_vector = result.data()["snapshots"]["statevector"]["final_state"][0]
        
        state_vector = Statevector(final_state_vector)
        probabilities = state_vector.probabilities()
        # expected value
        #print("prob-dict")
        #print(state_vector.probabilities_dict())
        probabilities_states = invert_counts(state_vector.probabilities_dict())
        expected_value = 0
        for state,probability in probabilities_states.items():
            # get cost from state
            cost = tsp_obj_2(state, G, _LAMBDA)
            expected_value += cost*probability

        
        #print(probabilities)
        
        counts = result.get_counts()

        #qc.save_statevector()   # Tell simulator to save statevector
        #qobj = assemble(qc)     # Create a Qobj from the circuit for the simulator to run
        #state_vector = sim.run(qobj).result().get_statevector()
        #state_vector = Statevector(state_vector)
        #probabilities = state_vector.probabilities()

        mean = compute_tsp_energy_2(invert_counts(counts),G)
        global _UNIFORM_CONVERGENCE_SAMPLE
        _UNIFORM_CONVERGENCE_SAMPLE.append({
            "beta" : beta,
            "gamma" : gamma,
            "counts" : counts,
            "mean" : mean,
            "probabilities" : probabilities,
            "expected_value" : expected_value
        })
        return mean
    return f


def compute_tsp_min_energy_2(counts, G):
    energy = 0
    get_counts = 0
    total_counts = 0
    min = 1000000000000000000000
    index = 0
    min_meas = "" 
    for meas, meas_count in counts.items():
        index = index + 1
        obj_for_meas = tsp_obj_2(meas, G, _LAMBDA)
        if obj_for_meas < min:
            min = obj_for_meas
            min_meas = meas
    return index, min, min_meas

def compute_tsp_min_energy_1(counts, G):
    energy = 0
    get_counts = 0
    total_counts = 0
    min = 1000000000000000000000
    index = 0
    min_meas = "" 
    for meas, meas_count in counts.items():
        index = index + 1
        obj_for_meas = tsp_obj(meas, G)
        if obj_for_meas < min:
            min = obj_for_meas
            min_meas = meas
    return index, min, min_meas

def test_counts_2(counts, G):
    mean_energy2  = compute_tsp_energy_2(invert_counts(counts),G)
    cantidad, min, min_meas = compute_tsp_min_energy_2(invert_counts(counts),G)
    print("*************************")
    print("En el algoritmo 2 (Marina) el valor esperado como resultado es " + str(mean_energy2))
    print("El valor minimo de todos los evaluados es " + str(min) + " se evaluaron un total de " + str(cantidad))
    print("El vector minimo es " + min_meas)


def test_counts_1(counts, G):
    mean_energy1  = compute_tsp_energy(invert_counts(counts),G)
    cantidad, min, min_meas = compute_tsp_min_energy_1(invert_counts(counts),G)
    print("*************************")
    print("En el algoritmo 1 (Pablo) el valor esperado como resultado es " + str(mean_energy1))
    print("El valor minimo de todos los evaluados es " + str(min) + " se evaluaron un total de " + str(cantidad))
    print("El vector minimo es " + min_meas)

def test_solution(grafo=None, p=7):
    global _UNIFORM_CONVERGENCE_SAMPLE
    _UNIFORM_CONVERGENCE_SAMPLE = []
    if grafo == None:
        cantidad_ciudades = 2
        pesos, conexiones = None, None
        mejor_camino = None

        while not mejor_camino:
            pesos, conexiones = rand_graph(cantidad_ciudades)
            mejor_costo, mejor_camino = classical(pesos, conexiones, loop=False)
        
        G = mapeo_grafo(conexiones, pesos)
        print(mejor_costo)
        print(mejor_camino)
        print(G.edges())
        print(G.nodes())
    else:
        G = grafo
    # beta [0,pi], gamma [0, 2pi]
   
    # create bounds for beta [0,pi]
    bounds = []
    intial_random = []

    for i in range(p):
        bounds.append((0, np.pi))
        intial_random.append(np.random.uniform(0,np.pi))

    # create bounds for gamma [0,2*pi]
    for i in range(p):
        bounds.append((0, np.pi * 2))
        intial_random.append(np.random.uniform(0,2*np.pi))

    init_point = np.array(intial_random)

    # Pablo Solutions
    #obj = get_black_box_objective(G,p)
    
    #res_sample_1 = minimize(obj, init_point,method="COBYLA",options={"maxiter":2500,"disp":True})
    #print(res_sample_1)

    # Marina Solutions

    obj = get_black_box_objective_2(G,p)
    res_sample_2 = minimize(obj, init_point, method="COBYLA", options={"maxiter":2500,"disp":True})
    print(res_sample_2)

    #theta_1 = res_sample_1.x
    theta_2 = res_sample_2.x
    
    #beta = theta_1[:p]
    #gamma = theta_1[p:]
    #_lambda = _LAMBDA # get global _lambda 
    #qc = get_QAOA_circuit(G, beta, gamma, _LAMBDA)
    #backend = Aer.get_backend('qasm_simulator')
    #job_1 = execute(qc, backend, shots=_SHOTS)
    #resutls_1 = job_1.result().get_counts()
    #test_counts_1(resutls_1, G)

    beta = theta_2[:p]
    gamma = theta_2[p:]
    _lambda = _LAMBDA # get global _lambda 
    qc = get_QAOA_circuit(G, beta, gamma, _LAMBDA)
    backend = Aer.get_backend('qasm_simulator')
    job_2 = execute(qc, backend, shots=_SHOTS)
    resutls_2 = job_2.result().get_counts()
    test_counts_2(resutls_2, G)
    #print( _UNIFORM_CONVERGENCE_SAMPLE)
    return job_2, G, _UNIFORM_CONVERGENCE_SAMPLE
    
def create_multiple_p_mismo_grafo():
    header = ['p', 'state', 'probability', 'mean']
    length_p = 10
    with open('qaoa_multiple_p.csv', 'w', encoding='UTF8') as f:
        writer = csv.writer(f)
        # write the header
        writer.writerow(header)
        first_p = False
        UNIFORM_CONVERGENCE_SAMPLE = []

        for p in range(length_p):
            p = p+1
            if first_p == False:
                job_2, G, UNIFORM_CONVERGENCE_SAMPLE = test_solution(p=p)
                first_p = True
            else:
                job_2, G, UNIFORM_CONVERGENCE_SAMPLE = test_solution(grafo=G, p=p)
                
            # Sort the JSON data based on the value of the brand key
            UNIFORM_CONVERGENCE_SAMPLE.sort(key=lambda x: x["mean"])


            mean = UNIFORM_CONVERGENCE_SAMPLE[0]["mean"]
            print(mean)
            state = 0
            for probability in UNIFORM_CONVERGENCE_SAMPLE[0]["probabilities"]:
                state += 1
                writer.writerow([p,state, probability,mean])

def create_multiple_p_mismo_grafo_multiples_instanncias():
    header = ['instance','p','distance', 'mean']
    length_p = 4
    length_instances = 10
    with open('qaoa_multiple_p_distance.csv', 'w', encoding='UTF8') as f:
        writer = csv.writer(f)
        # write the header
        writer.writerow(header)
        instance_index = 0
        for instance in range(length_instances):
            instance_index += 1
            first_p = False
            UNIFORM_CONVERGENCE_P = []
            UNIFORM_CONVERGENCE_SAMPLE = []
            for p in range(length_p):
                p = p+1
                print("p es igual  " + str(p))
                if first_p == False:
                    print("Vuelve a llamar a test_solution")
                    job_2, G, UNIFORM_CONVERGENCE_SAMPLE = test_solution(p=p)
                    first_p = True
                else:
                    job_2, G, UNIFORM_CONVERGENCE_SAMPLE = test_solution(grafo=G, p=p)

                # Sort the JSON data based on the value of the brand key
                UNIFORM_CONVERGENCE_SAMPLE.sort(key=lambda x: x["expected_value"])
                convergence_min = UNIFORM_CONVERGENCE_SAMPLE[0]
                UNIFORM_CONVERGENCE_P.append({
                    "mean":convergence_min["expected_value"],
                    "probabilities": convergence_min["probabilities"]
                })
                print("expected value min con p =" + str(p) + " : " + str(convergence_min["expected_value"]))
            
            cauchy_function_nk = UNIFORM_CONVERGENCE_P[len(UNIFORM_CONVERGENCE_P) - 1]
            p_index = 0
            for p_state in UNIFORM_CONVERGENCE_P:
                p_index += 1
                print(p_index)
                mean = p_state["mean"]
                #print(p_state)
                print("expected value min")
                print(mean)
                distance_p_cauchy_function_nk = np.max(np.abs(cauchy_function_nk["probabilities"] - p_state["probabilities"]))
                writer.writerow([instance_index, p_index, distance_p_cauchy_function_nk, mean])
            
        
    
    
        
if __name__ == '__main__':
    #create_multiple_p_mismo_grafo()
    create_multiple_p_mismo_grafo_multiples_instanncias()

def defult_init():
    cantidad_ciudades = 2
    pesos, conexiones = None, None
    mejor_camino = None

    while not mejor_camino:
        pesos, conexiones = rand_graph(cantidad_ciudades)
        mejor_costo, mejor_camino = classical(pesos, conexiones, loop=False)

    G = mapeo_grafo(conexiones, pesos)

    print(mejor_costo)
    print(mejor_camino)
    print(G.edges())
    print(G.nodes())
    print("labels")
    labels = nx.get_edge_attributes(G,'weight')

    #z_term, zz_term = get_classical_simplified_hamiltonian(G, 1)
    
    #print("z term")
    #print(z_term)
    #print("*****************")
    #print("zz term")
    #print(zz_term)

    #print(get_QAOA_circuit(G, beta = [2,3], gamma = [4,5], _lambda = 1))

    p = 5
    obj = get_black_box_objective(G,p)
    init_point = np.array([0.8,2.2,0.83,2.15,0.37,2.4,6.1,2.2,3.8,6.1])
    #res_sample = minimize(obj, init_point,method="COBYLA",options={"maxiter":2500,"disp":True})
    #print(res_sample)

    # Marina Solutions
    obj = get_black_box_objective_2(G,p)
    res_sample = minimize(obj, init_point,method="COBYLA",options={"maxiter":2500,"disp":True})
    print(res_sample)

    theta_2 = [0.72685401, 2.15678239, 0.86389827, 2.19403121, 0.26916675, 2.19832144, 7.06651453, 3.20333137, 3.81301611, 6.08893568]
    theta_1 = [0.90644898, 2.15994212, 1.8609325 , 2.14042604, 1.49126214, 2.4127999, 6.10529434, 2.18238732, 3.84056674, 6.07097744]

    beta = theta_1[:p]
    gamma = theta_1[p:]
    _lambda = _LAMBDA # get global _lambda 
    qc = get_QAOA_circuit(G, beta, gamma, _LAMBDA)
    backend = Aer.get_backend('qasm_simulator')
    job = execute(qc, backend)
    print(plot_histogram(job.result().get_counts(), color='midnightblue', title="New Histogram"))


    beta = theta_2[:p]
    gamma = theta_2[p:]
    _lambda = _LAMBDA # get global _lambda 
    qc = get_QAOA_circuit(G, beta, gamma, _LAMBDA)
    backend = Aer.get_backend('qasm_simulator')
    job = execute(qc, backend)
    print(plot_histogram(job.result().get_counts(), color='midnightblue', title="New Histogram"))

    
