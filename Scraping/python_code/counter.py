from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit.circuit.library import QFT

from src.arithmetic.increment import control_increment, control_decrement
from src.util.util import run_qc


def count(circuit, count_register, control_register, amount=1, step=1, apply_QFT=True):
    q_l = len(count_register)
    a_l = len(control_register)
    assert a_l % step == 0

    if apply_QFT:
        # circuit.barrier()
        circuit = circuit.compose(QFT(num_qubits=q_l, approximation_degree=0, do_swaps=True,
                                      inverse=False, insert_barriers=True, name='qft'), qubits=count_register)
        # circuit.barrier()

    for i in range(int(a_l / step)):
        circuit = control_increment(circuit, count_register, control_register[i * step: (i + 1) * step],
                                    amount, apply_QFT=False)

    if apply_QFT:
        # circuit.barrier()
        circuit = circuit.compose(QFT(num_qubits=q_l, approximation_degree=0, do_swaps=True,
                                      inverse=True, insert_barriers=True, name='iqft'), qubits=count_register)
        # circuit.barrier()

    return circuit


def mincount(circuit, count_register, control_register, amount=1, step=1, apply_QFT=True):
    q_l = len(count_register)
    a_l = len(control_register)

    assert a_l % step == 0

    if apply_QFT:
        # circuit.barrier()
        circuit = circuit.compose(QFT(num_qubits=q_l, approximation_degree=0, do_swaps=True,
                                      inverse=False, insert_barriers=True, name='qft'), qubits=count_register)
        # circuit.barrier()

    for i in range(int(a_l / step)):
        circuit = control_decrement(circuit, count_register, control_register[i * step:(i + 1) * step], amount, apply_QFT=False)

    if apply_QFT:
        # circuit.barrier()
        circuit = circuit.compose(QFT(num_qubits=q_l, approximation_degree=0, do_swaps=True,
                                      inverse=True, insert_barriers=True, name='iqft'), qubits=count_register)
        # circuit.barrier()

    return circuit


def test():
    q = QuantumRegister(3)
    a = QuantumRegister(3)
    c = ClassicalRegister(3)
    qc = QuantumCircuit(q, a, c)

    qc.x(a[0])
    qc.x(q[:])

    qc = mincount(qc, q, a)

    # Should equal 110
    qc.measure(q[:], c[:])

    run_qc(qc)
    qc.draw(output="mpl")


if __name__ == "__main__":
    test()
