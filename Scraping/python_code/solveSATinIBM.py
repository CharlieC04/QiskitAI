


import math
import random
import matplotlib.pyplot as plt

def is_edge(graph, u, v):
    return u in graph[v] or v in graph[u]

def generate_clauses(graph, k):
    n = len(graph)
    clauses = []
    
    # Cláusulas para garantir que k vértices são selecionados
    for i in range(1, k+1):
        clauses.append([j + n * (i - 1) for j in range(1, n+1)])
    
    # Cláusulas para garantir que não há dois vértices no mesmo slot
    for i in range(1, k+1):
        for u in range(1, n+1):
            for v in range(u + 1, n+1):
                clauses.append([-(u + n * (i - 1)), -(v + n * (i - 1))])
    
    # Cláusulas para garantir que todos os pares de vértices no clique são adjacentes
    for i in range(1, k):
        for j in range(i+1, k+1):
            for u in range(1, n+1):
                for v in range(1, n+1):
                    if not is_edge(graph, u-1, v-1):
                        clauses.append([-(u + n * (i - 1)), -(v + n * (j - 1))])

    return clauses

if __name__ == '__main__':
    graph = {
        0: [1, 2, 3, 4],
        1: [0, 2, 3, 4],
        2: [0, 1, 3, 4],
        3: [0, 1, 2, 4],
        4: [0, 1, 2, 3],
    }  

    

    K = 5
    cnf_clauses = generate_clauses(graph, K)
    print(cnf_clauses)

    print("***************")

    expression = ''
    for i, clause in enumerate(cnf_clauses):
        if i > 0:
            expression += ' & '
        expression += '(' + ' | '.join(['x' + str(x) if x > 0 else '~x' + str(abs(x)) for x in clause]) + ')'
    print(expression)

    # Apply "optimized" Grover 
    from qiskit.circuit.library import PhaseOracle
    from qiskit.primitives import Sampler
    from qiskit.visualization import plot_histogram
    from qiskit_algorithms import AmplificationProblem, Grover

    from qiskit import *

    from qiskit_ibm_provider import IBMProvider

    provider = IBMProvider(token='8f69cea4cf33304753bfe092aacdf58174e59f8e9813d9305e21c248e3bbb19b98b8508540e15ad4959f3a585675058da81276c3871dce532772da60b370566b')
    backend = provider.get_backend('ibm_kyoto')

    iteracoes = 3

    oracle = PhaseOracle(expression)
    problem = AmplificationProblem(oracle)
    grover = Grover(sampler=Sampler(), iterations=iteracoes)

    #results = grover.amplify(problem)


    # Construir o circuito do Grover
    qc = grover.construct_circuit(problem, iteracoes, True)
    
    # Transpilar o circuito para o backend
    transpiled_qc = transpile(qc, backend=backend)

    print("Starting ........................")

    # Executar o circuito no backend
    job = backend.run(transpiled_qc, shots=1024)
    

    result = job.result()
    counts = result.get_counts()

    # Análise dos resultados
    top_measurement = max(counts, key=counts.get)
    max_probability = counts[top_measurement] / 1024
    oracle_evaluation = 'True' if max_probability > 0 else 'False'


    print('É Satisfatível?', oracle_evaluation)
    print('Estado amplificado', top_measurement)
    print('Probabilidade estado amplificado', max_probability)
    print('Iterações máximas', iteracoes)
    print('Width', problem.grover_operator.decompose().width())
    print('Depth', problem.grover_operator.decompose().depth())

    # Gerar somente resultados relevantes
    output = {}
    for x in counts:
        value = counts[x] / 1024
        if value >= max_probability - max_probability * 0.05:
            output[x] = value
            print(f"estado_amplificado: {x} probabilidade {value}")

    # Ordenar o output por probabilidade
    sorted_output = dict(sorted(output.items(), key=lambda item: item[1], reverse=True))

    # Plotar o histograma
    plt.bar(sorted_output.keys(), sorted_output.values(), width=0.5)
    plt.xticks(fontsize=8, rotation=45)
    plt.xlabel('States')
    plt.ylabel('Probability')
    plt.title('Histogram of Amplified States')
    plt.ylim(0, max(sorted_output.values()) * 1.1)  # Ajustar o limite superior do eixo y

    # Adicionar as probabilidades sobre as barras
    for i, (state, probability) in enumerate(sorted_output.items()):
        plt.text(i, probability, f'{probability:.2f}', ha='center', va='bottom', fontsize=8)

    plt.show()
    #input()

