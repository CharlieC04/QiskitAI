#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
from qiskit import QuantumCircuit


# ## Create Circuit

# In[2]:


def createInputCircuit(data):
    qubits_num = len(data)
    qcircuit = QuantumCircuit(qubits_num, qubits_num)
    qubits = qcircuit.qubits

    for i, d in enumerate(data):
        qcircuit.rx(d * np.pi, qubits[i])
        
    return qcircuit


# In[3]:


def createModelCircuit(params):
    qubits_num = len(params[0])
    qcircuit = QuantumCircuit(qubits_num, qubits_num)
    qubits = qcircuit.qubits

    for i in range(qubits_num):
        qcircuit.u3(*params[0][i], qubits[i])

    for i in range(qubits_num - 1):
        qcircuit.cz(qubits[i], qubits[i + 1])
    qcircuit.cz(qubits[0], qubits[qubits_num - 1])

    for i in range(qubits_num):
        qcircuit.u3(*params[1][i], qubits[i])
        
    return qcircuit


# In[4]:


def createCircuit(params, data):
    input_circuit = createInputCircuit(data)
    model_circuit = createModelCircuit(params)
    full_circuit = input_circuit.compose(model_circuit)
    
    return full_circuit


# ## Create Noisy Circuit

# In[8]:


from qiskit.providers.aer.noise import NoiseModel
from qiskit.providers.aer.utils import insert_noise
from qiskit.providers.aer.noise import pauli_error, depolarizing_error


# In[9]:


def createNoiseModel(p, errorType):
    # QuantumError objects
    if errorType == 'bit_flip':
        error = pauli_error([('X', p), ('I', 1 - p)])
    elif errorType == 'phase_flip':
        error = pauli_error([('Z', p), ('I', 1 - p)])
    elif errorType == 'depolarizing':
        error = depolarizing_error(p, num_qubits=1)
        
    ## two-qubits quantumError objects 
    if errorType == 'depolarizing':
        error_2qubits = depolarizing_error(p, num_qubits=2)
    else:
        error_2qubits = error.tensor(error)
        
    # Add errors to noise model
    noise_model = NoiseModel()
    
    noise_model.add_all_qubit_quantum_error(error, ['u3'])
    noise_model.add_all_qubit_quantum_error(error_2qubits, ['cz'])
    
    return noise_model


# In[10]:


def createNoisyModelCircuit(params, p, errorType):
    noise_model = createNoiseModel(p, errorType)
    model_circuit = createModelCircuit(params)
    
    return insert_noise(model_circuit, noise_model)


# In[12]:
