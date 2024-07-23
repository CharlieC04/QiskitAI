#!/usr/bin/python3



# ---------------- IMPORTATIONS ----------------

#quantum lib
import qiskit as q






# ---------------- CLASS ----------------
class Qomputer:

	#initialization
	def __init__(self, qbit_nbr, measure_nbr):
		self.simulator = q.Aer.get_backend('qasm_simulator')
		self.circuit   = q.QuantumCircuit(qbit_nbr, measure_nbr)

	#console display
	def showCircuit(self):
		print( self.circuit.draw(output='text') )

	#execution
	def run(self, shots):
		raw_results = q.execute(
			self.circuit,
			self.simulator,
			shots=shots
		).result().get_counts(
			self.circuit
		)

		#format results
		results = []
		for r in raw_results:
			results.append( raw_results[r] )

		return results
