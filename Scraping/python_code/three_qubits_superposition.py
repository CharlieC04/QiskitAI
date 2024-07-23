from qiskit import execute, Aer, QuantumCircuit, IBMQ


class ThreeQubitSuperposition:
    @classmethod
    def run(cls):
        # Use Aer's qasm_simulator
        simulator = Aer.get_backend('qasm_simulator')
        # Create a Quantum Circuit acting on the q register
        circuit = QuantumCircuit(3, 3)
        # Add a H gate on qubit 0
        circuit.h(0)
        circuit.h(1)
        circuit.h(2)
        # Map the quantum measurement to the classical bits
        for i in range(3):
            circuit.measure(i, i)
        # Execute the circuit on the qasm simulator
        job = execute(circuit, simulator, shots=1024)
        # Grab results from the job
        result = job.result()
        # Returns counts
        counts = result.get_counts(circuit)
        print("\nTotal count all possible states are:", counts)

        provider = IBMQ.load_account()
        backend = provider.backends.ibmq_valencia
        # Execute the circuit on a real device
        job = execute(circuit, backend=backend, shots=1024)
        # Grab results from the job
        result = job.result()
        # Returns counts
        counts = result.get_counts(circuit)
        print("\nTotal count for all possible states are:", counts)
        # Draw the circuit
        print(circuit)
