from qiskit import QuantumCircuit

from QCLG_lvl3.oracles.cnot_oracle import CnotOracle


class DeutschJosza:

    @classmethod
    def deutsch_josza(cls, bit_string: str, eval_mode: bool) -> QuantumCircuit:
        n = len(bit_string)

        dj_circuit = QuantumCircuit(n + 1, n)
        # Apply H-gates
        for qubit in range(n):
            dj_circuit.h(qubit)

        # Put output qubit in state |->
        dj_circuit.x(n)
        dj_circuit.h(n)

        # Construct balanced oracle
        balanced_oracle = CnotOracle.create_cnot_oracle(bit_string, n, eval_mode)

        # Add oracle
        dj_circuit += balanced_oracle

        # Repeat H-gates
        for qubit in range(n):
            dj_circuit.h(qubit)
        dj_circuit.barrier()

        # Measure
        for i in range(n):
            dj_circuit.measure(i, i)
        if not eval_mode:
            print(dj_circuit)

        # return circuit
        return dj_circuit



