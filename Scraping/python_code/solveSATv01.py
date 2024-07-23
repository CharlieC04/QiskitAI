
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
from qiskit.result import Counts
from heapq import nlargest
from matplotlib.pyplot import show, subplots, xticks, yticks
from matplotlib.backend_bases import MouseEvent


N: int = 3                          # Number of qubits
SEARCH_VALUES: set[int] = { 0,1,3 } # Set of m nonnegative integers to search for using Grover's algorithm (i.e. TARGETS in base 10)
SHOTS: int = 1024                   # Amount of times the algorithm is simulated
FONTSIZE: int = 10                  # Histogram's font size
TARGETS: set[str] = { f"{s:0{N}b}" for s in SEARCH_VALUES }     # Set of m N-qubit binary strings representing target state(s) (i.e. SEARCH_VALUES in base 2)
QUBITS: qr = qr(N, "qubit")  



def print_circuit(circuit: qc, name: str = ""):
    print(f"\n{name}:" if name else "")
    print(f"{circuit}")


def outcome(winners: list[str], counts: Counts):
    print("WINNER(S):")
    print(f"Binary = {winners}\nDecimal = {[ int(key, 2) for key in winners ]}\n")
        
    print("TARGET(S):")
    print(f"Binary = {TARGETS}\nDecimal = {SEARCH_VALUES}\n")

    winners_frequency, total = 0, 0

    for value, frequency in counts.items():
        if value in winners:
            winners_frequency += frequency
        total += frequency
    
    print(f"Target(s) found with {winners_frequency / total:.2%} accuracy!")



def display_results(results: Counts, combine_other_states: bool = True):
    # State(s) with highest count and their frequencies
    winners = { winner : results.get(winner) for winner in nlargest(len(TARGETS), results, key = results.get) }

    # Print outcome
    outcome(list(winners.keys()), results)

    # X-axis and y-axis value(s) for winners, respectively
    winners_x_axis = [ str(winner) for winner in [*winners] ]
    winners_y_axis = [ *winners.values() ]

    # All other states (i.e. non-winners) and their frequencies
    others = {state : frequency for state, frequency in results.items() if state not in winners}

    # X-axis and y-axis value(s) for all other states, respectively
    other_states_x_axis = "Others" if combine_other_states else [*others]
    other_states_y_axis = [ sum([*others.values()]) ] if combine_other_states else [ *others.values() ]

    # Create histogram for simulation results
    figure, axes = subplots(num = "Grover's Algorithm — Results", layout = "constrained")
    axes.bar(winners_x_axis, winners_y_axis, color = "green", label = "Target")
    axes.bar(other_states_x_axis, other_states_y_axis, color = "red", label = "Non-target")
    axes.legend(fontsize = FONTSIZE)
    axes.grid(axis = "y", ls = "dashed")
    axes.set_axisbelow(True)

    # Set histogram title, x-axis title, and y-axis title respectively
    axes.set_title(f"Outcome of {SHOTS} Simulations", fontsize = int(FONTSIZE * 1.45))
    axes.set_xlabel("States (Qubits)", fontsize = int(FONTSIZE * 1.3))
    axes.set_ylabel("Frequency", fontsize = int(FONTSIZE * 1.3))

    # Set font properties for x-axis and y-axis labels respectively
    xticks(fontsize = FONTSIZE, family = "monospace", rotation = 0 if combine_other_states else 70)
    yticks(fontsize = FONTSIZE, family = "monospace")
    
    # Set properties for annotations displaying frequency above each bar
    annotation = axes.annotate("",
                               xy = (0, 0),
                               xytext = (5, 5),
                               xycoords = "data",
                               textcoords = "offset pixels",
                               ha = "center",
                               va = "bottom",
                               family = "monospace",
                               weight = "bold",
                               fontsize = FONTSIZE,
                               bbox = dict(facecolor = "white", alpha = 0.4, edgecolor = "None", pad = 0)
                               )
    
    def hover(event: MouseEvent):
        visibility = annotation.get_visible()
        if event.inaxes == axes:
            for bars in axes.containers:
                for bar in bars:
                    cont, _ = bar.contains(event)
                    if cont:
                        x, y = bar.get_x() + bar.get_width() / 2, bar.get_y() + bar.get_height()
                        annotation.xy = (x, y)
                        annotation.set_text(y)
                        annotation.set_visible(True)
                        figure.canvas.draw_idle()
                        return
        if visibility:
            annotation.set_visible(False)
            figure.canvas.draw_idle()
        
    # Display histogram
    id = figure.canvas.mpl_connect("motion_notify_event", hover)
    show()
    figure.canvas.mpl_disconnect(id)




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

            for j in range(index, sup_index + 1):
                sup[j] = np.sqrt((N / num_el) / N)

            subsets[k] = sup
            index = index + (N // num_sub_states) + 1
            sup_index = sup_index + (N // num_sub_states) + 1
            k = k + 1

        sup = [0.] * N
        for j in range(len(sup)):
            sup[j] = np.sqrt((N / num_el) / N)

        subsets[num_sub_states - 1] = sup

    else:
        k = 0
        for i in range(0, num_sub_states):
            sup = [0.] * N
            num_el = N / num_sub_states

            for j in range(index, sup_index):
                sup[j] = np.sqrt((N / num_el) / N)

            subsets[k] = sup
            index = index + (N // num_sub_states)
            sup_index = sup_index + (N // num_sub_states)
            k = k + 1
    return subsets




def oracle_circuit(sat, num_qubits, subsets, targets: set[str] = TARGETS, name: str = "Oracle", display_oracle: bool = True):
    # oracle = QuantumCircuit(num_qubits + 1, name=name)

    # for target in targets:
    #     # Reverse target state since Qiskit uses little-endian for qubit ordering
    #     target = target[::-1]
        
    #     # Flip zero qubits in target
    #     for i in range(num_qubits):
    #         if target[i] == "0":
    #             oracle.x(i)                            # Pauli-X gate

    #     # Simulate (N - 1)-control Z gate
    #     oracle.h(num_qubits - 1)                       # Hadamard gate
    #     oracle.mcx(list(range(num_qubits - 1)), num_qubits - 1) # (N - 1)-control Toffoli gate
    #     oracle.h(num_qubits - 1)                       # Hadamard gate

    #     # Flip back to original state
    #     for i in range(num_qubits):
    #         if target[i] == "0":
    #             oracle.x(i)    

    # if display_oracle: print_circuit(oracle, "ORACLE")

    # return oracle                
                

    for clause in sat:
        oracle = QuantumCircuit(num_qubits+1)
        for literal in clause:
            if literal > 0:
                #oracle.x(literal-1)
                oracle.h(num_qubits - 1)

        oracle.mcx(list(range(num_qubits - 1)), num_qubits - 1)

        for literal in clause:
            if literal > 0:
                #oracle.x(literal-1)
                oracle.h(num_qubits - 1)

        #oracle.append(oracle.to_gate().control(num_qubits+1), list(range(num_qubits+1)))               

    if display_oracle: print_circuit(oracle, "ORACLE")

    return oracle


    #using subsets
    # qc = QuantumCircuit(num_qubits + 1)
    # for i, subset in enumerate(subsets):
    #     for j, amplitude in enumerate(subset):
    #         if j < num_qubits:
    #             #qc.ry(2 * amplitude, j)
    #             qc.h(num_qubits - 1)
    #     #qc.mcp(2 * np.pi, list(range(num_qubits)), num_qubits)
    #     qc.mcx(list(range(num_qubits - 1)), num_qubits - 1)
    #     for j, amplitude in enumerate(subset):
    #         if j < num_qubits:
    #             #qc.ry(-2 * amplitude, j)
    #             qc.h(num_qubits - 1)
    # return qc



def diffusion_circuit(num_qubits, name: str = "Diffuser", display_diffuser: bool = True):
    qc = QuantumCircuit(num_qubits, name = name)
    
    for qubit in range(num_qubits):
        qc.h(qubit)
    for qubit in range(num_qubits):
        qc.x(qubit)
    qc.h(num_qubits - 1)
    qc.mcp(np.pi, list(range(num_qubits - 1)), num_qubits - 1)
    qc.h(num_qubits - 1)
    for qubit in range(num_qubits):
        qc.x(qubit)
    for qubit in range(num_qubits):
        qc.h(qubit)

    if display_diffuser: print_circuit(qc, "DIFFUSER")

    return qc


def grover_algorithm(oracle, diffusion, num_iterations, name: str = "Grover Circuit", display_grover: bool = True):
    num_qubits = oracle.num_qubits - 1
    qc = QuantumCircuit(num_qubits + 1, num_qubits, name = name)
    for qubit in range(num_qubits):
        qc.h(qubit)
    qc.x(num_qubits)
    qc.h(num_qubits)
    for _ in range(num_iterations):
        qc.append(oracle.to_gate(), range(num_qubits + 1))
        qc.append(diffusion.to_gate(), range(num_qubits))
    qc.measure(range(num_qubits), range(num_qubits))

    if display_grover: print_circuit(qc, "GROVER CIRCUIT")
    
    return qc


def map_solution(qubit_configurations, clique_size):
    # Mapeia as configurações dos qubits de volta para as soluções do problema original (clique máximo)
    solutions = []
    for config in qubit_configurations:
        solution = [i for i, bit in enumerate(config) if bit == '1']
        if len(solution) == clique_size:  # Apenas considera as soluções que têm o tamanho correto da clique
            solutions.append(solution)
    return solutions


if __name__ == '__main__':
    k = N
    graph = [
        [0, 1, 0, 1],
        [1, 0, 1, 1],
        [0, 1, 0, 0],
        [1, 1, 0, 0]
    ]

    #print(graph)
    #graph = generate_complete_graph(k)
    #print(graph)


    # Plotar o grafo gerado
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
    print("Fórmula SAT gerada:")
    for clause in cnf_clauses:
        print(clause)

    max_clique = solve(len(graph), cnf_clauses)
    print("Clique máximo encontrado pelo solve:", max_clique)


    if max_clique:
        print("Maximal-Clique problem found:", [x - 1 for x in max_clique])
    else:
        print("It's not possible to find maximal-clique problem!")

    
    num_qubits = N  # Número de qubits necessário para representar a fórmula SAT
    num_sub_states = 2 # Número de subestados para dividir o espaço SAT
    subsets = amplify(num_qubits, num_sub_states) # Aplicar amplify para otimização da busca

    oracle = oracle_circuit(cnf_clauses, num_qubits, subsets)
    diffusion = diffusion_circuit(num_qubits)
    grover_circuit = grover_algorithm(oracle, diffusion, SHOTS)

    backend = AerSimulator()
    new_circuit = transpile(grover_circuit, backend)
    result = backend.run(new_circuit).result()
    counts = result.get_counts(grover_circuit)
    print("Counts:", counts)

    solutions = map_solution(counts.keys(), len(max_clique))
    print("Solutions found:", solutions)

    plot_histogram(counts)
    plt.show()

    display_results(counts, False)
                                                                                                                                        

