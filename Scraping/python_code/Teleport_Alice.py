from qiskit import *

from channel_class import Channel

n_master = 2  # two qubits, the one on alice side
n_slave = 1 # two quantum channels and one qubit on bobs side
master_offset = 0
slave_offset = n_master

circ = QuantumCircuit(n_master + n_slave)

channel = Channel(slave_offset, 5000, remote_port = 5001)

## Master, Oracle
circ.rx(0.234,0 + channel._offset)
circ.rz(0.54,0 + channel._offset)
circ.ry(0.94,0 + channel._offset)
circ.rx(0.1,0 + channel._offset)

##Creating Entaglement
circ.h(1+channel._offset)
circ.cx(1+channel._offset,2+channel._offset)

## Master, teleportation protocol
circ.cx(0 + channel._offset, 1  + channel._offset)
circ.h(0 + channel._offset)

# this should be done with classical communication ...
#circ.cx(0 + channel._offset, 2 + channel._offset)
#circ.cx(1 + channel._offset, 3 + channel._offset)

channel.send(circ,[1])  ## TODO: remove

circ.draw(output='mpl',filename='teleport_alice.png')

