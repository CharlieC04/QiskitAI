from qiskit import QuantumCircuit

from QCLG_lvl3.oracles.secret_number_oracle import SecretNUmberOracle


class BernsteinVazirani:

    @classmethod
    def bernstein_vazirani(cls, random_binary, eval_mode: bool) -> QuantumCircuit:
        # Construct secret number oracle

        secret_number_oracle = SecretNUmberOracle.create_secret_number_oracle(random_binary=random_binary, eval_mode=eval_mode)
        num_of_qubits = secret_number_oracle.num_qubits

        # Construct circuit according to the length of the number

        dj_circuit = QuantumCircuit(num_of_qubits, num_of_qubits - 1)
        dj_circuit_before_oracle = QuantumCircuit(num_of_qubits, num_of_qubits - 1)

        # Apply H-gates
        for qubit in range(num_of_qubits - 1):
            dj_circuit_before_oracle.h(qubit)

        # Put output qubit in state |->
        dj_circuit_before_oracle.x(num_of_qubits - 1)
        dj_circuit_before_oracle.h(num_of_qubits - 1)

        dj_circuit += dj_circuit_before_oracle

        # Add oracle
        dj_circuit += secret_number_oracle

        dj_circuit_after_oracle = QuantumCircuit(num_of_qubits, num_of_qubits - 1)
        # Repeat H-gates
        for qubit in range(num_of_qubits - 1):
            dj_circuit_after_oracle.h(qubit)
        dj_circuit_after_oracle.barrier()

        # Measure
        for i in range(num_of_qubits - 1):
            dj_circuit_after_oracle.measure(i, i)

        dj_circuit += dj_circuit_after_oracle
        if not eval_mode:
            print("Circuit before the oracle\n")
            print(QuantumCircuit.draw(dj_circuit_before_oracle))
            print("Circuit after the oracle\n")
            print(QuantumCircuit.draw(dj_circuit_after_oracle))
            print(dj_circuit)
        return dj_circuit
