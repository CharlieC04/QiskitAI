from qiskit.circuit.library import PhaseOracle
from qiskit import QuantumCircuit
from qiskit.circuit.library import GroverOperator
from qiskit import Aer, transpile


sat_problem = [
    [1],
    [4,5,6],
    [7],
    [-3,-6],
    [-2,4,-5]]
 
def save_to_dimacs(file_path, clauses,number_of_bits,number_of_clauses):
    with open(file_path, 'w') as file:
        file.write("p cnf " + str(number_of_bits) + " " + str(number_of_clauses) + "\n")

        for clause in clauses:
            file.write(" ".join(map(str, clause)) + " 0\n")


save_to_dimacs("formula.dimacs", sat_problem,7,len(sat_problem)

def Grovers_algorithm(number_of_qubits):
  oracle = PhaseOracle.from_dimacs_file('formula.dimacs')
  circuit = QuantumCircuit(number_of_qubits)
  for i in range(number_of_qubits):
    circuit.h(i)
  grover = GroverOperator(oracle)
  qc = circuit.compose(grover_operator)
  qc.measure_all()
  sim = Aer.get_backend('aer_simulator')
  transpile_qc = transpile(qc, sim)
  sim.run(transpile_qc).result().get_counts()

Grovers_algorithm(7)

