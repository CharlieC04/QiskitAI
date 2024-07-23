import random
import pycosat
import numpy as np
from qiskit import QuantumCircuit, transpile, QuantumRegister
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt
import networkx as nx

from qiskit import QuantumCircuit as qc
from qiskit import QuantumRegister as qr
from heapq import nlargest
from matplotlib.pyplot import show, subplots, xticks, yticks

from qiskit import ClassicalRegister


def generate_complete_graph(clique_size):
    graph = [[1 if i != j else 0 for j in range(clique_size)] for i in range(clique_size)]
    return remove_random_edges(graph, clique_size)


def remove_random_edges(graph, clique_size):
    num_vertices = len(graph)
    max_edges = clique_size * (clique_size - 1) // 2
    edges_to_remove = random.sample(range(max_edges, num_vertices * (num_vertices - 1) // 2),
                                    k=num_vertices * (num_vertices - 1) // 2 - max_edges)

    for edge in edges_to_remove:
        row = edge // num_vertices
        col = edge % num_vertices
        graph[row][col] = 0
        graph[col][row] = 0

    return graph


def clique_max_sat(graph):
    num_vertices = len(graph)
    cnf_clauses = []

    # Constraint 1: There is an ith vertex
    for i in range(num_vertices):
        clique_clause = [j + 1 for j in range(num_vertices) if j != i]
        cnf_clauses.append(clique_clause)

    # Constraint 2: The ith and jth vertices are different
    for i in range(num_vertices):
        for j in range(i + 1, num_vertices):
            if graph[i][j] == 0:
                cnf_clauses.append([-1 * (i + 1), -1 * (j + 1)])

    return cnf_clauses



def solve(number_of_vertices, cnf_clauses):
    solution = pycosat.solve(cnf_clauses)
    if solution != "UNSAT":
        return [i for i in range(1, number_of_vertices + 1) if i in solution]
    return None


def amplify(num_of_qubits, num_sub_states):
    subsets = np.empty(num_sub_states, dtype=object)
    N = 2 ** num_of_qubits
    index = 0
    sup_index = (N // num_sub_states)

    if (N % num_sub_states != 0):
        k = 0
        for i in range(1, num_sub_states):
            sup = [0.] * N
            num_el = (N // num_sub_states) + 1
            sub_state = QuantumCircuit(num_of_qubits)

            for j in range(index, sup_index + 1):
                sup[j] = np.sqrt((N / num_el) / N)

            sub_state.initialize(sup, range(num_of_qubits))
            subsets[k] = sub_state
            index = index + (N // num_sub_states) + 1
            sup_index = sup_index + (N // num_sub_states) + 1
            k = k + 1

        sub_state = QuantumCircuit(num_of_qubits)
        sup = [0.] * N
        for j in range(index-1, sup_index):
            sup[j] = np.sqrt((N / num_el) / N)

        sub_state.initialize(sup, range(num_of_qubits))
        subsets[num_sub_states - 1] = sub_state

    else:
        k = 0
        for i in range(0, num_sub_states):
            sup = [0.] * N
            num_el = N / num_sub_states
            sub_state = QuantumCircuit(num_of_qubits)

            for j in range(index, sup_index):
                sup[j] = np.sqrt((N / num_el) / N)

            sub_state.initialize(sup, range(num_of_qubits))
            subsets[k] = sub_state

            index = index + (N // num_sub_states)
            sup_index = sup_index + (N // num_sub_states)
            k = k + 1
    return subsets




def n_controlled_Z(circuit, controls, target):
    if len(controls) == 1:
        circuit.h(target)
        circuit.cx(controls[0], target)
        circuit.h(target)
    elif len(controls) > 1:
        circuit.h(target)
        circuit.mcx(controls, target)
        circuit.h(target)
    else:
        raise ValueError("At least one control qubit is required for controlled-Z gate.")



def inversion_about_average(circuit, f_in, n):
    for j in range(n):
        circuit.h(f_in[j])
    for j in range(n):
        circuit.x(f_in[j])
    n_controlled_Z(circuit, [f_in[j] for j in range(n-1)], f_in[n-1])
    for j in range(n):
        circuit.x(f_in[j])
    for j in range(n):
        circuit.h(f_in[j])



def input_state(circuit, f_in, f_out, n):
    for j in range(n):
        circuit.h(f_in[j])
    circuit.x(f_out)
    circuit.h(f_out)



def oracle(circuit, f_in, f_out, aux, cnf_sat):

    num_clauses = len(cnf_sat)
    
    for (k, clause) in enumerate(cnf_sat):
        for literal in clause:
            if literal > 0:
                circuit.cx(f_in[literal-1], aux[k])
            else:
                circuit.x(f_in[-literal-1])
                circuit.cx(f_in[-literal-1], aux[k])
        
        circuit.ccx(f_in[0], f_in[1], aux[num_clauses])
        circuit.ccx(f_in[2], aux[num_clauses], aux[k])
        
        circuit.ccx(f_in[0], f_in[1], aux[num_clauses])
        for literal in clause:
            if literal < 0:
                circuit.x(f_in[-literal-1])
    
    if num_clauses > 0:
        circuit.mcx(aux[:-1], f_out[0])
    
    for (k, clause) in enumerate(cnf_sat):
        for literal in clause:
            if literal > 0:
                circuit.cx(f_in[literal-1], aux[k])
            else:
                circuit.x(f_in[-literal-1])
                circuit.cx(f_in[-literal-1], aux[k])
        
        circuit.ccx(f_in[0], f_in[1], aux[num_clauses])
        circuit.ccx(f_in[2], aux[num_clauses], aux[k])
        circuit.ccx(f_in[0], f_in[1], aux[num_clauses])
        
        for literal in clause:
            if literal < 0:
                circuit.x(f_in[-literal-1])



if __name__ == '__main__':

    graph = generate_complete_graph(3)

    G = nx.Graph()
    for i in range(len(graph)):
        for j in range(i + 1, len(graph)):
            if graph[i][j] == 1:
                G.add_edge(i, j)


    plt.figure(figsize=(6, 6))
    nx.draw(G, with_labels=True, font_weight='bold')
    plt.title('Grafo Gerado')
    plt.show()

    
    cnf_clauses = clique_max_sat(graph)
    for clause in cnf_clauses:
        print(clause)

    print(cnf_clauses)

    max_clique = solve(len(graph), cnf_clauses)
    print("Clique máximo :", max_clique)

    num_qubits = 3
    num_sub_states = 2
    subsets = amplify(num_qubits, num_sub_states) 

    #cnf_clauses = [[1, 2, 3], [-1, -2, -3], [-1, -2, -3]]
    #cnf_clauses = [[1, 2, -3], [-1, -2, -3], [-1, 2, 3]]
    #cnf_clauses = [[1, -2, -3, -4], [-1, 2, -3, -4], [-1, -2, 3, -4], [-1, -2, -3, 4]]
    #cnf_clauses = [[-1, -2, -3, -4], [-1, -2, -3, -4], [-1, -2, -3, -4], [-1, -2, -3, -4]]

    f_in = QuantumRegister(num_qubits)
    f_out = QuantumRegister(1)
    aux = QuantumRegister(len(cnf_clauses) + 1)
    ans = ClassicalRegister(num_qubits)

    grover = QuantumCircuit()

    grover.add_register(f_in)
    grover.add_register(f_out)
    grover.add_register(aux)
    grover.add_register(ans)

    #print(grover)

    #substate_circuit = QuantumCircuit(num_qubits)
    #substate_circuit.initialize(subsets[0], range(num_qubits))
    #grover = grover.compose(substate_circuit)

    input_state(grover, f_in, f_out, num_qubits)
    grover = grover.compose(subsets[0])

    #print(grover)
    #input_state(grover, f_in, f_out, num_qubits)
    #print(grover)


    T = 2
    for t in range(T):
        oracle(grover, f_in, f_out, aux, cnf_clauses)
        inversion_about_average(grover, f_in, num_qubits)


    for j in range(num_qubits):
        grover.measure(f_in[j], ans[j])

    #print(grover)

    backend = AerSimulator()
    new_circuit = transpile(grover, backend)
    result = backend.run(new_circuit).result()
    counts = result.get_counts(grover)
    print("Counts:", counts)

    plot_histogram(counts)
    plt.show()
