from qiskit import QuantumCircuit


class CnotOracle:
    @classmethod
    def create_cnot_oracle(cls, input_string, input_length, eval_mode: bool) -> QuantumCircuit:
        balanced_oracle = QuantumCircuit(input_length + 1)
        # Place X-gates
        for qubit in range(len(input_string)):
            if input_string[qubit] == '1':
                balanced_oracle.x(qubit)

        # Use barrier as divider
        balanced_oracle.barrier()

        # Controlled-NOT gates
        for qubit in range(input_length):
            balanced_oracle.cx(qubit, input_length)

        balanced_oracle.barrier()

        # Place X-gates
        for qubit in range(len(input_string)):
            if input_string[qubit] == '1':
                balanced_oracle.x(qubit)
        if not eval_mode:
            # Show oracle
            print("This is the oracle function, aka the black box. NORMALLY THIS WOULD BE HIDDEN!")
            print(balanced_oracle)
        return balanced_oracle
