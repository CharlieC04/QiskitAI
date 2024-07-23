from qiskit import execute, Aer, QuantumCircuit


class Interference:
    @classmethod
    def run(cls):
        # Use Aer's qasm_simulator

        simulator = Aer.get_backend('qasm_simulator')

        # Create a Quantum Circuit acting on the q register
        circuit = QuantumCircuit(1, 1)

        # Add a H gate on qubit 0
        circuit.h(0)
        # Add another H gate to qubit 0
        circuit.h(0)

        # Map the quantum measurement to the classical bits
        circuit.measure(0, 0)

        # Execute the circuit on the qasm simulator
        job = execute(circuit, simulator, shots=1000)

        # Grab results from the job
        result = job.result()

        # Returns counts
        counts = result.get_counts(circuit)
        print("Results for the Quantum Interference experiment.")
        print("\nTotal count for 0 and 1 are:", counts)
        print(circuit)
