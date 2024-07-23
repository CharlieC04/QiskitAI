import math
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, execute, BasicAer
from qiskit.visualization import plot_histogram



# 4,0 -> 00
# 4,1 -> 01
# 4,2 -> 10
# 4,3 -> 11


# 4, 3 -> 11
# 2,3 -> 1,1
# 1,1 -> exit


def genvec(veclen, n):
    vec = []
    veclen = int(veclen/2)
    while veclen > 0:
        if veclen <= n:
            n = n - veclen
            vec.append(1)
        else:
            vec.append(0)
        
        veclen = int(veclen/2)
        vec.reverse()
    return vec


def convertToState(v): # converts from [0,0,1,0] to [1,0]
    # initializing the returning vector
    lenv = len(v)
    for i in range(lenv):
        if v[i] != 0:
            return genvec(lenv,i)
    return False
        
def mcts(circuit, controls, target, ancilla, activq):# multi cubit toffoli select
    for i in range(len(controls)):
        if activq[i] == 0:
            circuit.x(controls[i])
    circuit.mct(controls, target, ancilla, 'basic')
    for i in range(len(controls)):
        if activq[i] == 0:
            circuit.x(controls[i])

def all0(v):
    for e in v:
        if e != 0:
            return False
    return True

def fnon0(v):
    for e in v:
        if e != 0:
            return e
    return False

def vdeg(v):
    for i in range(len(v)):
        e = v[i]
        if e != 0:
            return i
    return False

def vecinfo(v):
    for i in range(len(v)):
        e = v[i]
        if e != 0:
            return [e,i]
    return False


def make_circuit(hamil):
    matlen = len(hamil)
    N = int(math.log(matlen,2))
    q1 = QuantumRegister(N)
    q2 = QuantumRegister(N)
    q3 = QuantumRegister(1)
    q4 = QuantumRegister(N)
    ancils = QuantumRegister(N)
    cr = ClassicalRegister(N)
    circuit = QuantumCircuit(q1,q2,q3,q4,ancils,cr)
    print(q1)
    # w
    for i in range(matlen):
        if all0(hamil[i]): 
            continue # if there is no correcponding state
        else:
            # find the target
            val = fnon0(hamil[i])
            targetLocation = genvec(matlen,val) # weight
            print(hamil[i],i,targetLocation)
            for j in range(N):# for each controlled output
                if targetLocation[j] == 1:
                    print(matlen,j,i)
                    mcts(circuit, q1, q4[j], ancils, genvec(matlen,i))
    circuit.barrier()
    print("b")
    # m
    for i in range(matlen):
        if all0(hamil[i]): 
            continue # if there is no correcponding state
        else:
            # find the target
            val = fnon0(hamil[i])
            targetLocation = convertToState(hamil[i]) # multiplication result
            print(hamil[i],i,targetLocation)
            for j in range(N):# for each controlled output
                if targetLocation[j] == 1:
                    print(matlen,j,i)
                    mcts(circuit, q1, q2[j], ancils, genvec(matlen,i))
    # f
    # -a
    # -m
    return circuit


make_circuit(
[
    [0,2,0,0],
    [2,0,0,0],
    [0,0,0,1],
    [0,0,1,0]
]
).draw(output = "mpl")

