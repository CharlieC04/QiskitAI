#!/usr/bin/env python
# coding: utf-8

# In[1]:


from qiskit import *
from qiskit.quantum_info import Statevector

#From Marc
from parser import QSerializer

#From Luca
import socket
from SocketChannel import SocketChannel


# In[33]:


class Channel:    
    def __init__(self,slave_offset=0):
        self._state_vector = None
        self._arr_qubits = None
        self._basis_gates = ['u1', 'u2', 'u3', 'cx','x','y','H','z']
        self._master = True
        self._offset = 0
        self._slave_offset = slave_offset
        
    def send(self,circuit,arr_qubits):
        self._state_vector = Statevector.from_instruction(circuit)  
        self._arr_qubits = arr_qubits
       
        #From Marc
        ser = parser.QSerializer()
        ser.add_element('channel_class', self)
        str_to_send = ser.encode()

        #From Luca
        message = str_to_send
        TCP_IP = '127.0.0.1'

        channel = SocketChannel()
        channel.connect(TCP_IP, 5005)

        channel.send(message)
        #channel.close()
        
        ## TODO: TCP THINGS
        return self
        
    def receive(self,circuit)#,recieve_channel):  ## TODO: remove recieve as an input
        #TODO: TCP things
        #recieve_channel = TCP_STUFF
        
        #From Luca
        channel = SocketChannel(port=5005, listen=True)
        data = channel.receive()
        print("received data:", data)
        #channel.close()
        
        #From Marc
        ser2 = parser.QSerializer()
        ser2.decode(data)
        recieve_channel = ser2.get_element('channel_class')
        
        self._slave_offset = recieve_channel._slave_offset
        if(recieve_channel._master):
            self._master = False
            self._offset = self._slave_offset
        
        new_circuit = QuantumCircuit(len(recieve_channel._state_vector.dims()))
        new_circuit.initialize(recieve_channel._state_vector.data, range(len(recieve_channel._state_vector.dims())))
        new_circuit = transpile(new_circuit, basis_gates=self._basis_gates)
        return new_circuit, self._offset   


# In[34]:



n_master = 2
n_slave = 1
master_offset = 0
slave_offset = n_master



circ = QuantumCircuit(n_master + n_slave)



channel = Channel(slave_offset)

## Master
circ.h(0 + channel._offset)
#circ.cx(0 + channel._offset, 1  + channel._offset)
#irc.h(1 + channel._offset)


to_tpc = channel.send(circ,[1])  ## TODO: remove
circ.draw()


# In[35]:


#Bob Part
circ_bob = QuantumCircuit(3)

bob_channel = Channel()
circ_bob, offset = bob_channel.receive(circ_bob)#,to_tpc)
circ_bob.draw()


# In[11]:


# Initialize circ-2 in state psi (using transpile to remove reset)
#circ2 = QuantumCircuit(2)
#circ2.initialize(psi1.data, [0, 1])
#circ2 = transpile(circ2, basis_gates=basis_gates)
#circ2.draw()


# In[6]:


# Add new gates to circ2
circ_bob.h(0+offset)
#circ_bob.cx(0+offset, 1+offset)
#psi2 = Statevector.from_instruction(circ_bob)

to_tpc = bob_channel.send(circ_bob,[1])
circ_bob.draw()


# In[7]:


#Alice Part
circ_alice = QuantumCircuit(3)

alice_channel = Channel()
circ_alice , offset = alice_channel.receive(circ_alice,to_tpc)
circ_alice.draw()


# In[8]:


_

