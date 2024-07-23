from qiskit import *
#provider = IBMQ.enable_account('YOUR API KEY HERE')
#backend = provider.get_backend('ibm_oslo')

def applyHadamard(qc, qubits):
    for q in qubits:
        qc.h(q)

    return qc

def createBooleanOracle(input):
    oracle_circuit = QuantumCircuit(4,name="boolean oracle")
    for x in range(3):
        if input[x] == '0':
            oracle_circuit.x(x)

    oracle_circuit.mct([0,1,2], 3)

    for x in range(3):
        if input[x] == '0':
            oracle_circuit.x(x)

    return oracle_circuit.to_gate()

def createPhaseOracle(input):
    oracle_circuit = QuantumCircuit(3,name="phase oracle")
    for x in range(3):
        if input[x] == '0':
            oracle_circuit.x(x)

    oracle_circuit.ccz(0,1,2)

    for x in range(3):
        if input[x] == '0':
            oracle_circuit.x(x)

    return oracle_circuit.to_gate()

def amplificationGate():
    ampGate = QuantumCircuit(3,name="amplification gate")
    for x in range(3):
        ampGate.x(x)

    ampGate.ccz(0,1,2)

    for x in range(3):
        ampGate.x(x)
    
    for x in range(3):
        ampGate.h(x)

    return ampGate.to_gate()

def runSimulator(grover_circuit): # >70% accuracy  mine until 78% accuracy??????
    backend = BasicAer.get_backend('qasm_simulator')
    job = execute(grover_circuit, backend, shots=8192)
    result = job.result()
    counts = result.get_counts()
    return counts

def runReal(grover_circuit): # <50% accuracy
    job = execute(grover_circuit, backend, shots=8192)
    result = job.result()
    counts = result.get_counts()
    return counts

def mine(input, type_choice):
    grover_circuit = QuantumCircuit(4,3)
    grover_circuit.initialize('0000', grover_circuit.qubits)

    grover_circuit = applyHadamard(grover_circuit, [0,1,2,3])
    #grover_circuit.append(createBooleanOracle(input), [0,1,2,3])
    grover_circuit.append(createPhaseOracle(input), [0,1,2])
    grover_circuit = applyHadamard(grover_circuit, [0,1,2,3])
    grover_circuit.append(amplificationGate(), [0,1,2])
    grover_circuit.measure([0,1,2], [0,1,2])

    if type_choice == "1":
        counts = runSimulator(grover_circuit)
    if type_choice == "2":
        counts = runReal(grover_circuit)
    
    searchFor = input[::-1]
    accuracy = (counts[searchFor] / 8192) * 100
    return accuracy
    
