from qiskit.circuit import Parameter, QuantumCircuit

def remove_unassigned_parameterized_gates(circuit: QuantumCircuit) -> QuantumCircuit:
    """ Remove all the gates with unassigned parameters from the given circuit.
    """
    return circuit.remove_nonlocal_gates()

def remove_unassigned_parameterized_qubits(circuit: QuantumCircuit) -> QuantumCircuit:
    """ Remove all the qubits with unassigned parameters from the given circuit.
    """
    return circuit.remove_nonlocal_qubits()

def remove_unassigned_parameters(circuit: QuantumCircuit) -> QuantumCircuit:
    """ Remove all the parameters with unassigned values from the given circuit.
    """
    return circuit.remove_nonlocal_parameters()

def remove_unassigned_parameters_from_gate(gate: QuantumCircuit) -> QuantumCircuit:
    """ Remove all the parameters with unassigned values from the given gate.
    """
    return gate.remove_nonlocal_parameters()

def remove_unassigned_parameters_from_instruction(instruction: QuantumCircuit) -> QuantumCircuit:
    """ Remove all the parameters with unassigned values from the given instruction.
    """
    return instruction.remove_nonlocal_parameters()

def remove_unassigned_parameters_from_parameterized_gate(gate: QuantumCircuit) -> QuantumCircuit:
    """ Remove all the parameters