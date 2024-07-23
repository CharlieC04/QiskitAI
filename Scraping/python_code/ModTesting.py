from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, execute, Aer, IBMQ
from qiskit.compiler import transpile, assemble
from qiskit.tools.jupyter import *
from qiskit.visualization import *
from datetime import datetime

backend = Aer.get_backend("qasm_simulator")

global n_reg # = QuantumRegister(6, 'n')
global scratch_a
global class_reg # = ClassicalRegister(6, 'y')

global qc # = QuantumCircuit(n_reg, m_reg, scratch_a, class_reg)

test_timestamp = datetime.now()

from ArithmaticFunctions import *

def setup_each_addition():
    n_reg = QuantumRegister(6, 'n')
    m_reg = QuantumRegister(6, 'm')
    scratch_a = QuantumRegister(6, 'sca')
    scratch_b = QuantumRegister(6, 'scb')
    class_reg = ClassicalRegister(6, 'y')
    qc = QuantumCircuit(n_reg, m_reg, scratch_a, scratch_b, class_reg)
    
    return {'n_reg': n_reg, 'm_reg': m_reg, 'scratch_a': scratch_a, 'scratch_b': scratch_b, 'class_reg': class_reg, 'qc': qc }

# def get_results_of_last_test():
# #     for bit in range(len(n_reg)):
# #         qc.measure(n_reg[bit], class_reg[bit])
# 	simulate = execute(qc, backend=backend, shots=1024).result()
    return simulate.get_counts()

def verify_results(expected):
    
    if [expected] == list(results.keys()):
        print("PASSING - ", test_timestamp)
    else:
        print("FAILING - ", test_timestamp)
        print(f'Got - {results}')
    
tc = setup_each_addition()
qc = tc['qc']

qc.x(tc['m_reg'][0])
qc.x(tc['m_reg'][2])

qc.x(tc['n_reg'][3])

mod_reduce(circuit=qc, mod_reg=tc['m_reg'], base_reg=tc['n_reg'], scratch_carry=tc['scratch_a'], scratch_unadd=tc['scratch_b'] )
qc.measure(tc['n_reg'], tc['class_reg'])
simulate = execute(qc, backend=backend, shots=1024).result()
print(simulate.get_counts())
