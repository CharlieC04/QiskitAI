#!/usr/bin/env python
# coding: utf-8

# In[13]:


get_ipython().run_line_magic('matplotlib', 'inline')
# Importing standard Qiskit libraries and configuring account
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, execute, Aer, IBMQ
from qiskit.compiler import transpile, assemble
from qiskit.tools.jupyter import *
from qiskit.visualization import *
import math
# Loading your IBM Q account(s)
IBMQ.load_accounts()


# In[14]:


backend = Aer.get_backend("qasm_simulator")


# In[26]:


n_reg = QuantumRegister(4, 'n')
m_reg = QuantumRegister(8, 'm')
c_reg = ClassicalRegister(8, 'y')
qc = QuantumCircuit(n_reg, m_reg,c_reg)


# In[27]:


# Register n set to 5
qc.x(n_reg[0])
qc.x(n_reg[2])
# Register m set to 3
qc.x(m_reg[0])
qc.x(m_reg[1])


# In[24]:


def bit_shift_x_bits(circuit, control_reg, acc_reg, power):
    """Implement bit shift.
    @param circuit: QuantumCircuit containing operands
    @param control_reg: QuantumRegister containing qubit that defines power (all operations conditional on this)
    @param acc_reg: QuantumRegister containing integer to shift
    @param power: int number of places to shift (if control_reg[power])"""
    ## NOTE: Power is the number of places to shift. Power 1 is controlled by
    ## control register's 2nd bit, which is control_reg[1]
    ## and refers to shift of 2^1, or shift one place
    
    # Flip all qubits in accumulator to allow ripple carry
#     for qubit in range(len(acc_reg)):
#         circuit.x(acc_reg[qubit])
        
    for target_bit in range(len(acc_reg) - 1):
        # shift bit by correct number of places
        circuit.ccx(control_reg[power], acc_reg[target_bit], acc_reg[target_bit + power])
        # Flip next bit if carry occurs
        for flipped_bit in range(target_bit, len(acc_reg) - 1):
            ## Carry occurs if target now 0 (if flip makes it 1).
            circuit.cx(control_reg[power], acc_reg[flipped_bit])
            circuit.ccx(control_reg[power], acc_reg[flipped_bit], acc_reg[flipped_bit + 1])
            circuit.cx(control_reg[power], acc_reg[flipped_bit])
            # Flip bit that's being shifted
            # circuit.cx(control_reg[power], acc_reg[target_bit])


# In[28]:


bit_shift_x_bits(qc, n_reg, m_reg, 1)
for index in range(len(n_reg)):
    qc.measure(n_reg[index], c_reg[index])
qc.draw()


# In[29]:


simulate = execute(qc, backend=backend, shots=1024).result()


# In[30]:


simulate.get_counts()


# In[6]:


print([x for x in range(9, 4, -1)])


# In[ ]:




