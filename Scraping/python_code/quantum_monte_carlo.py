from typing import List
from qiskit import QuantumCircuit, transpile, QuantumRegister, ClassicalRegister
from qiskit import BasicAer,Aer,execute, IBMQ
from qiskit.providers.aer import QasmSimulator
from qiskit.circuit.library.arithmetic import DraperQFTAdder, RGQFTMultiplier
from qiskit.circuit.library import IntegerComparator
from qiskit.algorithms import IterativeAmplitudeEstimation, AmplitudeEstimation
from qiskit.algorithms import EstimationProblem
from qiskit.utils import QuantumInstance
from qiskit.providers.fake_provider import FakeMontreal


def encode_input(x: List[int]) -> "Gate":
    num_qubits = len(x)
    qc = QuantumCircuit(num_qubits, name="encoding")
    for i in range(num_qubits):
        if x[i] == 1:
            qc.x(num_qubits - i - 1)
    return qc


def encode_hadamard_copy(num_qubits: int) -> "Gate":
    qc = QuantumCircuit(num_qubits * 2, name="extension")
    for i in range(num_qubits):
        qc.cx(i, i + num_qubits)
    return qc


def encode_hadamard(num_qubits: int) -> "Gate":
    qc = QuantumCircuit(num_qubits, name="encoding")
    for i in range(num_qubits):
        qc.h(i)
    return qc


def classical(x: List[int], y: List[int]) -> int:
    num1 = 0
    for i in range(len(x)):
        num1 += x[i] * 0.5 ** (i + 1)

    num2 = 0
    for i in range(len(y)):
        num2 += x[i] * 0.5 ** (i + 1)

    result = num1 ** 2 + num2 ** 2
    if result < 1:
        return 1
    return 0


def operator(bits_per_input, x1, x2, useQAE):
    num_bits_after_mult = 2 * bits_per_input
    num_bits_comparer = num_bits_after_mult + 1
    nQubits = 4 * bits_per_input + 2 * num_bits_after_mult + 1 + num_bits_comparer
    nClassical = 1

    input_register_1 = QuantumRegister(size=bits_per_input)
    input_register_1_copy = QuantumRegister(size=bits_per_input)
    input_register_2 = QuantumRegister(size=bits_per_input)
    input_register_2_copy = QuantumRegister(size=bits_per_input)
    if len(x1) == 0 and len(x2) == 0:
        input_circuit_1 = encode_hadamard(bits_per_input)
        input_circuit_1_copy = encode_hadamard_copy(bits_per_input)
        input_circuit_2 = encode_hadamard(bits_per_input)
        input_circuit_2_copy = encode_hadamard_copy(bits_per_input)
    else:
        input_circuit_1 = encode_input(x1)
        input_circuit_1_copy = encode_input(x1)
        input_circuit_2 = encode_input(x2)
        input_circuit_2_copy = encode_input(x2)

    carry_qubits_mult_1 = QuantumRegister(size=num_bits_after_mult)
    carry_qubits_mult_2 = QuantumRegister(size=num_bits_after_mult)
    carry_qubits_comparer = QuantumRegister(size=num_bits_comparer)
    carry_qubit_addition = QuantumRegister(size=1)  # 1 additional qubit for addition

    if useQAE == False:
        output_register = ClassicalRegister(size=nClassical)
        circuit = QuantumCircuit(
            input_register_1,
            input_register_1_copy,
            input_register_2,
            input_register_2_copy,
            carry_qubits_mult_1,
            carry_qubits_mult_2,
            carry_qubit_addition,
            carry_qubits_comparer,
            output_register
        )
    else:
        circuit = QuantumCircuit(
            input_register_1,
            input_register_1_copy,
            input_register_2,
            input_register_2_copy,
            carry_qubits_mult_1,
            carry_qubits_mult_2,
            carry_qubit_addition,
            carry_qubits_comparer
        )

    # encoding
    circuit.append(input_circuit_1, input_register_1[:])
    if len(x1) == 0 and len(x2) == 0:
        circuit.append(input_circuit_1_copy, input_register_1[:] + input_register_1_copy[:])
    else:
        circuit.append(input_circuit_1_copy, input_register_1_copy[:])
    circuit.append(input_circuit_2, input_register_2[:])
    if len(x1) == 0 and len(x2) == 0:
        circuit.append(input_circuit_2_copy, input_register_2[:] + input_register_2_copy[:])
    else:
        circuit.append(input_circuit_2_copy, input_register_2_copy[:])

    # multiplication
    multiplicator = RGQFTMultiplier(num_state_qubits=bits_per_input)
    circuit.append(multiplicator, input_register_1[:] + input_register_1_copy[:] + carry_qubits_mult_1[:])
    circuit.append(multiplicator, input_register_2[:] + input_register_2_copy[:] + carry_qubits_mult_2[:])

    # addition
    adder = DraperQFTAdder(num_bits_after_mult, kind="half")
    circuit.append(adder, carry_qubits_mult_1[:] + carry_qubits_mult_2[:] + carry_qubit_addition[:])

    # inequality check if in circle
    s = 2 ** (bits_per_input) - 1
    comparer = IntegerComparator(num_bits_after_mult + 1, s * s + 1, False)
    circuit.append(comparer, carry_qubits_mult_2[:] + carry_qubit_addition[:] + carry_qubits_comparer[:])

    # readout
    if useQAE == False:
        circuit.measure(nQubits - num_bits_comparer, 0)

    return circuit


def get_circuit(**kwargs):
    bits_per_input =1  # num qubits per number
    useQAE =True
    circuit =operator(bits_per_input,[],[],useQAE)
    #circuit.draw('mpl')

    #backend = FakeMontreal()
    #circuit_transpiled = transpile(circuit,backend)
    #circuit_transpiled.draw('mpl')
    #circuit_transpiled.depth()

    backend =Aer.get_backend('qasm_simulator')

    circuit_to_return = None
    if useQAE == True:
        quantum_instance = Aer.get_backend('qasm_simulator')
        num_bits_after_mult = 2 * bits_per_input
        num_bits_comparer =num_bits_after_mult+1
        nQubits=4*bits_per_input + 2*num_bits_after_mult+1 +num_bits_comparer

        problem = EstimationProblem(
            state_preparation=circuit.decompose(),  # A operator
            objective_qubits=[nQubits-num_bits_comparer],  # the "good" state Psi1 is identified as measuring |1> in qubit 0
        )

        print(f"Depth: ", circuit.depth())
        print(f"Width: ", circuit.num_qubits)

        ae = AmplitudeEstimation(
            num_eval_qubits=3,  # the number of evaluation qubits specifies circuit width and accuracy
            quantum_instance=quantum_instance,
        )

        iae = IterativeAmplitudeEstimation(
            epsilon_target=0.01,  # target accuracy
            alpha=0.05,  # width of the confidence interval
            quantum_instance=quantum_instance,
        )

        circuit_to_return = iae.construct_circuit(problem, measurement=True).decompose()
        print(circuit_to_return)
        result =iae.estimate(problem)
        print(result)
    else:
        shots =1000
        job= execute(circuit,backend=backend,shots=shots)
        counts =job.result().get_counts()
        print(counts)
        #print(4 * counts['1'] /shots )

    return circuit_to_return
