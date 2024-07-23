from qiskit import QuantumProgram
import Qconfig

import sys

qp = QuantumProgram()
qp.set_api(Qconfig.APItoken, Qconfig.config['url']) # set the APIToken and API url

# set up registers and program
qr = qp.create_quantum_register('qr', 16)
cr = qp.create_classical_register('cr', 16)
qc = qp.create_circuit('smiley_writer', [qr], [cr])

# rightmost eight (qu)bits have ')' = 00101001
qc.x(qr[0])
qc.x(qr[3])
qc.x(qr[5])

# second eight (qu)bits have superposition of
# '8' = 00111000
# ';' = 00111011
# these differ only on the rightmost two bits
qc.h(qr[9]) # create superposition on 9
qc.cx(qr[9],qr[8]) # spread it to 8 with a cnot
qc.x(qr[11])
qc.x(qr[12])
qc.x(qr[13])

# measure
for j in range(16):
  qc.measure(qr[j], cr[j])

backend = 'ibmqx_qasm_simulator'

if len(sys.argv) > 1:
  backend = sys.argv[1]

# run and get results
print('Executing..')
results = qp.execute(['smiley_writer'], backend, shots=1024)


print('waiting for results')
stats = results.get_counts('smiley_writer')

print(stats)
