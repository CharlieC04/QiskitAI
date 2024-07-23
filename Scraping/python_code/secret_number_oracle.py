from qiskit import QuantumCircuit


class SecretNUmberOracle:
    @classmethod
    def create_secret_number_oracle(cls, random_binary, eval_mode: bool) -> QuantumCircuit:

        n = len(random_binary)
        secret_number_oracle = QuantumCircuit(len(random_binary) + 1, len(random_binary))

        # Use barrier as divider
        secret_number_oracle.barrier()

        # Controlled-NOT gates
        for qubit in range(len(random_binary)):
            if random_binary[qubit] == '1':
                secret_number_oracle.cx(qubit, n)

        secret_number_oracle.barrier()
        if not eval_mode:
            # Show oracle
            print("This is the oracle function, aka the black box. NORMALLY THIS WOULD BE HIDDEN!")
            print(secret_number_oracle)
        return secret_number_oracle
