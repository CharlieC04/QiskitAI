import numpy as np
import qiskit as q
#Code based on Qiskit offcial Textbook
#Create the oracle for the Deutsch-Jozsa Algorithm    
def dj_oracle(case: str, num_qubits: int) -> q.QuantumCircuit:

    #Create the circuit
    oracle_qc = q.QuantumCircuit(num_qubits + 1)

    #Create the balanced oracle
    if case == "balanced":
        #Ganerate a random binary string
        b = np.random.randint(1, 2 ** num_qubits)
        b_str = format(b, f"0{num_qubits}b")
        for index, bit in enumerate(b_str):
            if bit == "1":
                #If the position is equal to 1, apply X-gate
                oracle_qc.x(index)
        for index in range(num_qubits):
            #For all the qubits, apply CX-gate 
            oracle_qc.cx(index, num_qubits)
        for index, bit in enumerate(b_str):
            if bit == "1":
                #If the position is equal to 1, apply X-gate
                oracle_qc.x(index)
    
    #Create the the constant oracle 
    if case == "constant":
        #Set the output to 0 or 1 randomly
        output = np.random.randint(2)
        if output == 1:
            #If the position is equal to 1, apply X-gate
            oracle_qc.x(num_qubits)

    #Create the Gate    
    oracle_gate = oracle_qc.to_gate()

    return oracle_gate

#Carry out the Deutsch-Jozsa Algorithm
def dj_algorithm(oracle: q.QuantumCircuit, num_qubits: int) -> q.QuantumCircuit:
    
    #Create a quantum circuit
    dj_circuit = q.QuantumCircuit(num_qubits + 1, num_qubits)
    
    #Apply X-gates to the output qubit
    dj_circuit.x(num_qubits)
    
    #Apply H-gates to the output qubit
    dj_circuit.h(num_qubits)

    #Apply H-gate to all qubits
    for qubit in range(num_qubits):
        dj_circuit.h(qubit)
    
    #Apply the oracle created
    dj_circuit.append(oracle, range(num_qubits + 1))

    #Apply H-gate to all qubits
    for qubit in range(num_qubits):
        dj_circuit.h(qubit)

    #Measure all the qubits
    for i in range(num_qubits):
        dj_circuit.measure(i, i)

    return dj_circuit

#Run the simulation with the created circuit
def deutsch_jozsa(case: str, num_qubits: int) -> q.result.counts.Counts:
    
    #Get the simulator
    simulator = q.Aer.get_backend("qasm_simulator")

    #Get the oracle
    oracle = dj_oracle(case, num_qubits)

    #Ger the circuit
    dj_circuit = dj_algorithm(oracle, num_qubits)

    #Performe the algorithm 
    job = q.execute(dj_circuit, simulator, shots=1000)

    return job.result().get_counts(dj_circuit)