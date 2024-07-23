import numpy as np
import os
import datetime
import time
import pickle
from qiskit import *
from qiskit.providers.jobstatus import JOB_FINAL_STATES, JobStatus

def start_or_retrieve_job(filename, backend, circuit=None, options=None):
    """function that
       1) retrieves the job from the backend if saved to file,
       2) or executes a job on a backend and saves it to file

    Parameters
    ----------
    filename : string
        The filename to write/read from. The extension ".job" is
        automatically appended to the string.

    backend : qiskit.providers.ibmq.ibmqbackend.IBMQBackend
        The backend where the job has been/is to be executed.

    circuit : qiskit.circuit.quantumcircuit.QuantumCircuit, optional
        The circuit that is to be executed.

    options: dict, optional
        The following is a list of all options and their default value
        options={'shots': 1024, 'forcererun': False, 'useapitoken': False, 'directory': 'jobs'}
        the directory is created if it does not exist

    Returns
    -------
    job : qiskit.providers.ibmq.job.ibmqjob.IBMQJob,
          qiskit.providers.aer.aerjob.AerJob
        

    """
    ### options parsing
    if options == None:
        options={}
    shots = options.get('shots', 1024)
    forcererun = options.get('forcererun', False)
    useapitoken = options.get('useapitoken', False)
    directory = options.get('directory', 'jobs')

    filename = filename+'.job'
    if not os.path.exists(directory):
        os.makedirs(directory)

    if not(forcererun) and os.path.isfile(directory+'/'+filename):
        #read job id from file and retrieve the job
        with open(directory+'/'+filename, 'r') as f:
            apitoken = f.readline().rstrip()
            backendname = f.readline().rstrip()
            job_id = f.readline().rstrip()
        if useapitoken:
            IBMQ.save_account(apitoken, overwrite=True)
            IBMQ.load_account()
            provider = IBMQ.get_provider(hub='ibm-q')
            backend_tmp = provider.get_backend(backendname)
            if backend.name() != backend_tmp.name():
                raise Exception("The backend of the job was "+backend_tmp.name()+", but you requested "+backend.name())
            job = backend_tmp.retrieve_job(job_id)
        else:
            job = backend.retrieve_job(job_id)
    else:
        # otherwise start the job and write the id to file
        hasnotrun = True
        while hasnotrun:
            error = False
            try:
                job = execute(circuit, backend, shots=int(shots))
            except Exception as e:
                error = True
                sec  = 60
                if "Error code: 3458" in str(e):
                    print(filename +' No credits available, retry in '+str(sec)+' seconds'+', time='+str(datetime.datetime.now()), end='\r')
                else:
                    print('{j} Error! Code: {c}, Message: {m}, Time {t}'.format(j=str(filename), c = type(e).__name__, m = str(e), t=str(datetime.datetime.now())), ", retry in ",str(sec),' seconds', end='\r')
                time.sleep(sec)
            if not(error):
                hasnotrun = False
        job_id = job.job_id()
        apitoken = IBMQ.active_account()['token']
        backendname = backend.name()
        if job_id != '':
            file = open(directory+'/'+filename,'w')
            file.write(apitoken+'\n')
            file.write(backendname+'\n')
            file.write(job_id)
            file.close()
    return job

def write_results(filename, job, options=None):
    """function that writes the results of a job to file

    Parameters
    ----------
    filename : string
        The filename to write to. The extension ".result" is
        automatically appended to the string.

    job : qiskit.providers.ibmq.job.ibmqjob.IBMQJob,
          qiskit.providers.aer.aerjob.AerJob
        The job to get the results from

    options: dict, optional
        The following is a list of all options and their default value
        options={'overwrite': False, 'directory': 'results'}

    Returns
    -------
    success : bool
        set to True if the results from the job are written to file
        it is set to False, e.g., if the job has not yet finished successfully

    """
    ### options parsing
    if options == None:
        options={}
    overwrite = options.get('overwrite', False)
    directory = options.get('directory', 'results')

    filename=filename+'.result'
    if not os.path.exists(directory):
        os.makedirs(directory)

    success = False
    fileexists = os.path.isfile(directory+'/'+filename)
    if (fileexists and overwrite) or not(fileexists):
        jobstatus = job.status()
        if jobstatus == JobStatus.DONE:
            res=job.result().results
            tmpfile = open(directory+'/'+filename,'wb')
            pickle.dump(res,tmpfile)
            tmpfile.close()
            success = True
    return success

def read_results(filename, options=None):
    """function that reads results from file

    Parameters
    ----------
    filename : string
        The filename to read from. The extension ".result" is
        automatically appended to the string.

    options: dict, optional
        The following is a list of all options and their default value
        options={'directory': 'results'}

    Returns
    -------
    results : Object
        the form is dictated by job.result().results
        can be None, if the file does not exist

    success : bool
        set to True if the results 

    """
    ### options parsing
    if options == None:
        options={}
    directory = options.get('directory', 'results')

    filename=filename+'.result'

    results = None
    if os.path.isfile(directory+'/'+filename):
        tmpfile = open(directory+'/'+filename,'rb')
        results=pickle.load(tmpfile)
        tmpfile.close()
    return results

def get_id_error_rate(backend):
    errorrate=[]
    gates=backend.properties().gates
    for i in range(0,len(gates)):
        if getattr(gates[i],'gate') == 'id':
            gerror = getattr(getattr(gates[i],'parameters')[0], 'value')
            errorrate.append(gerror)
    return errorrate

def get_U3_error_rate(backend):
    errorrate=[]
    gates=backend.properties().gates
    for i in range(0,len(gates)):
        if getattr(gates[i],'gate') == 'u3':
            gerror = getattr(getattr(gates[i],'parameters')[0], 'value')
            errorrate.append(gerror)
    return errorrate

def get_T1(backend):
    val=[]
    unit=[]
    gates=backend.properties().gates
    for i in range(backend.configuration().n_qubits):
        qubit=backend.properties().qubits[i][0]
        assert qubit.name == 'T1'
        val.append(qubit.value)
        unit.append(qubit.unit)
    return val, unit

def get_T2(backend):
    val=[]
    unit=[]
    gates=backend.properties().gates
    for i in range(backend.configuration().n_qubits):
        qubit=backend.properties().qubits[i][1]
        assert qubit.name == 'T2'
        val.append(qubit.value)
        unit.append(qubit.unit)
    return val, unit

def get_readouterrors(backend):
    val=[]
    gates=backend.properties().gates
    for i in range(backend.configuration().n_qubits):
        qubit=backend.properties().qubits[i][3]
        assert qubit.name == 'readout_error'
        val.append(qubit.value)
    return val

def get_prob_meas0_prep1(backend):
    val=[]
    gates=backend.properties().gates
    for i in range(backend.configuration().n_qubits):
        qubit=backend.properties().qubits[i][4]
        assert qubit.name == 'prob_meas0_prep1'
        val.append(qubit.value)
    return val

def get_prob_meas1_prep0(backend):
    val=[]
    gates=backend.properties().gates
    for i in range(backend.configuration().n_qubits):
        qubit=backend.properties().qubits[i][5]
        assert qubit.name == 'prob_meas1_prep0'
        val.append(qubit.value)
    return val

def get_cx_error_map(backend):
    """
    function that returns a 2d array containing CX error rates.
    """
    num_qubits=backend.configuration().n_qubits
    two_qubit_error_map = np.zeros((num_qubits,num_qubits))
    backendproperties=backend.properties()
    gates=backendproperties.gates
    for i in range(0,len(gates)):
        if getattr(gates[i],'gate') == 'cx':
            cxname = getattr(gates[i],'name')
            error = getattr(getattr(gates[i],'parameters')[0], 'value')
            #print(cxname, error)
            for p in range(num_qubits):
                for q in range(num_qubits):
                    if p==q:
                        continue
                    if cxname == 'cx'+str(p)+'_'+str(q):
                        two_qubit_error_map[p][q] = error
                        break
    return two_qubit_error_map

def getNumberOfControlledGates(circuit):
    """function that returns the number of CX, CY, CZ gates.
       N.B.: swap gates are counted as 3 CX gates.
    """
    numCx=0
    numCy=0
    numCz=0
    for instr, qargs, cargs in circuit.data:
        gate_string = instr.qasm()
        if gate_string == "swap":
            numCx += 3
        elif gate_string == "cx":
            numCx += 1
        elif gate_string == "cy":
            numCy += 1
        elif gate_string == "cz":
            numCz += 1
    return numCx, numCy, numCz

def convert_to_binarystring(results):
    list=[]
    for item in range(0,len(results)):
        dict={}
        co = results[item].data.counts
        for i in range(0,2**5):
            if(hasattr(co,hex(i))):
                binstring="{0:b}".format(i).zfill(5)
                counts = getattr(co, hex(i))
                dict[binstring] = counts
        list.append(dict)
    return list


