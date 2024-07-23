import qiskit
#Code based on Qiskit offcial Textbook
#Create the circuit for the Bernstein-Vazirani algorithm
def bv_algorithm(bitstring: str, num_qubits: int) -> qiskit.QuantumCircuit:
    
    #Create the quantum circuit
    bv_circuit = qiskit.QuantumCircuit(num_qubits + 1, num_qubits)

    #Apply H-gate to the output qubit
    bv_circuit.h(num_qubits)
    
    #Apply Z-gate to the output qubit
    bv_circuit.z(num_qubits)

    #Apply H-gates to all qubits
    for qubit in range(num_qubits):
        bv_circuit.h(qubit)

    #Reverse the order of the bitstring
    s = bitstring[::-1]  
    for qubit in range(num_qubits):
        if s[qubit] == '0':
            #If the position equals to 0, apply an I-gate
            bv_circuit.i(qubit)
        else:
            #Else, apply CX-gates
            bv_circuit.cx(qubit, num_qubits)

    #Apply H-gates to all qubits
    for qubit in range(num_qubits):
        bv_circuit.h(qubit)

    #Measure all the qubits 
    for qubit in range(num_qubits):
        bv_circuit.measure(qubit, qubit)

    return bv_circuit

#Run the simulation with the given circuit
def bernstein_azirani(bitstring: str, num_qubits: int) -> qiskit.QuantumCircuit:

    #Get the simulator 
    simulator = qiskit.Aer.get_backend('qasm_simulator')

    #Get the circuit
    circuit = bv_algorithm(bitstring, num_qubits)

    #Execute the Bernstein-Vazirani algorithm
    job = qiskit.execute(circuit, simulator, shots=1000)
    
    #Get results
    result = job.result().get_counts()
    
    return result