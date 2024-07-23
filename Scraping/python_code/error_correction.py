import os, shutil
from qiskit import *
from qiskit.visualization import plot_histogram
from qiskit.visualization import circuit_drawer as drawer
import numpy as np
from matplotlib.pyplot import draw, plot, show

N = 1000 # number of circuits with random errors
p = 0.1 # error probability

LaTex_folder_Error_Correction = str(os.getcwd())+'/Latex_quantum_gates/Error_Correction/'
if not os.path.exists(LaTex_folder_Error_Correction):
    os.makedirs(LaTex_folder_Error_Correction)
else:
    shutil.rmtree(LaTex_folder_Error_Correction)
    os.makedirs(LaTex_folder_Error_Correction)

def ERROR_X(circuit, q):
    if(np.random.rand()<p):
        circuit.x(q)

def ERROR_Y(circuit, q):
    if(np.random.rand()<p):
        circuit.y(q)

def ERROR_Z(circuit, q):
    if(np.random.rand()<p):
        circuit.z(q)

def All_Errors(circuit, q):
    for qubit in q:
        ran = np.random.rand()
        if(ran < 1/3):
            ERROR_X(circuit, qubit)
        elif(ran < 2/3):
            ERROR_Y(circuit, qubit)
        else:
            ERROR_Z(circuit, qubit)
    
def Shor_error_correction(Circuit_FUNC, qr, qr_Shor):
    # This function creates the Shor error correction circuit
    # for a error-prone function Circuit_FUNC and its related
    # qubit(s) qr (qr_Shor are the ancilla qubits)
    # it returns this error corrected circuit
    
    qc_preprocess = QuantumCircuit(qr, qr_Shor)
    for i, qubit in enumerate(qr):
        qc_preprocess.cx(qubit, qr_Shor[8*i+2])
        qc_preprocess.cx(qubit, qr_Shor[8*i+5])
        
        qc_preprocess.h(qubit)
        qc_preprocess.h(qr_Shor[8*i+2])
        qc_preprocess.h(qr_Shor[8*i+5])
        
        qc_preprocess.cx(qubit, qr_Shor[8*i])
        qc_preprocess.cx(qubit, qr_Shor[8*i+1])
        qc_preprocess.cx(qr_Shor[8*i+2], qr_Shor[8*i+3])
        qc_preprocess.cx(qr_Shor[8*i+2], qr_Shor[8*i+4])
        qc_preprocess.cx(qr_Shor[8*i+5], qr_Shor[8*i+6])
        qc_preprocess.cx(qr_Shor[8*i+5], qr_Shor[8*i+7])
        #qc_preprocess.barrier()
    qc_preprocess.barrier()
    qc = qc_preprocess

    # apply main function (with possible errors) to qr 
    # and the error ancilla qubits
    Circuit_FUNC(qc, qr)
    for j in range(8):
        Circuit_FUNC(qc, qr_Shor[j:j+8*len(qr):8])
    qc.barrier()

    qc_postprocess = QuantumCircuit(qr,qr_Shor)
    for i, qubit in enumerate(qr):
        qc_postprocess.cx(qubit, qr_Shor[8*i])
        qc_postprocess.cx(qubit, qr_Shor[8*i+1])
        qc_postprocess.cx(qr_Shor[8*i+2], qr_Shor[8*i+3])
        qc_postprocess.cx(qr_Shor[8*i+2], qr_Shor[8*i+4])
        qc_postprocess.cx(qr_Shor[8*i+5], qr_Shor[8*i+6])
        qc_postprocess.cx(qr_Shor[8*i+5], qr_Shor[8*i+7])
        
        qc_postprocess.ccx(qr_Shor[8*i], qr_Shor[8*i+1], qubit)
        qc_postprocess.ccx(qr_Shor[8*i+3], qr_Shor[8*i+4], qr_Shor[8*i+2])
        qc_postprocess.ccx(qr_Shor[8*i+6], qr_Shor[8*i+7], qr_Shor[8*i+5])

        qc_postprocess.h(qubit)
        qc_postprocess.h(qr_Shor[8*i+2])
        qc_postprocess.h(qr_Shor[8*i+5])

        qc_postprocess.cx(qubit, qr_Shor[8*i+2])
        qc_postprocess.cx(qubit, qr_Shor[8*i+5])
        qc_postprocess.ccx(qr_Shor[8*i+2], qr_Shor[8*i+5], qubit)

        #qc_postprocess.barrier()
    
    qc = QuantumCircuit.compose(qc, qc_postprocess)
    return qc

## X-Error
print("X error")
for qubit in [0, 1]:
    answer_plot = {}
    print("|",qubit,'> : ',end='')
    for i in range(N):
        q = QuantumRegister(1,'q')
        q_Shor = QuantumRegister(8*len(q),'q_shor')
        c = ClassicalRegister(len(q), 'c')
        qc = QuantumCircuit(q,q_Shor, c)
        if(qubit):
            qc.x(q)
        qc_Shor = Shor_error_correction(ERROR_X, q, q_Shor)
        qc_Shor.barrier()
        qc_Shor = QuantumCircuit.compose(qc, qc_Shor)        
        qc_Shor.measure(q, c)

        # evaluate result
        simulator = Aer.get_backend('qasm_simulator')
        result = execute(qc_Shor, backend=simulator, shots=100).result()
        answer = result.get_counts()
        for measureresult in answer.keys():
            measureresults_input = measureresult
            if measureresults_input in answer_plot:
                answer_plot[measureresults_input] += answer[measureresult]
            else:
                answer_plot[measureresults_input] = answer[measureresult]
    # Plot the categorised results
    print(answer_plot)
    #plt = plot_histogram(answer_plot)
    #draw()
    #show(block=True)

LaTex_code = qc_Shor.draw(output='latex_source', initial_state=True, justify=None) # draw the circuit
f_name = 'Shor_error_correction_XERROR.tex'
with open(LaTex_folder_Error_Correction+f_name, 'w') as f:
            f.write(LaTex_code)

## Y-Error
print("Y error")
for qubit in [0, 1]:
    answer_plot = {}
    print("|",qubit,'> : ',end='')
    for i in range(N):
        q = QuantumRegister(1,'q')
        q_Shor = QuantumRegister(8*len(q),'q_shor')
        c = ClassicalRegister(len(q), 'c')
        qc = QuantumCircuit(q,q_Shor, c)
        if qubit:
            qc.x(q)
        qc.h(q) # y error is detected in Hadamard basis

        qc_Shor = Shor_error_correction(ERROR_Y, q, q_Shor) 
        qc_Shor.barrier()
        qc_Shor = QuantumCircuit.compose(qc, qc_Shor)

        qc_Shor.h(q) # y error is detected in Hadamard basis
            
        qc_Shor.measure(q, c)

        # evaluate result
        simulator = Aer.get_backend('qasm_simulator')
        result = execute(qc_Shor, backend=simulator, shots=100).result()
        answer = result.get_counts()
        for measureresult in answer.keys():
            measureresults_input = measureresult
            if measureresults_input in answer_plot:
                answer_plot[measureresults_input] += answer[measureresult]
            else:
                answer_plot[measureresults_input] = answer[measureresult]

    # Plot the categorised results
    print(answer_plot)
    #plt = plot_histogram(answer_plot)
    #draw()
    #show(block=True)

LaTex_code = qc_Shor.draw(output='latex_source', initial_state=True, justify=None) # draw the circuit
f_name = 'Shor_error_correction_YERROR.tex'
with open(LaTex_folder_Error_Correction+f_name, 'w') as f:
            f.write(LaTex_code)

## Z-Error
print("Z error")
for qubit in [0, 1]:
    answer_plot = {}
    print("|",qubit,'> : ',end='')
    for i in range(N):
        q = QuantumRegister(1,'q')
        q_Shor = QuantumRegister(8*len(q),'q_shor')
        c = ClassicalRegister(len(q), 'c')
        qc = QuantumCircuit(q,q_Shor, c)
        if qubit:
            qc.x(q)
        qc.h(q) # z error is detected in Hadamard basis
        qc_Shor = Shor_error_correction(ERROR_Z, q, q_Shor) 
        qc_Shor.barrier()
        qc_Shor = QuantumCircuit.compose(qc, qc_Shor)
        qc_Shor.h(q) # z error is detected in Hadamard basis
        qc_Shor.measure(q, c)

        # evaluate result
        simulator = Aer.get_backend('qasm_simulator')
        result = execute(qc_Shor, backend=simulator, shots=100).result()
        answer = result.get_counts()
        for measureresult in answer.keys():
            measureresults_input = measureresult
            if measureresults_input in answer_plot:
                answer_plot[measureresults_input] += answer[measureresult]
            else:
                answer_plot[measureresults_input] = answer[measureresult]
    # Plot the categorised results
    print(answer_plot)
    #plt = plot_histogram(answer_plot)
    #draw()
    #show(block=True)

LaTex_code = qc_Shor.draw(output='latex_source', initial_state=True, justify=None) # draw the circuit
f_name = 'Shor_error_correction_ZERROR.tex'
with open(LaTex_folder_Error_Correction+f_name, 'w') as f:
            f.write(LaTex_code)
## All three errors possible before CX-gate
print("CX with all error types")
for qubit1 in [0, 1]:
    for qubit2 in [0, 1]:
        print("|",qubit1,qubit2,'> : ',end='')
        answer_plot = {}
        for i in range(N):
            q = QuantumRegister(2,'q')
            c = ClassicalRegister(len(q), 'c')
            q_Shor = QuantumRegister(8*len(q),'q_shor')
            qc = QuantumCircuit(q, q_Shor, c)
            
            if(qubit1):
                qc.x(q[0])
            if(qubit2):
                qc.x(q[1])
            qc.barrier()

            qc_Shor = Shor_error_correction(All_Errors, q, q_Shor)
            qc_Shor.barrier()

            qc_Shor = QuantumCircuit.compose(qc, qc_Shor)
            qc_Shor.cx(q[0],q[1])
            for i, qubit in enumerate(reversed(q)):
                qc_Shor.measure(qubit, c[i])

            # evaluate result
            simulator = Aer.get_backend('qasm_simulator')
            result = execute(qc_Shor, backend=simulator, shots=10).result()
            answer = result.get_counts()
            for measureresult in answer.keys():
                measureresults_input = measureresult
                if measureresults_input in answer_plot:
                    answer_plot[measureresults_input] += answer[measureresult]
                else:
                    answer_plot[measureresults_input] = answer[measureresult]
        # Plot the categorised results
        print(answer_plot)
        plt = plot_histogram(answer_plot)
        draw()
        show(block=True)