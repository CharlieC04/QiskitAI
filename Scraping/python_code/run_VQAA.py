import matplotlib.pyplot
import math
import random
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from pathlib import Path

from qiskit import Aer, transpile, assemble, BasicAer, transpiler
from qiskit.providers.aer import Aer
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit.circuit.library import QFT, PhaseGate
from random import uniform
from qiskit.providers.aer.library import save_statevector
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister, execute
from qiskit.providers.aer.noise.errors import thermal_relaxation_error, pauli_error
from qiskit.providers.aer.noise import NoiseModel

# GRAPH = nx.random_graphs.random_regular_graph(DEGREE, AES_KEY_LENGTH)

error_list = {
    "1qb" : -1,
    "2qb" : -1,
    "spam": -1,
    "thermal" : [5000,6000]
}
pauli_Z = np.array([[1, 0], [0, -1]])

def is_noisy(error_type):
    random_noise = uniform(0.0, 1.0)
    if error_type == "1qb" or error_type == "2qb":
        if random_noise <= error_list[error_type]:
            different_gate_noise = uniform(0.0, 1.0)
            if 0.0 <= different_gate_noise < 1/3:
                return "X"
            elif 1/3 <= random_noise < 2/3:
                return "Y"
            else:
                return "Z"
        else:
            return False
    else:
        if random_noise <= error_list[error_type]:
            return True
        else:
            return False
def generate_circuit_with_state_vector(ansatz_type, if_back_control, plain_text, theta_list):
    n = len(plain_text)
    key_space = QuantumRegister(n)
    data_space = QuantumRegister(n)
    qc = QuantumCircuit(key_space, data_space)

    ## Begin ansatz
    qc.h(key_space)
    ### 1-qubit gate noise
    for i in range(n):
        if_noisy = is_noisy("1qb")
        if if_noisy == False:
            continue
        else:
            if if_noisy == "X":
                qc.x(key_space[i])
            elif if_noisy == "Y":
                qc.y(key_space[i])
            else:
                qc.z(key_space[i])


    for i in range(n):
        qc.ry(theta_list[i], key_space[i])
        # 1-qubit gate noise
        if_noisy = is_noisy("1qb")
        if if_noisy == False:
            continue
        else:
            if if_noisy == "X":
                qc.x(key_space[i])
            elif if_noisy == "Y":
                qc.y(key_space[i])
            else:
                qc.z(key_space[i])
    qc.barrier()

    if ansatz_type == "rx":
        for i in range(n - 1):
            qc.cx(key_space[i], key_space[i+1])
    elif ansatz_type == "ry":
        for i in range(n - 1):
            qc.cy(key_space[i], key_space[i+1])
    elif ansatz_type == "rz":
        for i in range(n - 1):
            qc.cz(key_space[i], key_space[i+1])
    # 2-qubit gate noise
    for i in range(n - 1):
        if_noisy = is_noisy("2qb")
        if if_noisy == False:
            continue
        else:
            if if_noisy == "X":
                qc.x(key_space[i + 1])
            elif if_noisy == "Y":
                qc.y(key_space[i + 1])
            else:
                qc.z(key_space[i + 1])


    if if_back_control:
        if ansatz_type == "rx":
            qc.cx(key_space[n - 1], key_space[0])
        elif ansatz_type == "ry":
            qc.cy(key_space[n - 1], key_space[0])
        elif ansatz_type == "rz":
            qc.cz(key_space[n - 1], key_space[0])

        # 2-qubit gate noise
        if_noisy = is_noisy("2qb")
        if if_noisy != False:
            if if_noisy == "X":
                qc.x(key_space[0])
            elif if_noisy == "Y":
                qc.y(key_space[0])
            else:
                qc.z(key_space[0])
    qc.barrier()
    ## End ansatz

    ## Prepare plaintext
    for i in range(n):
        if plain_text[i] == '1':
            qc.x(data_space[i])
            # 1-qubit gate noise
            if_noisy = is_noisy("1qb")
            if if_noisy != False:
                if if_noisy == "X":
                    qc.x(data_space[i])
                elif if_noisy == "Y":
                    qc.y(data_space[i])
                else:
                    qc.z(data_space[i])
    qc.barrier()

    ## Begin AES encryption
    for i in range(n // 2):
        qc.swap(data_space[i], data_space[n - 1 - i])
    qc.barrier()
    for i in range(n):
        qc.cx(key_space[i], data_space[i])
        #2-qubit gate noise
        if_noisy = is_noisy("2qb")
        if if_noisy == False:
            continue
        else:
            if if_noisy == "X":
                qc.x(data_space[i])
            elif if_noisy == "Y":
                qc.y(data_space[i])
            else:
                qc.z(data_space[i])

    qc.barrier()
    ## End AES encryption

    ## spam error
    for i in range(n):
        if_noisy = is_noisy("spam")
        if if_noisy == False:
            continue
        else:
            qc.x(data_space[i])
    qc.save_statevector(label="final")
    # qc.measure(data_space, classic_reg)
    return qc

def get_thermal_error(num_qubits):
    t1 = error_list["thermal"][0]
    t2 = error_list["thermal"][1]

    # nanosecond
    time_u1 = 50
    time_x = 10
    time_h = 10
    time_cx = 10
    time_cu1 = 10
    time_measure = 1000 # 1 microsecond
    errors_measure = thermal_relaxation_error(t1, t2, time_measure)
    errors_u1 = thermal_relaxation_error(t1, t2, time_u1)
    errors_x = thermal_relaxation_error(t1, t2, time_x)
    errors_h = thermal_relaxation_error(t1, t2, time_h)
    errors_cx = thermal_relaxation_error(t1, t2, time_cx).expand(
        thermal_relaxation_error(t1, t2, time_cx))
    errors_cu1 = thermal_relaxation_error(t1, t2, time_cu1).expand(
        thermal_relaxation_error(t1, t2, time_cu1))

    noise_model = NoiseModel()
    noise_model.add_all_qubit_quantum_error(errors_u1, "u1")
    noise_model.add_all_qubit_quantum_error(errors_x, "x")
    noise_model.add_all_qubit_quantum_error(errors_h, "h")
    # noise_model.add_all_qubit_quantum_error(errors_cx, "cx")
    # noise_model.add_all_qubit_quantum_error(errors_cu1, "cu1")
    noise_model.add_all_qubit_quantum_error(errors_measure, "measure")

    for i in range(num_qubits - 1):
        for j in range(i + 1, num_qubits):
            noise_model.add_quantum_error(errors_cx, "cx", [i, j])
            noise_model.add_quantum_error(errors_cu1, "cu1", [i, j])

    return noise_model



def run_one_sim(qc, if_gpu, error_type):
    backend = Aer.get_backend("statevector_simulator")
    if if_gpu:
        backend.set_options(device="GPU")

    if error_type == "thermal":
        noise_thermal = get_thermal_error(qc.num_qubits)
        job = execute(qc, backend=backend, noise_model=noise_thermal, optimization_level=0)
    else:
        tqc = transpile(qc, backend)
        job = backend.run(tqc)

    result = job.result()
    state_vector = result.data()["final"]

    return state_vector



def VQAA(ansatz, if_back, optimization, max_iter, plain, key, cipher, if_GPU, error_type, threshold, end_prob):
    prev_cost = 114514
    learning_rate = 0.72
    xerr = -9
    gd_time = -1
    graph = create_graph(degree=3, aes_key_length=len(plain))
    cur_iter = 0
    theta_list = [math.pi / 4 for _ in range(len(cipher))]
    while cur_iter < max_iter:
        # 进入一轮优化循环
        qc = generate_circuit_with_state_vector(ansatz_type=ansatz, if_back_control=if_back,
                                                plain_text=plain, theta_list=theta_list)
        ## 获取这一次的测量结果
        from time import perf_counter
        qc_start_time = perf_counter()
        state_vector = run_one_sim(qc=qc, if_gpu=if_GPU, error_type=error_type)
        qc_end_time = perf_counter()
        qc_run_time = round(qc_end_time - qc_start_time)

        ## 计算这次的哈密顿量

        prob = prob_of_measure_correct_cipher(state_vector, cipher)
        expectation = cal_expect_of_ham(g=graph, state_vector=state_vector, cipher=cipher)
        print("---"*60)
        print(f"Current iter is {cur_iter} . This prob is {prob} . Expectation of Ham is {expectation} . Theta : {theta_list}")
        if prob > end_prob:
            if_end = 1
        else:
            if_end = 0
            ## 通过哈密顿量和theta的值更新下一轮线路的theta
            if optimization == "gd":
                gd_begin_time = perf_counter()
                cost, theta_list = gd(graph, ansatz, if_back, plain, cipher,
                                      if_GPU, error_type, expectation, theta_list, threshold, learning_rate, xerr)
                # if (prev_cost - cost) <= threshold:
                #     if_end = 1
                # else:
                #     prev_cost = cost
                gd_end_time = perf_counter()
                gd_time = gd_end_time - gd_begin_time

        with open(Path(f"./iter_{cur_iter}.txt"), "w") as f:
            f.write(f"key : {key}\n")
            f.write(f"plaintext : {plain}\n")
            f.write(f"cipher : {cipher}\n")
            f.write(f"error type : {error_type}\n")
            f.write(f"error level : {error_list[error_type]}\n")
            f.write(f"ansatz type : {ansatz}\n")
            f.write(f"optimization method : {optimization}\n")
            f.write(f"if back : {if_back}\n")
            f.write(f"max iteration : {max_iter}\n")
            f.write(f"if gpu : {if_GPU}\n")
            f.write(f"end prob threshold : {end_prob}")
            f.write(f"--------------------------------------------------------------------------------------------\n")
            f.write(f"current iteration : {cur_iter}\n")
            f.write(f"qc run time : {qc_run_time}\n")
            f.write(f"gd run time : {gd_time}\n")
            f.write(f"correct cipher prob : {prob}\n")
            f.write(f"expectation : {expectation}\n")
            f.write(f"learning rate : {learning_rate}\n")
            f.write(f"xerr : {xerr}\n")
            f.write(f"cost : {cost}\n")
            f.write(f"optimized theta_list : {theta_list}\n")
            f.write(f"if end : {if_end}\n")

        if if_end:
            return

        cur_iter += 1
    return



def create_graph(degree, aes_key_length=8):
    # G = nx.random_graphs.random_regular_graph(degree, aes_key_length)
    G = nx.Graph()
    G.add_node(range(0,aes_key_length))
    G.add_edge(0, 1)
    G.add_edge(0, 6)
    G.add_edge(0, 7)
    G.add_edge(1, 7)
    G.add_edge(1, 3)
    G.add_edge(2, 4)
    G.add_edge(2, 5)
    G.add_edge(2, 7)
    G.add_edge(3, 4)
    G.add_edge(3, 6)
    G.add_edge(4, 5)
    G.add_edge(5, 6)

    return G

    pos = nx.circular_layout(G)
    options = {
        "with_labels": True,
        "font_size": 20,
        "font_weight": "bold",
        "font_color": "white",
        "node_size": 2000,
        "width": 2
    }
    nx.draw_networkx(G, pos, **options)
    ax = plt.gca()
    ax.margins(0.20)
    plt.axis("off")

    plt.savefig("g.png", format="png")
    return G


def get_corresponding_beta_vector(state_vector, n, single_i, omega_i=-1, omega_j=-1):
    # print(state_vector)
    normalized_v = state_vector / np.linalg.norm(state_vector)

    # print(normalized_v)
    if single_i == -1:
        prob = np.array([0, 0, 0, 0],dtype=float).reshape((-1, 1))
        for i in range(2 ** (2 * n)):
            bin_index = bin(i)[2:].rjust(2 * n, '0')
            if bin_index[omega_i] == "0" and bin_index[omega_j] == "0":
                prob[0] = prob[0] + abs(normalized_v[i]) ** 2
            elif bin_index[omega_i] == "0" and bin_index[omega_j] == "1":
                prob[1] = prob[1] + abs(normalized_v[i]) ** 2
            elif bin_index[omega_i] == "1" and bin_index[omega_j] == "0":
                prob[2] = prob[2] + abs(normalized_v[i]) ** 2
            elif bin_index[omega_i] == "1" and bin_index[omega_j] == "1":
                prob[3] = prob[3] + abs(normalized_v[i]) ** 2

    else:
        prob = np.array([0, 0], dtype=float).reshape((-1, 1))
        for i in range(2 ** (2 * n)):
            bin_index = bin(i)[2:].rjust(2 * n, '0')
            if bin_index[single_i] == "0":
                prob[0] = prob[0] + abs(normalized_v[i]) ** 2
            elif bin_index[single_i] == "1":
                prob[1] = prob[1] + abs(normalized_v[i]) ** 2
    return prob


def cal_expect_of_ham(g: nx.Graph, state_vector, cipher):
    """
    :param g: 使用的3-正则图
    :param theta_list: 应该是测量的结果向量，如[0,0,1,0,1,0,1,0]
    :return:
    """
    n = len(cipher)
    expectation = 0
    edge_list = g.edges
    # print(g.edges)
    for one_edge in edge_list:
        V_i, V_j = one_edge[0], one_edge[1]
        if cipher[V_i] == cipher[V_j]:
            omega_ij = -1
        else:
            omega_ij = 1
        correspond_theta_vector = get_corresponding_beta_vector(state_vector=state_vector, n=n, single_i=-1, omega_i=V_i, omega_j=V_j)

        # print(f"omega i,j de vector is {correspond_theta_vector}")
        # print(f"corresponding matrix is {np.kron(pauli_Z, pauli_Z)}")
        expectation = expectation + omega_ij * (correspond_theta_vector.T.conjugate() @ (np.kron(pauli_Z, pauli_Z)) @ correspond_theta_vector)
    #
    for i in range(len(cipher)):
        if cipher[i] == "0":
            t_i = -0.5
        else:
            t_i = 0.5
        correspond_theta_vector = get_corresponding_beta_vector(state_vector=state_vector, n=n, single_i=i)
        # print(f"omega i,j de vector is {correspond_theta_vector}")
        # print(f"corresponding matrix is {pauli_Z}")
        expectation = expectation + t_i * (correspond_theta_vector.T.conjugate() @ pauli_Z @ correspond_theta_vector)

    return expectation[0][0]



def arr2str(vec: np.array):
    return ','.join(str(i) for i in vec)


def prob_of_measure_correct_cipher(state_vector, cipher):
    n = len(cipher)
    prob = 0
    normalized_v = state_vector / np.linalg.norm(state_vector)
    for i in range(2 ** (2 * n)):
        if_add = 1
        bin_index = bin(i)[2:].rjust(2 * n, '0')

        for j in range(n):
            if bin_index[j] != cipher[j]:
                if_add = 0
                break
        if if_add:
            prob += (normalized_v[i]) ** 2
    return prob


def gd(graph, ansatz, if_back, plain, cipher, if_GPU, error_type, expectation, thetas, threshold, lr=0.72, xerr=-9):
    times = 0
    x0 = thetas
    length = len(x0)
    cost = expectation

    print("***"*20)
    print(f"current theta list is {x0}")
    times += 1

    Gd = [0] * length
    for i in range(length):
        x = [t for t in x0]
        x[i] += 0.5
        qc = generate_circuit_with_state_vector(ansatz_type=ansatz, if_back_control=if_back,
                                                plain_text=plain, theta_list=x)
        state_vector = run_one_sim(qc=qc, if_gpu=if_GPU, error_type=error_type)
        cost_ = cal_expect_of_ham(g=graph, state_vector=state_vector, cipher=cipher)
        print(f"changing the {i}th of parameter of theta list and new cost is {cost_}")
        times += 1
        Gd[i] = (cost_ - cost) / 0.5
    r0 = random.uniform(0, 1)
    print(f"current gradient is : {Gd}")

    for j in range(length):
        x0[j] = x0[j] - (lr / abs(cost) + math.log10(times) / times * r0) * Gd[j]

    def abs_sum(some_list):
        return sum([abs(tmp) for tmp in some_list])

    t_sum = abs_sum(Gd)
    if t_sum < 0.8:
        x0 = [random.uniform(0, math.pi / 2) for _ in range(length)]
    print(f"After one iter of gd, |Gd| is {t_sum}")

    for i in range(len(x0)):
        x0[i] = x0[i] % (2 * math.pi)

    return cost, x0



if __name__ == '__main__':
    qc = generate_circuit_with_state_vector("rx", 1, "11110001", "00000010", "11100101",[0,0,0,0,0,0,0])


    qc.draw(output='mpl')
    matplotlib.pyplot.savefig("m.png")
