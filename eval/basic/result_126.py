from qiskit.circuit.library import HGate
from qiskit.quantum_info import Operator, process_fidelity
import numpy as np
def calculate_phase_difference_fidelity():
    """ Create two quantum operators using Hadamard gate that differ only by a global phase. Calculate the process fidelity between these two operators and return the process fidelity value.
    """
    # Create two quantum operators using Hadamard gate that differ only by a global phase.
    op1 = Operator(HGate())
    op2 = Operator(HGate())
    op2.data = np.exp(1j * np.pi / 2) * op2.data

    # Calculate the process fidelity between these two operators.
    process_fidelity_value = process_fidelity(op1, op2)

    return process_fidelity_value

process_fidelity_value = calculate_phase_difference_fidelity()
print("Process fidelity value:", process_fidelity_value)

from qiskit.circuit.library import HGate
from qiskit.quantum_info import Operator, process_fidelity
import numpy as np
def calculate_phase_difference_fidelity():
    """ Create two quantum operators using Hadamard gate that differ only by a global phase. Calculate the process fidelity between these two operators and return the process fidelity value.
    """
    # Create two quantum operators using Hadamard gate that differ only by a global phase.
    op1 = Operator(HGate