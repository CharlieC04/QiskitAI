from qiskit import *
import matplotlib.pyplot as plt

from channel_class import Channel

#Bob Part
circ_bob = QuantumCircuit(3)

bob_channel = Channel(myport = 5001, remote_port = 5000)
#circ_bob.h(0)
#circ_bob.draw(output='mpl','test.png')

circ_bob, offset = bob_channel.receive(circ_bob)#,to_tpc)

# Add new gates to circ2
circ_bob.x(0+offset)
#circ_bob.cx(0+offset, 1+offset)
#psi2 = Statevector.from_instruction(circ_bob)

import time
time.sleep(2)
to_tpc = bob_channel.send(circ_bob,[1])
circ_bob.draw()

