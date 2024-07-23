#---------------------1-------------------------
from qiskit import QuantumCircuit as qubit  # Import QuantumCircuit class from qiskit library as qubit
qc = qubit(2)  # Create a quantum circuit with 2 qubits
qc.h(0)  # Apply a Hadamard gate to the first qubit (qubit 0), putting it in a superposition state
qc.cx(0, 1)  # Apply a CNOT gate with the first qubit (qubit 0) as control and the second qubit (qubit 1) as target, entangling them
qc.draw(output="mpl")  # Draw the circuit diagram using matplotlib (mpl) 

#---------------------2-------------------------
from qiskit.quantum_info import Pauli  # Import Pauli class from qiskit library for Pauli operators
from qiskit_aer.primitives import Estimator  # Import Estimator class from qiskit library for estimating expectation values
ZZ = Pauli("ZZ")  # Define a Pauli operator ZZ
ZI = Pauli("ZI")  # Define a Pauli operator ZI
IZ = Pauli("IZ")  # Define a Pauli operator IZ
XX = Pauli("XX")  # Define a Pauli operator XX
XI = Pauli("XI")  # Define a Pauli operator XI
IX = Pauli("IX")  # Define a Pauli operator IX
observable = [ZZ, ZI, IZ, XX, XI, IX]  # List of observables (tensor products of Pauli operators)
estimator = Estimator()  # Initialize an Estimator to calculate expectation values
job = estimator.run([qc] * len(observable), observable)  # Run the estimator on the quantum circuit for each observable
print(job.result())  # Print the result of the estimation

#---------------------3-------------------------
import matplotlib.pyplot as plt  # Import pyplot class from matplotlib library for plotting
data = ["ZZ", "ZI", "IZ", "XX", "XI", "IX"]  # List of observables as strings
values = job.result().values  # Get the expectation values from the job result
plt.plot(data, values, '-o')  # Plot the data with expectation values
plt.xlabel("Observables")  # Set the label for the x-axis
plt.ylabel("Expectation value")  # Set the label for the y-axis
plt.show()  # Show the plot

#---------------------4-------------------------
def QcforNQubits(n: int):  # Define a function that creates a quantum circuit with n qubits
    qc = qubit(n)  # Initialize a quantum circuit with n qubits
    qc.h(0)  # Apply a Hadamard gate to the first qubit (qubit 0)
    for i in range(n - 1):  # Loop through qubits from 0 to n-1
        qc.cx(i, i + 1)  # Apply a CNOT gate between each qubit and the next one
    return qc  # Return the created quantum circuit

n = 10  # Number of qubits for the new circuit
qc = QcforNQubits(n)  # Create a quantum circuit with 10 qubits
qc.draw(output="mpl")  # Draw the circuit diagram using matplotlib (mpl)

#---------------------5-------------------------
from qiskit.quantum_info import SparsePauliOp  # Import SparsePauliOp class from qiskit library for sparse Pauli operators
operatorStrings = ["Z" + "I" * i + "Z" + "I" * (n - 2 - i) for i in range(n - 1)]  # Create operator strings for ZZ measurements at different distances
operators = [SparsePauliOp(operatorString) for operatorString in operatorStrings]  # Convert operator strings to SparsePauliOp objects
print(operatorStrings)

#---------------------6-------------------------
from qiskit_ibm_runtime import QiskitRuntimeService  # Import QiskitRuntimeService class for accessing IBM's quantum services
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager  # Import function to generate preset pass managers
from qiskit_ibm_runtime import EstimatorV2  # Import EstimatorV2 class for estimating expectation values using IBM runtime
from qiskit_ibm_runtime import EstimatorOptions  # Import EstimatorOptions class for configuring the EstimatorV2
backendName = "ibm_brisbane"  # Define the name of the backend to use
# Initialize the IBM Quantum service with the provided API token and channel
backend = QiskitRuntimeService(token="API_TOKEN", channel="ibm_quantum").backend(backendName)
# Generate a preset pass manager for circuit optimization
passManager = generate_preset_pass_manager(optimization_level=1, backend=backend)
qcTranspiled = passManager.run(qc)  # Transpile the quantum circuit for the backend
operatorsTranspiledList = [op.apply_layout(qcTranspiled.layout) for op in operators]  # Apply the layout to each operator
options = EstimatorOptions()  # Initialize Estimator options
options.resilience_level = 1  # Set resilience level to 1
options.optimization_level = 0  # Set optimization level to 0
options.dynamical_decoupling.enable = True  # Enable dynamical decoupling
options.dynamical_decoupling.sequence_type = "XY4"  # Set dynamical decoupling sequence type to XY4
estimatorv2 = EstimatorV2(backend, options=options)  # Initialize EstimatorV2 with the backend and options
job = estimatorv2.run([(qcTranspiled, operatorsTranspiledList)])  # Run the estimator job with the transpiled circuit and operators
