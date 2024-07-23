import random, pickle, os, copy, random, qiskit_aer, psutil
from qiskit import QuantumCircuit
from qiskit.converters import circuit_to_dag, dag_to_circuit
from qiskit.dagcircuit.dagcircuit import DAGCircuit
from qiskit.quantum_info import Statevector
import numpy as np

from qiskit_helper_functions.conversions import dict_to_array


def scrambled(orig):
    dest = orig[:]
    random.shuffle(dest)
    return dest


def read_dict(filename):
    if os.path.isfile(filename):
        f = open(filename, "rb")
        file_content = {}
        while 1:
            try:
                file_content.update(pickle.load(f))
            except EOFError:
                break
        f.close()
    else:
        file_content = {}
    return file_content


def apply_measurement(circuit, qubits):
    measured_circuit = QuantumCircuit(circuit.num_qubits, len(qubits))
    for circuit_inst, circuit_qubits, circuit_clbits in circuit.data:
        measured_circuit.append(circuit_inst, circuit_qubits, circuit_clbits)
    measured_circuit.barrier(qubits)
    measured_circuit.measure(qubits, measured_circuit.clbits)
    return measured_circuit


def evaluate_circ(circuit, backend, options=None):
    circuit = copy.deepcopy(circuit)
    max_memory_mb = psutil.virtual_memory().total >> 20
    max_memory_mb = int(max_memory_mb / 4 * 3)
    if backend == "statevector_simulator":
        simulator = qiskit_aer.StatevectorSimulator()
        result = simulator.run(circuits=[circuit]).result()
        statevector = result.get_statevector(circuit)
        prob_vector = Statevector(statevector).probabilities()
        return prob_vector
    elif backend == "noiseless_qasm_simulator":
        simulator = qiskit_aer.AerSimulator(max_memory_mb=max_memory_mb)
        if isinstance(options, dict) and "num_shots" in options:
            num_shots = options["num_shots"]
        else:
            num_shots = max(1024, 2**circuit.num_qubits)

        if isinstance(options, dict) and "memory" in options:
            memory = options["memory"]
        else:
            memory = False
        if circuit.num_clbits == 0:
            circuit.measure_all()
        result = simulator.run(circuit, shots=num_shots, memory=memory).result()

        if memory:
            qasm_memory = np.array(result.get_memory(circuit))
            assert len(qasm_memory) == num_shots
            return qasm_memory
        else:
            noiseless_counts = result.get_counts(circuit)
            assert sum(noiseless_counts.values()) == num_shots
            noiseless_counts = dict_to_array(
                distribution_dict=noiseless_counts, force_prob=True
            )
            return noiseless_counts
    else:
        raise NotImplementedError


def circuit_stripping(circuit):
    # Remove all single qubit gates and barriers in the circuit
    dag = circuit_to_dag(circuit)
    stripped_dag = DAGCircuit()
    [stripped_dag.add_qreg(x) for x in circuit.qregs]
    for vertex in dag.topological_op_nodes():
        if len(vertex.qargs) == 2 and vertex.op.name != "barrier":
            stripped_dag.apply_operation_back(op=vertex.op, qargs=vertex.qargs)
    return dag_to_circuit(stripped_dag)


def dag_stripping(dag, max_gates):
    """
    Remove all single qubit gates and barriers in the DAG
    Only leaves the first max_gates gates
    If max_gates is None, do all gates
    """
    stripped_dag = DAGCircuit()
    [stripped_dag.add_qreg(dag.qregs[qreg_name]) for qreg_name in dag.qregs]
    vertex_added = 0
    for vertex in dag.topological_op_nodes():
        within_gate_count = max_gates is None or vertex_added < max_gates
        if vertex.op.name != "barrier" and len(vertex.qargs) == 2 and within_gate_count:
            stripped_dag.apply_operation_back(op=vertex.op, qargs=vertex.qargs)
            vertex_added += 1
    return stripped_dag


def _calc_exp_val(num_qubits: int, observable: str, state: int, prob: float) -> float:
    """Calculate the weighted eigen value of a state and its given prob

    Z|0> = |0>
    Z|1> = -|1>
    I|0> = |0>
    I|1> = |1>

    Args:
        num_qubits (int): _description_
        observable (str): _description_
        state_prob (Tuple[int, float]): _description_

    Returns:
        float: _description_
    """
    eigenvals = {"Z": {"0": 1, "1": -1}, "I": {"0": 1, "1": 1}}
    bin_state = bin(state)[2:].zfill(num_qubits)
    eigenval = 1
    for bit, base in zip(bin_state, observable):
        eigenval *= eigenvals[base][bit]
    return prob * eigenval


def expectation_val(prob_vector: np.ndarray, observable: str) -> float:
    """Calculate the expectation value of a given probability vector

    Args:
        prob_vector (np.ndarray): input probability vector
        observable (str): Z or I observables

    Returns:
        float: expectation value
    """
    num_qubits = len(observable)
    exp_val = 0
    for state, prob in enumerate(prob_vector):
        exp_val += _calc_exp_val(num_qubits, observable, state, prob)
    return exp_val
