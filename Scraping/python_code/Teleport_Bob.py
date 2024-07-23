from qiskit import *
import matplotlib.pyplot as plt

from channel_class import Channel

#Bob Part
circ_bob = QuantumCircuit(3)

#circ_bob.h(0)
#circ_bob.draw(output='mpl','test.png')

bob_channel = Channel(myport = 5001, remote_port = 5000)
circ_bob, offset = bob_channel.receive(circ_bob)#,to_tpc)

# Add new gates to circ2
circ_bob.cx(-1+offset,0+offset)
circ_bob.cz(-2+offset,0+offset)

circ_bob.rx(-0.1,0 + offset)
circ_bob.ry(-0.94,0 + offset)
circ_bob.rz(-0.54,0 + offset)
circ_bob.rx(-0.234,0 + offset)

circ_bob.draw(output='mpl',filename='teleport_bob.png')


#check the teleported state:
from qiskit import Aer
backend = Aer.get_backend('statevector_simulator')
job = execute(circ_bob,backend)
result = job.result()
outputstate = result.get_statevector(circ_bob,decimals=3)
print(outputstate)


meas = QuantumCircuit(3,1)
meas.barrier(range(3))
meas.measure([2],range(1))
qc = circ_bob + meas

#channel.send(qc)

backend_sim = Aer.get_backend('qasm_simulator')
job_sim = execute(qc,backend_sim,shots=1024)
result_sim = job_sim.result()
counts = result_sim.get_counts(qc)
print(counts)

