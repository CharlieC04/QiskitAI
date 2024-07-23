#Classical vs Quantum Computer


#!/usr/bin/env python
# coding: utf-8

# In[2]:


#simple unordered list of elements
my_list = [1, 3, 5, 2, 4, 9, 5, 8, 0, 7]


# In[4]:


#defining my varibale
#set wining number you would like
def the_oracle(my_input):
    winner=7
    if my_input is winner:
        response = True
    else:
        response = False
    return response


# In[25]:


#Classical computer enumeration on a winning number
for index, trial_number in enumerate(my_list):
    if the_oracle(trial_number) is True:
        print('winner winner found at index %i'%index)
        print('%i calls to the oracle used' % (index+1))
        break


# In[26]:


#Transistion to Qiskit Aer
#import dependencies

from qiskit import *
import matplotlib.pyplot as plt
import numpy as np


# In[11]:


#define the oracle circuit
oracle = QuantumCircuit(2, name='oracle')
oracle.cz(0,1)
oracle.to_gate()
oracle.draw()


# In[13]:


backend = Aer.get_backend('statevector_simulator')
grover_circ = QuantumCircuit(2,2)
grover_circ.h([0, 1])
grover_circ.append(oracle, [0, 1])
grover_circ.draw()


# In[15]:


job = execute(grover_circ, backend)
result = job.result()


# In[16]:


sv = result.get_statevector()
np.around(sv, 2)


# In[18]:
#Grovers Diffusion Operator [Operator] + [Reflection]

reflection = QuantumCircuit(2, name='reflection')
reflection.h([0, 1])
reflection.z([0,1])
reflection.cz(0,1)
reflection.h([0,1])
reflection.to_gate()


# In[20]:


reflection.draw()


# In[22]:


backend = Aer.get_backend('qasm_simulator')
grover_circ = QuantumCircuit(2, 2)
grover_circ.h([0,1])
grover_circ.append(oracle, [0, 1])
grover_circ.append(reflection, [0, 1])
grover_circ.measure([0, 1], [0,1])


# In[23]:


grover_circ.draw()


# In[24]:


job=execute(grover_circ,backend,shots=1)
result=job.result()
result.get_counts()


# In[ ]:




