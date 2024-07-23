import qiskit as qk
from qiskit import available_backends, get_backend, execute, register, least_busy
import numpy as np
from scipy.optimize import curve_fit
from qiskit.tools.qcvv.fitters import exp_fit_fun, osc_fit_fun, plot_coherence

qx_config = {
  "APItoken": 'dcdb2d9414a625c1f57373c544add3711c78c3d7faf39397fe2c41887110e8b59caf81bcb2bc32714d936da41a261fea510f96df379afcbdfa9df6cc6bfe3829',
    "url": 'https://quantumexperience.ng.bluemix.net/api'
}

#backend = 'local_qasm_simulator' # run on local simulator by default
register(qx_config['APItoken'], qx_config['url'])
backend = qk.get_backend('ibmqx4') # the device to run on
#backend = least_busy(available_backends({'simulator': False, 'local': False}))
#print("the best backend is " + backend)

# function for padding with QId gates
def pad_QId(circuit,N,qr):
    # circuit to add to, N = number of QId gates to add, qr = qubit reg
    for ii in range(N):
        circuit.barrier(qr)
        circuit.iden(qr)
    return circuit

shots = 1024    # the number of shots in the experiment
# Select qubit whose T1 is to be measured
qubit=1

# Creating registers
qr = qk.QuantumRegister(5)
cr = qk.ClassicalRegister(5)

# the delay times are all set in terms of single-qubit gates
# so we need to calculate the time from these parameters

params = backend.parameters['qubits'][qubit]
pulse_length=params['gateTime']['value'] # single-qubit gate time
buffer_length=params['buffer']['value'] # spacing between pulses
unit = params['gateTime']['unit']

steps=10
gates_per_step=120
max_gates=(steps-1)*gates_per_step+1
tot_length=buffer_length+pulse_length
time_per_step=gates_per_step*tot_length
qc_dict={}
for ii in range(steps):
    step_num='step_%s'%(str(ii))
    qc_dict.update({step_num:qk.QuantumCircuit(qr, cr)})
    qc_dict[step_num].x(qr[qubit])
    qc_dict[step_num]=pad_QId(qc_dict[step_num],gates_per_step*ii,qr[qubit])
    qc_dict[step_num].barrier(qr[qubit])
    qc_dict[step_num].measure(qr[qubit], cr[qubit])

circuits=list(qc_dict.values())

# run the program
status = backend.status
if status['operational'] == False or status['pending_jobs'] > 10:
    print('Warning: the selected backend appears to be busy or unavailable at present; consider choosing a different one if possible')
t1_job=qk.execute(circuits, backend, shots=shots)

# arrange the data from the run
result_t1 = t1_job.result()
keys_0_1=list(result_t1.get_counts(qc_dict['step_0']).keys())# get the key of the excited state '00001'

data=np.zeros(len(qc_dict.keys())) # numpy array for data
sigma_data = np.zeros(len(qc_dict.keys()))

# change unit from ns to microseconds
plot_factor=1
if unit.find('ns')>-1:
    plot_factor=1000
    punit='$\mu$s'
xvals=time_per_step*np.linspace(0,len(qc_dict.keys()),len(qc_dict.keys()))/plot_factor # calculate the time steps in microseconds

for ii,key in enumerate(qc_dict.keys()):
    # get the data in terms of counts for the excited state normalized to the total number of counts
    data[ii]=float(result_t1.get_counts(qc_dict[key])[keys_0_1[1]])/shots
    sigma_data[ii] = np.sqrt(data[ii]*(1-data[ii]))/np.sqrt(shots)

# fit the data to an exponential
fitT1, fcov = curve_fit(exp_fit_fun, xvals, data, bounds=([-1,2,0], [1., 500, 1]))
ferr = np.sqrt(np.diag(fcov))

plot_coherence(xvals, data, sigma_data, fitT1, exp_fit_fun, punit, 'T$_1$ ', qubit)

print("a: " + str(round(fitT1[0],2)) + u" \u00B1 " + str(round(ferr[0],2)))
print("T1: " + str(round(fitT1[1],2))+ " µs" + u" \u00B1 " + str(round(ferr[1],2)) + ' µs')
print("c: " + str(round(fitT1[2],2)) + u" \u00B1 " + str(round(ferr[2],2)))