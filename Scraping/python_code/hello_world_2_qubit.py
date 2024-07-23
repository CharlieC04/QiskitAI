from qiskit import QuantumCircuit 
import matplotlib.pyplot as plt

qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0,1)

# qc.draw('mpl',style='iqp')
# plt.show()


from qiskit.quantum_info import Pauli
ZZ = Pauli('ZZ')
ZI = Pauli('ZI')
IZ = Pauli('IZ')
XX = Pauli('XX')
XI = Pauli('XI')
IX = Pauli('IX')

observables = [ZZ,ZI,IZ,XX,XI,IX]

#execute

from qiskit_aer.primitives import Estimator

estimator = Estimator()

job = estimator.run([qc]*len(observables),observables)
# print(job.result())

#plotting

data = ['ZZ', 'ZI', 'IZ', 'XX', 'XI', 'IX']
values = job.result().values
plt.plot(data,values,'-o')
plt.xlabel('Observables')
plt.ylabel('Expected values')
plt.show()

