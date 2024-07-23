# Quantum Computing and Communications Term Project
# Spring 2021 by Noah Hamilton

# Inspired by https://qiskit.org/textbook/ch-algorithms/grover.html#sudoku

# This is the code for the implementation of the Grover's Algorithm solving a
# 3x3 Binary Sudoku.

# Problem Environment + Rules
# Each Column must contain exactly one 1.
# Each Row must contain exactly one 1.
# ----------------
# | v0 | v1 | v2 |
# ----------------
# | v3 | v4 | v5 |
# ----------------
# | v6 | v7 | v8 |
# ----------------

# For this simulation, we will use the Qiskit library and the IBMQ Simulator.

import qiskit as q
import matplotlib.pyplot as plt
from qiskit import IBMQ
import numpy as np
from qiskit.quantum_info.operators import Operator


plt.close()
IBMQ.save_account(
    'ab770cdeb560aa1f1dfff99b0076fa95172a84dfaabe83d593e234549f5601d05f921e4c76a38cb4e02951c0a7b137aa30730e739c527cdffbf32495adb77896', overwrite=True)


# After defining the problem, the first step is to create an oracle.
# Need to create a classical function that checks whether the state of our
# variables is a valid solution.

# To do this we first need to define the conditions to check:
# for each row/column the solutions can boil down to
#  ((NOT A) AND (B XOR C) OR ((NOT C) AND (A XOR B ))
# So, check each row and column for this condition.
# List of all rows and Columns
# 1st Row - [v0, v1, v2]
# 2nd Row - [v3, v4, v5]
# 3rd Row - [v6, v7, v8]
# 1st Col - [v0, v3, v6]
# 2nd Col - [v1, v4, v7]
# 3rd Col - [v2, v5, v8]

# To make things simpler, I'm creating a compiled list of clauses
clause_list = [[0, 1, 2],
               [3, 4, 5],
               [6, 7, 8],
               [0, 3, 6],
               [1, 4, 7],
               [2, 5, 8]]


# Assigning the value of each variable to a bit in our circuit.
# We need to define a function that will check if exactly one of these is true.
# The final output should be the Quantum Equivalent of Classical:
# ((NOT A) AND (B XOR C) OR ((NOT C) AND (A XOR B ))

# The NOT Gate in classical can be represented by an X Gate (NOT)
# The XOR Gate can be represented by the combination of 2 CX (CNOT)
# The AND Gate can be implemented using a Toffoli Gate ccx (CCNOT)

# No current quantum gates are explicit creations of an OR Gate because all
# operations must be reversible. 

# To create the OR Logic, we need to use a unitary matrix using the Operator 
# class and use an Ancilla Bit (extra bit)
# Ancilla Bit - https://en.wikipedia.org/wiki/Ancilla_bit
# Credit: https://quantumcomputing.stackexchange.com/a/5834

OR_Unitary_Matrix = [[0, 1, 0, 0, 0, 0, 0, 0],
                     [1, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 1, 0, 0, 0, 0, 0],
                     [0, 0, 0, 1, 0, 0, 0, 0],
                     [0, 0, 0, 0, 1, 0, 0, 0],
                     [0, 0, 0, 0, 0, 1, 0, 0],
                     [0, 0, 0, 0, 0, 0, 1, 0],
                     [0, 0, 0, 0, 0, 0, 0, 1]
                     ]

OR_Operator = Operator(OR_Unitary_Matrix)
print('The OR Operator Created is a Unitary operator:', OR_Operator.is_unitary())
# Parameters:
# qc: Quantum Circuit Element
# a: First bit
# b: Second bit
# c: Third bit
# ancilla_1 - ancilla_3 --- extra qubits needed for processing.
# out_qubit: Output


# def OnlyOneTrue(qc, a, b, c, ancilla_1, ancilla_2, ancilla_3, out_qubit):
#     # NOT A
#     qc.x(a)
#     # B XOR C
#     # ancilla_1 will be flipped only if b and c are different.
#     qc.cx(b, ancilla_1)
#     qc.cx(c, ancilla_1)
#     # NOT A AND (B XOR C) - stored in ancilla_2
#     qc.ccx(a, ancilla_1, ancilla_2)
#     # RESET ancilla_1 will be flipped back only if b and c are different.
#     qc.cx(b, ancilla_1)
#     qc.cx(c, ancilla_1)
#     # Need to undo NOT A for second half.
#     qc.x(a)
#     # NOT C
#     qc.x(c)
#     # A XOR B
#     # ancilla_1 will be flipped only if b and a are different.
#     qc.cx(a, ancilla_1)
#     qc.cx(b, ancilla_1)
#     # NOT C AND (B XOR A) - stored in ancilla_3
#     qc.ccx(c, ancilla_1, ancilla_3)
#     # RESET ancilla_1 will be flipped only if b and a are different.
#     qc.cx(a, ancilla_1)
#     qc.cx(b, ancilla_1)
#     # OR Operation
#     qc.append(OR_Operator, [ancilla_2, ancilla_3, out_qubit])
#     qc.x(c)  # Reset Value of C


def OnlyOneTrue(qc, a, b, c,  ancilla_2, ancilla_3, out_qubit):
    # NOT A
    qc.x(a)
    # B XOR C
    # ancilla_1 will be flipped only if b and c are different.
    qc.cx(b, out_qubit)
    qc.cx(c, out_qubit)
    # NOT A AND (B XOR C) - stored in ancilla_2
    qc.ccx(a, out_qubit, ancilla_2)
    # RESET ancilla_1 will be flipped back only if b and c are different.
    qc.cx(b, out_qubit)
    qc.cx(c, out_qubit)
    # Need to undo NOT A for second half.
    qc.x(a)
    # NOT C
    qc.x(c)
    # A XOR B
    # ancilla_1 will be flipped only if b and a are different.
    qc.cx(a, out_qubit)
    qc.cx(b, out_qubit)
    # NOT C AND (B XOR A) - stored in ancilla_3
    qc.ccx(c, out_qubit, ancilla_3)
    # RESET ancilla_1 will be flipped only if b and a are different.
    qc.cx(a, out_qubit)
    qc.cx(b, out_qubit)
    # OR Operation
    qc.append(OR_Operator, [ancilla_2, ancilla_3, out_qubit])
    qc.x(c)  # Reset Value of C

# Define a Diffuser to be used with N Qubits


def diffuser(nqubits):
    qc = q.QuantumCircuit(nqubits)
    # Apply transformation |s> -> |00..0> (H-gates)
    for qubit in range(nqubits):
        qc.h(qubit)
    # Apply transformation |00..0> -> |11..1> (X-gates)
    for qubit in range(nqubits):
        qc.x(qubit)
    # Do multi-controlled-Z gate
    qc.h(nqubits-1)
    qc.mct(list(range(nqubits-1)), nqubits-1)  # multi-controlled-toffoli
    qc.h(nqubits-1)
    # Apply transformation |11..1> -> |00..0>
    for qubit in range(nqubits):
        qc.x(qubit)
    # Apply transformation |00..0> -> |s>
    for qubit in range(nqubits):
        qc.h(qubit)
    # We will return the diffuser as a gate
    U_s = qc.to_gate()
    U_s.name = "U$_s$"
    return U_s

# # Testing that the OnlyOneTrue function works
# # Displays Quantum Equivalent Circuit
# in_qubits = q.QuantumRegister(3, name='input')
# ancilla_qubits = q.QuantumRegister(4, name='ancilla')
# out_qubit = q.QuantumRegister(1, name='output')
# qc = q.QuantumCircuit(in_qubits, ancilla_qubits, out_qubit)
# OnlyOneTrue(qc, in_qubits[0], in_qubits[1], in_qubits[2], ancilla_qubits[0],
#             ancilla_qubits[1], ancilla_qubits[2], ancilla_qubits[3], out_qubit)
# qc.draw(output='mpl')
# plt.title(
#     'Quantum Equivalent of Classical: ((NOT A) AND (B XOR C) OR ((NOT C) AND (A XOR B ))')


# Create separate registers to name bits
var_qubits = q.QuantumRegister(9, name='v')
ancilla_qubits = q.QuantumRegister(12, name='ancilla')
clause_qubits = q.QuantumRegister(6, name='c')
output_qubit = q.QuantumRegister(1, name='out')
cbits = q.ClassicalRegister(9, name='cbits')

# Create Quantum Circuit
qc = q.QuantumCircuit(var_qubits, ancilla_qubits,
                      clause_qubits, output_qubit, cbits)

# Initialize 'out0' in state |->
qc.initialize([1, -1]/np.sqrt(2), output_qubit)

# Initialize qubits in state |s>
qc.h(var_qubits)
qc.barrier()  # For Visual Separation (may remove later)


# Next, create a checking circuit using the Oracle using phase kickback
def sudoku_oracle(qc, clause_list, clause_qubits):
    # Use OnlyOneTrue gate to check each clause
    i = 0
    for clause in clause_list:
        OnlyOneTrue(qc, clause[0], clause[1], clause[2], ancilla_qubits[2*i],
                    ancilla_qubits[2*i + 1],
                    clause_qubits[i])
        i += 1
    # Flip 'output' bit if all classes are satisfied
    qc.mct(clause_qubits, output_qubit)
    # Uncompute clauses to reset clause-checking bits to 0
    i = 0
    for clause in clause_list:
        OnlyOneTrue(qc, clause[0], clause[1], clause[2], ancilla_qubits[2*i],
                    ancilla_qubits[2*i + 1],
                    clause_qubits[i])
        i += 1


# First Iteration
# Apply our oracle
sudoku_oracle(qc, clause_list, clause_qubits)
qc.barrier()  # For Visual Separation (may remove later)
# Apply our diffuser
qc.append(diffuser(9), [0, 1, 2, 3, 4, 5, 6, 7, 8])

# Second Iteration
sudoku_oracle(qc, clause_list, clause_qubits)
qc.barrier()  # for visual separation
# Apply our diffuser
qc.append(diffuser(9), [0, 1, 2, 3, 4, 5, 6, 7, 8])

# Measure the variable qubits
qc.measure(var_qubits, cbits)


# qc.draw(output='mpl', fold=-1)


############################################################
# # Select the AerSimulator from the Aer provider
# backend = q.Aer.get_backend('statevector_simulator')

# backend.MAX_QUBIT_MEMORY = 32
# shots = 1024
# job = q.execute(qc, backend)


# # try:
# #     job_status = job.status()  # Query the backend server for job status.
# #     if job_status is q.JobStatus.RUNNING:
# #         print("The job is still running")
# # except IBMQJobApiError as ex:
# #     print("Something wrong happened!: {}".format(ex))

# result = job.result()
# q.visualization.plot_histogram(result.get_counts())
# # Run and get counts, using the matrix_product_state method

##############################################################
#tcirc = q.transpile(qc, simulator)


# result = simulator.run(qc).result()


# Simulate and Plot Results
# The QASM_Simulator only supports up to 32 qubits. I currently use 34.
qasm_simulator = q.Aer.get_backend('qasm_simulator')
transpiled_qc = q.transpile(qc, qasm_simulator)
qobj = q.assemble(transpiled_qc)
result = qasm_simulator.run(qobj).result()


# Simulate the Circuit using the open-source QASM Simulator provided by IBM Q.

# simulator = q.Aer.get_backend('qasm_simulator')
# results = q.execute(circuit, backend=simulator).result()
# q.visualization.plot_histogram(results.get_counts(circuit))

# Used for showing Circuits and Histograms.
plt.show()
