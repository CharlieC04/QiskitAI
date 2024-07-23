import qiskit
from qiskit import QuantumCircuit, QuantumRegister
from qiskit.extensions import UnitaryGate

import numpy as np
from scipy.linalg import fractional_matrix_power
from scipy.io import loadmat, savemat

from copy import deepcopy





# problems = ((1,4),(1,8),(1,16),(2,4),(2,8),(2,16),(3,4),(3,16),(4,4),(4,16),(5,6),(5,20),(6,4),(6,16),(7,6),(7,20))
problems = ((5,6),(5,20),(6,4),(6,16),(7,6),(7,20))







def CR_phi_d(phi, d, register_1, register_2):
	circuit = QuantumCircuit(register_1,register_2,name = 'CR_( \\phi \\tilde {})'.format(d))
	
	circuit.cnot(register_2,register_1,ctrl_state=0)
	circuit.rz(phi*2, register_1)
	circuit.cnot(register_2,register_1,ctrl_state=0)
	
	return circuit








for problem in problems:
	problem_number = problem[0]
	size = problem[1]






	iterations = int(np.floor(128/size -1))
	# iterations = 7
	K = np.array( loadmat('N_{}_problem_{}.mat'.format(size,problem_number)) ).item()['A']
	R = np.array( loadmat('N_{}_problem_{}.mat'.format(size,problem_number)) ).item()['R']
	B = np.array( loadmat('N_{}_problem_{}.mat'.format(size,problem_number)) ).item()['B']
	f = np.array( loadmat('N_{}_problem_{}.mat'.format(size,problem_number)) ).item()['f']
	f = f/np.linalg.norm(f)
	print('|R|_2 = {}'.format(np.linalg.norm(R,2)))

	A = np.eye((iterations+1)*size,(iterations+1)*size)
	for block in range(iterations):
		A[(block+1)*size:(block+2)*size,(block)*size:(block+1)*size] = -R
#		 A[(block+1)*size:(block+2)*size,(block)*size:(block+1)*size] = -np.eye(size)

	A_orig = deepcopy(A)
	# Normalize the matrix using the upper bound
	A = A/2
	np.linalg.norm(A,2)
	
	RHS_provided = True








	A_shape = np.shape(A_orig)





	# Hermitian Dilation
	# Only if A is not Hermitian
	from copy import deepcopy
	if np.any(A != A.conj().T):
		A = np.block([
			[np.zeros(np.shape(A)),A],
			[A.conj().T,np.zeros(np.shape(A))]
		])
		HD = True
	else:
		HD = False
	print(HD)




	if RHS_provided:
		b = np.zeros(((iterations+1)*size,1))

		for block in range(iterations):
			b[(block+1)*size:(block+2)*size,:] = f
		b = b / np.linalg.norm(b,2)

		b = b.flatten()

		b_orig = deepcopy(b)

		if HD:
			b = np.concatenate([b,np.zeros(b.shape)])
		print(b)






	if np.size(A)>1:
		A_num_qubits = int(np.ceil(np.log2(np.shape(A)[0])))
		padding_size = 2**A_num_qubits - np.shape(A)[0]
		if padding_size > 0:
			A = np.block([
				[A, np.zeros([np.shape(A)[0],padding_size])],
				[np.zeros([padding_size,np.shape(A)[0]]), np.zeros([padding_size,padding_size])]
			])
	else:
		A_num_qubits = 1
		padding_size = 1
		A = np.array([[A,0],[0,0]])
		
	print(A_num_qubits)
	print(padding_size)


	print(A)




	# If RHS is given, it also needs to be padded
	if RHS_provided:
		b = np.pad(b,(0,padding_size))






	O = np.block([
		[A   ,   -fractional_matrix_power(np.eye(np.shape(A)[0]) - np.linalg.matrix_power(A,2),0.5)],
		[fractional_matrix_power(np.eye(np.shape(A)[0]) - np.linalg.matrix_power(A,2),0.5)   ,   A]
	])

	print(O)

	# We also need to get the block-encoding size, i.e. m, used to encode A in U_A

	m = int(np.log2(np.shape(O)[0]) - A_num_qubits)
	O_A_num_qubits = int(np.log2(np.shape(O)[0]))

	print('m = {} \nNumber of Qubits for O_A is {}'.format(m,O_A_num_qubits))




	blockA = UnitaryGate(O,label='O_A')








	register_1 = QuantumRegister(size = 1, name = '|0>')
	register_2 = QuantumRegister(size = m, name = '|0^m>')
	register_3 = QuantumRegister(size = O_A_num_qubits-m, name = '|\\phi>')





	from scipy.io import loadmat
	phi_angles = np.array( loadmat('phi_k_50_14.mat') ).item()['phi']

	phi_tilde_angles = np.zeros(np.shape(phi_angles))
	temp = np.zeros(np.shape(phi_angles))

	# plot QSP angles
	for d,phi in enumerate(phi_angles):
		if d==0 or d==np.size(phi_angles)-1:
			temp[d] = phi_angles[d] - np.pi/4
		else:
			temp[d] = phi_angles[d]

	phase_angles = phi_angles.reshape(phi_angles.shape[0])










	circuit = QuantumCircuit(register_1, register_2, register_3, name = 'QSP')

	if RHS_provided:
		circuit.initialize(b,list(reversed(register_3)))

	# First thing is to  Hadamard the ancilla qubit since we want Re(P(A))
	circuit.h(register_1)

	# Note: QSPPACK produces symmetric phase angles, so reversing phase angles is unnecessary
	# for d, phi in enumerate(reversed(phase_angles)):
	for d, phi in reversed(list(enumerate(phase_angles))):
		circuit = circuit.compose(CR_phi_d(phi,d,register_1,register_2))
		if d>0:
			# The endianness of the bits matters. Need to change the order of the bits
			circuit.append(blockA,list(reversed(register_3[:])) + register_2[:])


	# Apply the final Hadamard gate
	circuit.h(register_1)


	circuit = circuit.reverse_bits()
	circuit.size()




	from qiskit import transpile
	circuit = transpile(circuit)








	from qiskit import QuantumRegister, ClassicalRegister
	from qiskit import QuantumCircuit, execute
	from qiskit import Aer

	Aer.backends()












	# solver = 'unitary'
	solver = 'statevector'

	machine = "CPU"
	# machine = "GPU"

	# precision = "single"
	precision = "double"












	if solver=='unitary':
	#	 backend = Aer.get_backend('unitary_simulator',precision = 'double',device="GPU")
		backend = Aer.get_backend('unitary_simulator',precision = precision,device=machine)

		job = execute(circuit, backend, shots=0)
		result = job.result()
		
		QSP_unitary = result.get_unitary(circuit,100)
		QSP_matrix = np.array(QSP_unitary.to_matrix())
		print(QSP_matrix)
		
	elif solver=='statevector':
		backend = Aer.get_backend('statevector_simulator',precision = precision,device=machine)
	#	 backend = Aer.get_backend('statevector_simulator',precision = 'double',device="GPU")

		job = execute(circuit, backend, shots=0)
		result = job.result()
		
		QSP_statevector = result.get_statevector()
		
		print(QSP_statevector)











	if solver=='statevector':
	    # We can ignore the padding size and directly use the size of b (considering Hermitian dilation)
	    if HD:
	        P_A_b = np.real(QSP_statevector.data[int(b_orig.shape[0]):(2*b_orig.shape[0])])
	    else:
	        P_A_b = np.real(QSP_statevector.data[0:b.shape[0]])
	    P_A_b = P_A_b/np.linalg.norm(P_A_b)




	if solver=='statevector':
		expected_P_A_b = np.linalg.solve(A_orig,b_orig)
		expected_P_A_b = expected_P_A_b/np.linalg.norm(expected_P_A_b)




	exact_solution = np.linalg.solve(K,f)

	x_exact_normalized = exact_solution
	x_exact_normalized = x_exact_normalized/np.linalg.norm(x_exact_normalized)




	error_actual = []
	if solver=='statevector':
		for iteration_number in range(1,iterations):
			e = x_exact_normalized - (P_A_b[iteration_number*size:(iteration_number+1)*size]/np.linalg.norm(P_A_b[iteration_number*size:(iteration_number+1)*size])).reshape(np.shape(x_exact_normalized))
			error_actual.append(np.linalg.norm(e))



	error_expected = []
	if solver=='statevector':
		for iteration_number in range(1,iterations):
			e = x_exact_normalized - (expected_P_A_b[iteration_number*size:(iteration_number+1)*size]/np.linalg.norm(expected_P_A_b[iteration_number*size:(iteration_number+1)*size])).reshape(np.shape(x_exact_normalized))
			error_expected.append(np.linalg.norm(e))






	mdic = {"classical":error_expected,"quantum":error_actual,"kappa":np.linalg.cond(A_orig)}

	savemat("output_N_{}_problem_{}.mat".format(size,problem_number), mdic)





