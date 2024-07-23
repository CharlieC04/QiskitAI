# This algorithm demonstrates the creation of a Bell state.

# In this state, 2 qubits are entangled to create a link between their final and intermediate states.
# Let X and Y be the entangled qubits.
# When qubit X collapses into the state 0, Y then must be in the state 1.
# Through this concept, we create a unified final state probability distribution between
# the two and proceed with the execution on the QASM simulator, a quantum virtual
# machine.

import qiskit as qk
from qiskit import execute, BasicAer
backend = BasicAer.get_backend('qasm_simulator')

STATE_MEASUREMENTS = 10000

# Create the circuit registers.
qr = qk.QuantumRegister(2)
cr = qk.ClassicalRegister(2)

# Create the quantum circuit.
# Contains a single Hadamard gate and a CNOT gate
qc = qk.QuantumCircuit(qr, cr)
qc.h(qr[0])
qc.cx(qr[0], qr[1])

# Prepare the measurement.
measure_z = qk.QuantumCircuit(qr, cr)
measure_z.measure(qr, cr)

# Execute the job and take the measurement with the specified number of shots.
test_z = qc + measure_z
job_1 = qk.execute([test_z], backend, shots = STATE_MEASUREMENTS)
counts = job_1.result().get_counts(test_z)

print(counts)
