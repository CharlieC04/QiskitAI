'''
This program sets up the circuits for the randamised benchmarking routine
'''

import qiskit
import numpy as np
import os, shutil
import matplotlib.pyplot as plt
from matplotlib.pyplot import draw, show
import qiskit.ignis.verification.randomized_benchmarking as rb
from qiskit_aer.noise import NoiseModel
from qiskit_aer.noise.errors.standard_errors import depolarizing_error, thermal_relaxation_error

os.environ["QT_QPA_PLATFORM"] = "xcb" # for Linux only

folder_RBM = os.getcwd()+'/RBM/'
if not os.path.exists(folder_RBM):
    os.makedirs(folder_RBM)
else:
    shutil.rmtree(folder_RBM)
    os.makedirs(folder_RBM)

## Generate RB circuits (2Q RB)
# number of qubits
nQ=3 
rb_opts = {}
# Number of Cliffords in the sequence
rb_opts['length_vector'] = [1, 10, 20, 50, 75, 100, 125, 150, 175, 200]
# Number of seeds (random sequences)
rb_opts['nseeds'] = 5
# Default pattern
rb_opts['rb_pattern'] = [ [0, 1, 2] ]

rb_circs, xdata = rb.randomized_benchmarking_seq(**rb_opts)
print(len(rb_circs))
for i in range(len(rb_circs)):
    for n, circuit in enumerate(rb_circs[i]):
        filename = str(folder_RBM+'seed_'+str(i)+'_m_'+str(rb_opts['length_vector'][n]+1)+'.qasm')
        circuit.qasm(filename=filename)

# Run on a noisy simulator
noise_model = NoiseModel()

# Depolarizing error on the gates u2, u3 and cx (assuming the u1 is virtual-Z gate and no error)
p1Q = 0.002
p2Q = 0.01

noise_model.add_all_qubit_quantum_error(depolarizing_error(p1Q, 1), 'u2')
noise_model.add_all_qubit_quantum_error(depolarizing_error(2 * p1Q, 1), 'u3')
noise_model.add_all_qubit_quantum_error(depolarizing_error(p2Q, 2), 'cx')

backend = qiskit.Aer.get_backend('qasm_simulator')

# Create the RB fitter
backend = qiskit.Aer.get_backend('qasm_simulator')
basis_gates = ['u1','u2','u3','cx'] 
shots = 200
transpiled_circs_list = []
rb_fit = rb.RBFitter(None, xdata, rb_opts['rb_pattern'])
for rb_seed, rb_circ_seed in enumerate(rb_circs):
    print('Compiling seed %d'%rb_seed)
    new_rb_circ_seed = qiskit.compiler.transpile(rb_circ_seed, basis_gates=basis_gates)
    transpiled_circs_list.append(new_rb_circ_seed)
    print('Simulating seed %d'%rb_seed)
    ## THIS ONE IS FROM OUR RESULTS NOT THE BACKEND
    job = qiskit.execute(new_rb_circ_seed, 
                         backend, 
                         shots=shots,
                         noise_model=noise_model)    
    
    # Add data to the fitter
    rb_fit.add_data(job.result())
    print('After seed %d, alpha: %f, EPC: %f'%(rb_seed,rb_fit.fit[0]['params'][1], rb_fit.fit[0]['epc']))    

plt.figure(figsize=(8, 6))
ax = plt.subplot(1, 1, 1)

# Plot the essence by calling plot_rb_data
rb_fit.plot_rb_data(0, ax=ax, add_label=True, show_plt=False)
    
# Add title and label
ax.set_title('%d Qubit RB'%(nQ), fontsize=18)

plt.show()