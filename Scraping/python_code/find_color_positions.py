from qiskit import ClassicalRegister
from qiskit.circuit.quantumcircuit import QuantumCircuit
from qiskit.circuit.quantumregister import QuantumRegister
from src.logic.query import query_cd
from src.arithmetic.increment import control_increment, control_decrement
from src.logic.oracles import oracle_a
from src.util.util import run_qc


def FCP(circuit, y_register, qy_register, s_register, secret_string, c, d, d_positions=None):
    # init
    # q1 = QuantumRegister(num_position, "q1")
    # q2 = QuantumRegister(num_bits_color * num_position)
    # out = QuantumRegister(num_bits_color + 1, "o")

    # step 1: apply H gate
    circuit.h(y_register[:])
    circuit.barrier()

    # step 2: query
    circuit = circuit.compose(query_cd(c, d), [*y_register, *qy_register])
    # _build_query_two_colours(qc, qy_register, y_register, c, d)

    circuit.barrier()

    # step 3: ask oracle
    circuit = oracle_a(circuit, qy_register, s_register, secret_string)
    circuit.barrier()

    # step 3.alt: compensate for d positions

    if d_positions is not None:
        for (i, j) in enumerate(d_positions):
            if j == 1:
                # apply x gets to y
                circuit.x(y_register[i])
                # apply decrement with y control
                circuit = control_decrement(circuit, s_register, [y_register[i]])
                circuit.x(y_register[i])
                circuit.barrier()

    # step 4: apply Z to LSB
    circuit.z(s_register[0])
    circuit.barrier()

    # step 5: undo step 2 and 3
    circuit = oracle_a(circuit, qy_register, s_register, secret_string, do_inverse=True)
    circuit = circuit.compose(query_cd(c, d), [*y_register, *qy_register])
    # _build_query_two_colours(qc, qy_register, y_register, c, d)
    circuit.barrier()

    # step 5.alt: undo step 3.alt

    if d_positions is not None:
        for (i, j) in enumerate(d_positions):
            if j == 1:
                # apply x gets to y
                circuit.x(y_register[i])
                # apply decrement with y control
                circuit = control_increment(circuit, s_register, [y_register[i]])
                circuit.x(y_register[i])
                circuit.barrier()

    # step 6: apply H gate
    circuit.h(y_register[:])
    circuit.barrier()

    if c + d != 3:
        circuit.x(y_register)

    return circuit

    #     d
    #   x 0 1 2 3
    # c 0 - x x v
    #   1 x - v x
    #   2 x v - x
    #   3 v x x -
    #
    #   x - bit flip
    #   v - correct


if __name__ == "__main__":
    qy = QuantumRegister(8, name='qy')
    y = QuantumRegister(4, name='y')
    s = QuantumRegister(3)
    cr = ClassicalRegister(4)
    qc = QuantumCircuit(y, qy, s, cr)

    # qc.x(qy[0])
    qc = FCP(qc, y, qy, s, [1, 0, 3, 3], 1, 2)
    qc.barrier()

    qc.measure(y[:], cr[::-1])

    run_qc(qc, with_QI=False)
    qc.draw(output="mpl")
