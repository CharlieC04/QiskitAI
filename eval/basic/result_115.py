from qiskit.transpiler import Target, InstructionProperties
from qiskit.circuit.library import UGate, CXGate
from qiskit.circuit import Parameter
def create_target() -> Target:
    """ Create a Target object for a 2-qubit system and add UGate and CXGate instructions with specific properties.
    - Add UGate for both qubits (0 and 1) with parameters 'theta', 'phi', and 'lambda'.
    - Add CXGate for qubit pairs (0,1) and (1,0).
    - All instructions should have nonzero 'duration' and 'error' properties set.
    """
    target = Target()
    target.add_instruction(UGate(Parameter('theta'), Parameter('phi'), Parameter('lambda')), qubits=[0, 1], duration=100, error=0.001)
    target.add_instruction(CXGate(), qubits=[0, 1], duration=100, error=0.001)
    target.add_instruction(CXGate(), qubits=[1, 0], duration=100, error=0.001)
    return target

target = create_target()

# Print the properties of the instructions in the target object.
for instruction in target.instructions:
    print(f"Instruction: {instruction.name}")
    print(f"Duration: {instruction.duration}")
    print(f"Error: {instruction.error}")
    print()

from qiskit.transpiler import CouplingMap
from qiskit.transpiler.passes import Unroller
from qiskit.transpiler.passes import UnrollerConfig
from qiskit.transpiler.passes import UnrollerMode
from qiskit.transpiler.passes import Unroller3Q
