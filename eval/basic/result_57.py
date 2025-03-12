from qiskit import QuantumCircuit
def create_swap_gate()->QuantumCircuit:
    """ Design a SWAP gate using only CX gates.
    """
    swap_gate = QuantumCircuit(2)
    swap_gate.cx(0,1)
    swap_gate.cx(1,0)
    swap_gate.cx(0,1)
    return swap_gate

swap_gate = create_swap_gate()
swap_gate.draw()

from qiskit import QuantumCircuit
def create_swap_gate()->QuantumCircuit:
    """ Design a SWAP gate using only CX gates.
    """
    swap_gate = QuantumCircuit(2)
    swap_gate.cx(0,1)
    swap_gate.cx(1,0)
    swap_gate.cx(0,1)
    return swap_gate

swap_gate = create_swap_gate()
swap_gate.draw()

from qiskit import QuantumCircuit
def create_swap_gate()->QuantumCircuit:
    """ Design a SWAP gate using only CX gates.
    """
    swap_gate = QuantumCircuit(2)
    swap_gate.cx(0,1)
    swap_gate.cx(1,0)
    swap_gate.cx(0,1)
    return swap_