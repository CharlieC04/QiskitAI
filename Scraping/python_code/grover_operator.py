from qiskit import QuantumCircuit
from qiskit.circuit.library.standard_gates.x import MCXGate


# Class that creates and holds grover's circuit for some given expression
class GroverOperator:
    def get_control_circuit(self, label="Grover"):
        grit = self.main_circuit.to_gate()
        grit.label = label
        return grit.control()

    def __init__(self, n, cnf_exp):
        self.n_bits = n
        eq = len(cnf_exp)
        self.total_bits = n + eq + 1
        main_circuit = QuantumCircuit(self.total_bits)
        for i, e in enumerate(cnf_exp):
            state = ''
            target = n + i
            pos = []
            for qbit in e:
                state += '0' if (qbit > 0) else '1'
                pos.append(abs(qbit) - 1)
            pos.append(target)
            state = state[::-1]
            main_circuit.append(MCXGate(len(e), None, state), pos)
        oracle_rev = main_circuit.reverse_ops()
        main_circuit.append(MCXGate(eq, None, '0' * eq), range(n, self.total_bits))
        main_circuit = main_circuit.compose(oracle_rev)
        #     main_circuit.barrier()
        main_circuit.h(range(n))
        main_circuit.append(MCXGate(n, None, '0' * n), list(range(n)) + [self.total_bits - 1])
        main_circuit.h(range(n))
        #     main_circuit.barrier()
        self.main_circuit = main_circuit
        self.control_circuit = self.get_control_circuit()
