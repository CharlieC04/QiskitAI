from qiskit.quantum_info import schmidt_decomposition
def schmidt_test(data, qargs_B):
    """ Return the schmidt decomposition coefficients and the subsystem vectors for the given density matrix and partition.
    """
    # Compute the schmidt decomposition
    coeffs, states = schmidt_decomposition(data)
    # Compute the subsystem vectors
    qargs_A = [qargs_B[0]]
    qargs_B = [qargs_B[1]]
    subsys_A = [states[i] for i in range(len(states)) if qargs_A[0] in states[i].qargs]
    subsys_B = [states[i] for i in range(len(states)) if qargs_B[0] in states[i].qargs]
    return coeffs, subsys_A, subsys_B

# Test the function
data = np.array([[0.5, 0.5], [0.5, 0.5]])
qargs_B = [0, 1]
coeffs, subsys_A, subsys_B = schmidt_test(data, qargs_B)
print("Schmidt decomposition coefficients:", coeffs)
print("Subsystem vectors for subsystem A:", subsys_A)
print("Subsystem vectors for subsystem B:", subsys_B)

#