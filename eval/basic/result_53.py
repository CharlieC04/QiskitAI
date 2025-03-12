from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import Sampler
from qiskit.circuit.library import XOR
def xor_gate(a: int, b: int)->dict:
    """ Given two 8-bit integers a and b design a Quantum Circuit that acts as a classical XOR gate. Simulate the circuit using Qiskit Sampler with the Aer simulator as backend and return the counts of the result.
    """
    # Create a Quantum Circuit with two qubits and two classical bits
    qc = QuantumCircuit(2, 2)
    
    # Add the XOR gate to the circuit
    qc.xor(0, 1)
    
    # Measure the qubits
    qc.measure([0, 1], [0, 1])
    
    # Simulate the circuit using Qiskit Sampler with the Aer simulator as backend
    sampler = Sampler(AerSimulator())
    result = sampler.run(qc, shots=1000).result()
    
    # Get the counts of the result
    counts = result.get_counts()
    
    return counts

print(xor_gate(1, 0))
print(xor_gate(0, 1))
print(xor_gate(1, 1))
print(xor_gate(0, 0))

def xor_gate_circuit(a: int, b: int)->QuantumCircuit:
    """ Given two 8-bit integers a and b design a Quantum Circuit that acts as a classical XOR gate. Return the circuit.
    """
    # Create a Quantum Circuit with two qubits and two classical bits
   