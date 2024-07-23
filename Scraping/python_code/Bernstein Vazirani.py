from qiskit import QuantumCircuit
import matplotlib.pyplot as plt
from qiskit.circuit import Gate
from qiskit.visualization import plot_histogram



def oracle_function(qubits_number: int, secret_number: int) -> Gate:
    """
    This function returns a gate corresponding to the question asked 
    to know the secret number

    """

    assert 0 < secret_number < (2**qubits_number-1)
    assert qubits_number>0

    oracle_circuit = QuantumCircuit(qubits_number+ 1, name="oracle")

    for qubit, bit in enumerate(reversed(f"{secret_number:0{qubits_number}b}")):
        if bit == '1':
            oracle_circuit.cx(qubit, qubits_number)

    oracle=oracle_circuit.to_gate()
    
    return oracle



def circuit_function(oracle: Gate) -> QuantumCircuit:
    """
    This function returns the quantum circuit that represents  
    the algorithm of Bernstein Vazirani

    """
    
    qubits_number = oracle.num_qubits
    circuit = QuantumCircuit(qubits_number, qubits_number-1) 

    
    circuit.x(qubits_number-1)
    circuit.h(range(qubits_number))
    circuit.barrier()

    
    circuit.append(oracle, range(qubits_number))
    circuit.barrier()

    
    circuit.h(range(qubits_number-1))
    circuit.barrier()

    
    circuit.measure(range(qubits_number-1), range(qubits_number-1))
    circuit.barrier()

    return circuit


#example:
oracle = oracle_function(6, 33)
circuit = circuit_function(oracle)
        


print(circuit)
circuit.draw(output="mpl", style="clifford")
plt.show()
