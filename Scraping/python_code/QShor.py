"""Implementation of Shor's Algorithm using Qiskit and QASN simulator."""
"""All code by Shmuel Jacobs, algorithms as cited
Circuit is hard coded for specific case a=2, N=15 (N=21 code provided also)
"""

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, execute, Aer, IBMQ
from qiskit.compiler import transpile, assemble
# from qiskit.tools.jupyter import *
from qiskit.visualization import *
from datetime import datetime
import math

REG_SIZE=6
N=15
N_len=4
from ArithmaticFunctions import *

backend = Aer.get_backend("qasm_simulator")

x_reg = QuantumRegister(N_len, 'x') # register holds superposition of powers, to which a is raised.
base_reg = QuantumRegister(REG_SIZE, 'base') # Evaluate a^x in this register
scratch_a = QuantumRegister(REG_SIZE, 'sca') 
# Three scratch registers are needed. Each addition requires one carry register.
# Each multiplication requires additions, a register to hold conditional sum, and product accumulator.
# Multiplications as bitshifts require additions, conditional subtrahend and conditional shift value.
scratch_b = QuantumRegister(REG_SIZE, 'scb')
scratch_c = QuantumRegister(REG_SIZE, 'scc')
class_reg = ClassicalRegister(REG_SIZE, 'y')
# qc = QuantumCircuit(x_reg, base_reg, scratch_a, scratch_b, scratch_c, class_reg)

def qft(circ, q, n):
    """n-bit QFT on q in circ"""
    for j in range(n):
        circ.h(q[j])
        for k in range(j+1, n):
            circ.cu1(math.pi/float(2**(k-j)), q[k], q[j])
        circ.barrier()

def flip_twentyone(circ, reg):

	circ.x(reg[5])
	circ.x(reg[3])
	circ.x(reg[0])

def flip_fifteen(circ, reg):

	for bit in range(N_len):
		circ.x(reg[bit])

def build_circuit():
	"""In the interest of saving memory, this function only builds | x, y }> -> | x, a^x Mod y }>
	and transpiles along the way. QFT can be added after transpile."""

	# qft(qc, x_reg, N_len)

	#### Implement Exponentiation as a series of modular multiplications, Neilsen and Chang style
	# NOTE: Selection of 2 as base allows bit shifts of one instead of multiplying base**i
	# to prepare each exponential term. 2 is a suitable base for factoring 15 and 21, but is not 
	# always suitable. All multiplication by a power of two can be implemented as a bitshift.

	"""When using base that is not a square integer, implement each multiplication by x^i using the following.
		- Set scratch register to 1.
		- c_copy original base (constant a in Neilsen and Chuang description) into scratch register.
		- For j in 0:log2(i)
			- multiply scratch register by itself
			- mod reduce
	"""
	
	qc = QuantumCircuit(x_reg, base_reg, scratch_a, scratch_b, scratch_c, class_reg)

	# Set base to 1
	qc.x(base_reg[0])

	# When x[0], multiply base by 2 (base *= x^1, implemented as overwrite to 2), else no op.
	# This is a shortcut for 2^1 to cut down on multiplications.
	qc.reset(scratch_a)
	c_copy_register(qc, control_bit=x_reg[0], origin=base_reg, dest=scratch_a)
	bit_shift_left(qc, scratch_a)
	c_copy_register(qc, control_bit=x_reg[0], origin=scratch_a, dest=base_reg)

	#### If x[1], double 2 times

	# Copy into scratch register to double twice
	qc.reset(scratch_a)
	c_copy_register(qc, control_bit=x_reg[0], origin=base_reg, dest=scratch_a)
	bit_shift_left(qc, scratch_a, places=2)
	# Max value of scratch_a at this point is 2^3. Since period is not known,
	# all future shifts are immediately followed by mod reduction.

	#### Optimized multiplications are over. Define general case for a=2.

	#### If x[k], mod double base_reg 2^(k+1) times
	for k in range(2, len(x_reg)):
		for j in range(2**k): # Pattern of copy -- double the copy -- reduce -- copy back
			c_copy_register(qc, control_bit=x_reg[k], origin=base_reg, dest=scratch_a)
			bit_shift_left(qc, scratch_a, places=1)
			c_copy_register(qc, control_bit=x_reg[k], origin=scratch_a, dest=base_reg)
			flip_fifteen(circ=qc, reg=scratch_a )
			mod_reduce(
					circuit=qc,
					base_reg=base_reg,
					mod_reg=scratch_a,
					scratch_carry=scratch_b,
					scratch_unadd=scratch_c)


		gate_count = qc.count_ops()
		# Transpile after each U operation, or circuit will fill memory
		try:
			qc = transpile(qc, backend=backend, optimization_level=2)
		except MemoryError:
			print(f'Failed to transpile after multplying 2^{k} times, with {gate_count} gates in circuit.')

	"""At this point, base_reg holds a^x Mod N. Since x is superposition
	from 0 to 15, base_reg is superposition of periodic mod function."""

	# Get period of a^x Mod N
	qft(qc, x_reg, N_len)

	"""Quantum portion of algorithm is complete.
	-	Given period r = 4 for function 2^x Mod 15,we know 2^4 - 1 ModEquals 15 =>
		(2^2 + 1)(2^2 - 1) ModEquals 15. GCD(3, 15) = 3 => 3 is a factor of 15,
		GCD(5, 15) = 5 => 5 is a factor of 15.
	-	Given period r = 6 for function 2^x Mod 21,we know 2^6 - 1 ModEquals 21 =>
		(2^3 + 1)(2^3 - 1) ModEquals 21. GCD(9, 21) = 3 => 3 is a factor of 21,
		GCD(7, 21) = 7 => 7 is a factor of 21."""

	return qc

def main():

	first_QFT = QuantumCircuit(x_reg, base_reg, scratch_a, scratch_b, scratch_c, class_reg)
	qft(first_QFT, x_reg, 4)

	circuit = build_circuit()
	# num_unopt_ops = circuit.count_ops()
	# try:
	# 	clumsy_qasm_file = open("Shor_Clumsy.qasm", 'w')
	# 	clumsy_qasm_file.write(f'Un-optimized circuit uses {num_unopt_ops} gates')
	# 	clumsy_qasm_file.write(circuit.qasm())
	# 	clumsy_qasm_file.close()
	# 	del clumsy_qasm_file
	# except MemoryError:
	# 	print("Can't write non-optimized circuit to file.")
    
	# qc = transpile(circuit, backend=backend, optimization_level=2)
	circuit = first_QFT + circuit

	# try:
	# 	qasm_out_file = open("Shor_Opt.qasm", 'w')
	# 	qasm_out_file.write(circuit.qasm())
	# 	qasm_out_file.write("\n\n")
	# 	qasm_out_file.write(f'Optimized circuit uses {circuit.count_ops()} gates.')
	# 	qasm_out_file.write(f'Optimized circuit uses {circuit.depth()} qubits.')
	# except MemoryError:
	# 	print("Can't write optimized circuit to file.")
	# finally:
	# 	qasm_out_file.close()

	try:
		qasm_out_file = open("results.txt", 'w')
		simulate = execute(qc, backend=backend, shots=32).result()
		qasm_out_file.write(simulate.get_counts())
	except MemoryError:
		exit("Failed")
	finally:
		qasm_out_file.close()

main()