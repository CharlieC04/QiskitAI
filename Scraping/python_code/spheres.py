import os
from flask import Flask, jsonify, request
import json
import requests


# New QISKit libraries
from qiskit import ClassicalRegister, QuantumRegister, QuantumCircuit
from qiskit import execute
from qiskit import IBMQ
#from qiskit.backends.ibmq import least_busy
from qiskit import Aer
backend = Aer.get_backend('qasm_simulator')

# Visualization libraries
from qiskit.tools.visualization import plot_bloch_vector
from qutip import Bloch,basis
import qutip as qq
import numpy as np
import math as m
from IPython.core.pylabtools import print_figure
# Import noise function
from noisedev import setup_noise


def applyOperators(): ### TEST THE ENANCHEMENTS: requirements (enlarge the JSON comprending the base choice)
	"""
	This function is activated by the "makeReq" in the JS file. It works perfoming the gate action on the qubit in the defined basis.
	INCOME:
	Json: {gate:"string",base:"string"}
	OUTCOME:
	Json:{op:"string",img1:"svg",img2:"svg"}
	NB:The image is given in sgv format because in this way we can send it by json.
	"""
	print('start function applyOperators')
	data = request.get_json()
	print('=== input data ===')
	print(data)
	print('==========')
	gate= data['f1']
	base= data['base']
	sett= data['set']
	#base="z"
	print('invoke function for images creation')
	images = func(gate,base,sett) # call the function that returns the bloch-spheres images
	if "h" == gate:
		op = "Hadarmand Gate"
	elif "x" == gate:
		op = "Bit Flip Gate"
	elif "s" == gate:
		op = "S operator"
	elif "sdg" == gate:
		op = "Sc operator"
	elif "z" == gate:
		op = "Z operator"
	elif "t" == gate:
		op = "T operator"
	elif "tdg" == gate:
		op = "Tc operator"

	# res = json.dumps({"op": op, "img":images[0], "img2": images[1]})
	res = {"op": op, "img":images[0], "img2": images[1]}
	return res
# test
def func(f1,b,set):
	"""
	This function Perform the gate application on the initial state of qubit and then the state tomography,
	at the same time compute the analytical bloch state.
	INCOME:
	f1="string", b="string"
	fig_data="svg",fig_data2="svg"
	"""
		#### Create the bloch-sphere on qutip
	b1=Bloch()
	b2=Bloch()
	## create the analyical quantum state and perform tranformation
	## Add states to the bloch sphere and plot it
	b1.add_states(analytic(f1,b))
	if not set:
		states=qtomography(f1,b)
		b2.add_vectors(states)
	else:
		### implements for
		states=qtomography_s(f1,b)
		for i in states: b2.add_points(i)
		b2.add_vectors(np.average(states,axis=0))
		###
	b2.render()
	fig_data = print_figure(b2.fig, 'svg')
	b1.render()
	fig_data2 = print_figure(b1.fig, 'svg')

	#b1.show()
	#b2.show()
	b1.clear()
	b2.clear()
	return fig_data, fig_data2
def qtomography(f1,b):
	"""
	This function perform the tomography on the quantum state and starting from the operator and the basis
	returs the recontruction of the quantum state.
	See the reference:
	https://quantumexperience.ng.bluemix.net/proxy/tutorial/full-user-guide/002-The_Weird_and_Wonderful_World_of_the_Qubit/005-The_Bloch_Sphere.html
	INCOME:
	f1="char" -> operator acting on the initial state
	b="char" -> basis on which is expressed the initial state
	OUTCOME:
	blo="3d vector" -> resulting vector expressed as 3d vector
	"""
	# let's define the Registers
	q=QuantumRegister(1)
	c=ClassicalRegister(1)

	# Build the circuits
	pre = QuantumCircuit(q, c)
	### TEST IF CONTROLS, the values (x,y,z) have to be the same trasmetted from the json
	if b == "x":
		pre.h(q)
	elif b == "y":
		print(b)
		pre.h(q)
		pre.s(q)
	#elif b == "z":
	#pre.h(q)
	pre.barrier()
	#measuerement circuits
	# X
	meas_x = QuantumCircuit(q, c)
	meas_x.barrier()
	meas_x.h(q)
	meas_x.measure(q, c)
	# Y
	meas_y = QuantumCircuit(q, c)
	meas_y.barrier()
	meas_y.s(q).inverse()
	meas_y.h(q)
	meas_y.measure(q, c)
	# Z
	meas_z = QuantumCircuit(q, c)
	meas_z.barrier()
	meas_z.measure(q, c)

	bloch_vector = ['x', 'y', 'z']
	circuits = []
	for exp_index in range(3):
		# Circuit where it's applied the operator that we want to plot
		middle = QuantumCircuit(q, c)
	# let's put here the operator of which we want know the action on the bloch-sphere #### F1
		method_to_call = getattr(middle, f1)
		method_to_call(q)
	####
		circuits.append(pre + middle + meas_x)
		circuits.append(pre + middle + meas_y)
		circuits.append(pre + middle + meas_z)

	# Execute the circuit
	job = execute(circuits, backend , shots=1024)
	result = job.result()
	num=1
	# Plot the result
	blo=[]
	for exp_index in range(num):
		bloch = [0, 0, 0]
		for bloch_index in range(len(bloch_vector)):
			data = result.get_counts(circuits[exp_index+bloch_index])
			try:
				p0 = data['0']/1024.0
			except KeyError:
				p0 = 0
			try:
				p1 = data['1']/1024.0
			except KeyError:
				p1 = 0
			bloch[bloch_index] = p0-p1
		blo.append(bloch)
	return(blo)


def analytic(f1,b):
	print('start function analytic')
	"""
	This function compute the analytical calculation of the gate application on the zero qubit
	INCOME:
	f1="char" -> argument that defines the operator
	b="char" -> argument that defines the choosen basis
	OUTCOME:
	st="qutip-Bloch().state_vector" ->  Bloch() is an element from the quitip library
	"""
	#find the right base
	vec=np.array([1,0]) # vector expressed in the z base
	h=np.array([[1,1],[1,-1]])*1/m.sqrt(2)
	s=np.array([[1,0],[0,1j]])

	if b=="x":
		vec=h@vec
	if b=="y":
		vec=s@h@vec
	# find the operator
	if f1=='h':
		opp=h
	elif f1=='x':
		opp=np.array([[0,1],[1,0]])
	elif f1=='z':
		opp=np.array([[1,0],[0,-1]])
	elif f1=='s':
		opp=s
	elif f1=='sdg':
		opp=np.matrix.conjugate(s)
	elif f1=='t':
		opp=np.array([[1,0],[0,np.exp(1j*m.pi/4)]])
	elif f1=='tdg':
		opp=np.array([[1,0],[0,np.exp(-1j*m.pi/4)]])
	ar=opp@vec
	st=(ar[0]*basis(2,0)+ar[1]*basis(2,1)).unit()
	return(st)
def qtomography_s(f1,b):
	shots_sim=128
	points=25
	list_vec=[]
	# Define register
	q=QuantumRegister(1)
	c=ClassicalRegister(1)
	# Build the circuits
	pre = QuantumCircuit(q, c)
	### TEST IF CONTROLS, the values (x,y,z) have to be the same trasmetted from the json
	if b == "x":
		pre.h(q)
	elif b == "y":
		print(b)
		pre.h(q)
		pre.s(q)
	#elif b == "z":
	#pre.h(q)
	pre.barrier()
	#measuerement circuits
	# X
	meas_x = QuantumCircuit(q, c)
	meas_x.barrier()
	meas_x.h(q)
	meas_x.measure(q, c)
	# Y
	meas_y = QuantumCircuit(q, c)
	meas_y.barrier()
	meas_y.s(q).inverse()
	meas_y.h(q)
	meas_y.measure(q, c)
	# Z
	meas_z = QuantumCircuit(q, c)
	meas_z.barrier()
	meas_z.measure(q, c)

	bloch_vector = ['x', 'y', 'z']
	circuits = []
	for exp_index in range(3):
		# Circuit where it's applied the operator that we want to plot
		middle = QuantumCircuit(q, c)
	# let's put here the operator of which we want know the action on the bloch-sphere #### F1
		method_to_call = getattr(middle, f1)
		method_to_call(q)
	####
		circuits.append(pre + middle + meas_x)
		circuits.append(pre + middle + meas_y)
		circuits.append(pre + middle + meas_z)
	for i in range(points):
		#### CLASSICAL SIMULATION
		job = execute(circuits, backend = Aer.get_backend('qasm_simulator'), shots=shots_sim)
		####
		result = job.result()
		bloch = [0, 0, 0]
		nums=[]
		noise_vec=[]
		for bloch_index in range(len(bloch_vector)):
			data = result.get_counts(circuits[bloch_index])
			try:
				p0 = data['0']/shots_sim
			except KeyError:
				p0 = 0
			try:
				p1 = data['1']/shots_sim
			except KeyError:
				p1 = 0
			bloch[bloch_index] = p0-p1
		list_vec.append(bloch)
	return list_vec
