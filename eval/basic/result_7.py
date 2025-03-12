from qiskit.circuit import QuantumCircuit, Parameter
def create_parametrized_gate():
    """ Generate a 1 qubit QuantumCircuit with a parametrized Rx gate with parameter "theta".
    """
    theta = Parameter("theta")
    qc = QuantumCircuit(1)
    qc.rx(theta, 0)
    return qc

qc = create_parametrized_gate()
qc.draw()

from qiskit.circuit import ParameterVector
def create_parametrized_gate_with_parameter_vector():
    """ Generate a 1 qubit QuantumCircuit with a parametrized Rx gate with parameter vector "theta".
    """
    theta = ParameterVector("theta", 2)
    qc = QuantumCircuit(1)
    qc.rx(theta, 0)
    return qc

qc = create_parametrized_gate_with_parameter_vector()
qc.draw()

from qiskit.circuit import ParameterVector
def create_parametrized_gate_with_parameter_vector_and_label():
    """ Generate a 1 qubit QuantumCircuit with a parametrized Rx gate with parameter vector "theta" and label "theta".
    """
    theta = ParameterVector("theta", 2, label="theta")
    qc = QuantumCircuit(1)
    qc.rx(theta, 0)
   