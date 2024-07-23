#General Imports
import numpy as np
import matplotlib.pyplot as plt
import time
from itertools import product,permutations
from string import ascii_lowercase as asc
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 

#Qiskit Imports
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, Aer, transpile
from qiskit.circuit.library.standard_gates import MCXGate, CXGate, XGate, CSwapGate
from qiskit.circuit.library import Diagonal
from qiskit.quantum_info import partial_trace,purity


#############FUNCTIONS###########################################################################################################

#wrapper for measuring time taken by function 'func' 
def timeis(func):
    def wrap(*args,**kwargs):
        start = time.time()
        result = func(*args,**kwargs)
        end = time.time()
        if measure_time:
            print("{} took {:.2f}s".format(func.__name__,end-start))
        return result
    return wrap

#check if inputs are valid
def check_inputs(n,m):
    if n == 1:
        print("Case n=1 currently not supported")
    correct = 1
    if m>2**n:
        correct == 0

    if correct == 1:
        print("Inputs valid")
    return 0

#initialize quantum circuit with electron register, swap_ancillas, record_ancillas, collision_ancillas
def initialize_circuit(n,m,L):
    circuit = QuantumCircuit()
    #add main electron register (seed/target)
    for e in range(m):
        r_q = QuantumRegister(n,'{}'.format(asc[e]))#asc[i]=ith letter of the alphabe
        c = QuantumCircuit(r_q)
        circuit = circuit.combine(c)

    #add ancillas for comparator_swaps
    for k in range(int(np.ceil(m/2))):
        anc_q  = QuantumRegister(n-1,'anc_{}'.format(k))
        c = QuantumCircuit(anc_q)
        circuit = circuit.combine(c)

    #add 'record' register for storing outcomes of comparators
    for l in range(L):
        anc_q = QuantumRegister(1,'record_{}'.format(l))
        c = QuantumCircuit(anc_q)
        circuit = circuit.combine(c)

    #add ancillas to store the occurence of collisions between pairs of electrons
    for c in range(m-1):
        anc_q = QuantumRegister(1,'coll_record_{}'.format(c))
        c = QuantumCircuit(anc_q)
        circuit = circuit.combine(c)

    #add one ancilla to store if all other collision ancillas are '1' 
    anc_q = QuantumRegister(1,'collision_test')
    c = QuantumCircuit(anc_q)
    circuit = circuit.combine(c)

    return circuit

#returns x in binary format as string of length n, incl leading zeros
def binary_n(x,n):
    return bin(x)[2:].zfill(n)

#initializes j-th electron register with number x
def binary_init(circuit,n,m,input):
    for k,e in enumerate(input):
        e_bin = binary_n(e,n)
        for i in range(n):
            if e_bin[i]=='1':
                circuit.append(XGate(),[i+k*n])

    return circuit

#Apply a Hadamard gate to each qubit in the electron register
def Hadamard(circuit,n,m):
    for q in range(n*m):
        circuit.h(q)
    return circuit

#Compare bits at positions x and y, only output=(x<y) to position anc
def bit_compare(circuit,cbits,control,debug=True):
    x = cbits[0]
    y = cbits[1]
    anc = cbits[2]
    
    if debug:
        circuit.barrier()

    #control='01' for initial sorting and '10' for collision detection
    circuit.append(MCXGate(2,ctrl_state=control),[x,y,anc])
    
    if debug:
        circuit.barrier()
    return circuit

#split the array 'index' into array of pairs of adjacent indices; first entry is (e.g.) [0] if number of entries of index is odd
def get_subsets(index):
    #index = [0,1,2,3]   ->  result = [[0,1],[2,3]]
    #index = [0,1,2,3,4] ->  result = [[0],[1,2],[3,4]]
    M = len(index)
    result = []
    if M % 2 != 0:
        result.append(np.array([0]))
        n_split = int((M-1)/2)
        for s in np.split(index[1:M],n_split):
            result.append(s)
    else:
        result = np.split(index,M/2)
    return result

#get position of first qubit in swap_control ancilla register
def get_first_swap_ctrl(n,m):
    #n_comp_parallel is the number of comparators that are applied in each layer
    #n*m = main register for storing electron registers; 
    #(n_comp_parallel)*(n-1) = fixed ancilla register needed for compare_n 
    n_comp_parallel = int(np.ceil(m/2))
    ctrl_0 = n*m +  (n-1)*n_comp_parallel
    return ctrl_0

#get position of first qubit in collision_control ancilla register
def get_first_coll_ctrl(n,m,L):
    coll_0 = get_first_swap_ctrl(n,m) + L
    return coll_0

#return pairs of electron indices that need to be compared in collision-detection step
def get_coll_sets(m):
    ind = np.arange(m)

    if m == 2:
        sets_a = [np.array([0,1])]
        sets_b = []
        return sets_a,sets_b
    
    if m % 2 == 0:
        sets_a = np.split(ind,m/2)
        sets_b = np.split(ind[1:-1],(m-2)/2)
    else:
        sets_a = np.split(ind[:-1],(m-1)/2)
        sets_b = np.split(ind[1:],(m-1)/2)

    #all gates in sets_a can be applied in parallel
    #all gates in sets_b can be applied in parallel

    return sets_a,sets_b

#returns the first qubit position of the ancilla register used for swap of i and j (only really tested for m<6)
def get_anc(n,m,i,j):
    if abs(j-i) == 1:
        anc_reg = int( np.min([i,j])/2 )
    elif abs(j-i) == 2:
        anc_reg = int( np.ceil( np.min([i,j])/2 ))
    else:
        anc_reg = int( np.min([i,j]) )

    anc = n*m + anc_reg*(n-1)
    return anc

#Implement 'Compare2' function (Fig 3); input: two 2bit numbers, output: two 1bit numbers with same ordering
def compare_2(circuit,x_0,x_1,y_0,y_1,anc):
    #Notation: x = 2^1*x_0 + x_1  (reverse from paper!!)
    #compares numbers x,y and outputs two bits x',y' (at positions x_1 and y_1) with the same ordering
    circuit.append(XGate(),[anc])
    circuit.append(CXGate(),[y_0,x_0])
    circuit.append(CXGate(),[y_1,x_1])
    circuit.append(CSwapGate(),[x_0,x_1,anc])
    circuit.append(CSwapGate(),[x_0,y_0,y_1])
    circuit.append(CXGate(),[y_1,x_1])
    
    return circuit

#Generalisation of 'compare2' two nbit numbers, output: two 1bit numbers with same ordering at positions x1,y1
def compare_n(circuit,n,m,i,j,l,L,debug):
     
    index = np.arange(n)
    subsets = get_subsets(index)
    M = len(subsets)
    anc = get_anc(n,m,i,j)
    for s in subsets:
        if len(s)==2:
            if debug:
                circuit.barrier()

            x_0 = s[0] + i*n
            x_1 = s[1] + i*n
            y_0 = s[0] + j*n
            y_1 = s[1] + j*n
            circuit = compare_2(circuit,x_0,x_1,y_0,y_1,anc)
            anc += 1
    while (len(subsets)>1):
        index = np.array([subsets[k][-1] for k in range(M)])
        subsets = get_subsets(index)
        M = len(subsets)
        
        for s in subsets:
            if len(s)==2:
                if debug:
                    circuit.barrier()
        
                x_0 = s[0] + i*n
                x_1 = s[1] + i*n
                y_0 = s[0] + j*n
                y_1 = s[1] + j*n
                circuit = compare_2(circuit,x_0,x_1,y_0,y_1,anc)
                anc += 1       
    ########################################################################################################################################
    #at this point the bits x_1 and y_1 have the same ordering as numbers stored in registers i and j
    #e(i)<e(j) ->    x_1=0 and y_1=1                             
    #e(i)>e(j) ->    x_1=1 and y_1=0                             
    #e(i)=e(j) ->    x_1=0 y_1=0 if e(i) even or x_1=1 y_1=1 if e(i) odd   

    #prepare output for bit_compare function; anc iterates through the second ancilla register (+1 for each comparator)
    #l = current swap; each new swap gets a new ancilla for storing the outcome
    
    anc = get_first_swap_ctrl(n,m) + l 
    cbits = x_1,y_1,anc

    return circuit,cbits

#apply diagonal phase shift to qubit i, conditioned on qubit 'ctrl'
def cphase_shift(circuit,ctrl,i):
    target = i*n
    CDiag = Diagonal([-1,-1]).control(1)
    CDiag = CDiag.to_gate()
    CDiag.label = "D" #doesn't work currently
    circuit.append(CDiag,[ctrl,target])
    return circuit

#performs swap of registers i and j conditioned on ancilla qubit 'ctrl' 
def swap_registers(circuit,n,i,j,ctrl,debug):
    for g in range(n):
        circuit.append(CSwapGate(),[ctrl,i*n+g,j*n+g])
    if debug:
        circuit.barrier()

    return circuit

#compare electron registers i and j; swap registers iff e(i)<(j); l=current swap (0 to L)
def comparator_swap(n,m,i,j,l,L,phase,debug):
    
    #Perform comparison to generate output qubits "cbits"
    circuit_compute = initialize_circuit(n,m,L)
    circuit_compute,cbits = compare_n(circuit_compute,n,m,i,j,l,L,debug)

    #Add bit_compare between the two output qubits and store in ancilla
    circuit_bit_compare = initialize_circuit(n,m,L)
    circuit_bit_compare = bit_compare(circuit_bit_compare,cbits,'10',debug)
    
    #add uncomputing step only of the comparison circuit
    circuit_uncompute = circuit_compute.inverse()
    
    #Swap registers based on control ancilla 
    circuit_swap = initialize_circuit(n,m,L)
    #apply a conditioned phase shift to the first qubit of the register pair; is only called when sn is applied backwards, that's why it's (phase,swap) and not (swap,phase)
    if phase:
        circuit_swap = cphase_shift(circuit_swap,cbits[2],i)

    circuit_swap = swap_registers(circuit_swap,n,i,j,cbits[2],debug)

    #Combine circuits
    circuit_comparator = circuit_compute + circuit_bit_compare + circuit_uncompute + circuit_swap

    return circuit_comparator

#Apply the sorting network sn, where each comparator stores the outcome in ctrl_register
def apply_sorting_network(circuit,n,m,sn,L,phase,debug):
    for l,swap in enumerate(sn):
        #swap = [i, j, direction]; dir = 0 : descending (from the top); dir = 1 : ascending (from the top)
        if swap[2]==0:
            i = swap[0]
            j = swap[1]
        if swap[2]==1:
            i = swap[1]
            j = swap[0]

        circuit_comparator = comparator_swap(n,m,i,j,l,L,phase,debug)   
        circuit = circuit + circuit_comparator
    return circuit

#Apply the reverse of the sorting networkl sn for antisymmetrizing the input state
def apply_reverse_sorting_network(circuit,n,m,sn,L,phase,debug):
    circuit_sn = initialize_circuit(n,m,L)
    circuit_sn = apply_sorting_network(circuit_sn,n,m,sn,L,phase,debug)
    #reverse all gates in the circuit
    circuit_reverse_sn = circuit_sn.inverse()
    circuit = circuit + circuit_reverse_sn

    return circuit

#reset first register to [|0>,|0>,|0>,...] (all zeros)
def reset_electrons(circuit,n,m):
    circuit.barrier()

    for g in range(m):      
        g_indices = np.arange(g*n,(g+1)*n) #classical register positions for electron g
        for g_i in g_indices:
            circuit.reset(g_i)

    return circuit

#reset all registers except for the main electron register
def reset_ancillas(circuit,n,m,L):
    circuit.barrier()
    start = n*m
    end = get_first_coll_ctrl(n,m,L) + m

    for q in range(start,end):
        circuit.reset(q)

    return circuit

#Perform comparisons between all adjacent electron registers, with ctrl ancilla in the coll_register
def collision_compare(circuit,n,m,L,debug):
    #all sets in sets_a can be applied simultaneously (same for sets_b); both for loops are otherwise identical and could be combined
    sets_a,sets_b = get_coll_sets(m)

    c = 0
    for s in sets_a:
        circuit_coll_test = initialize_circuit(n,m,L)
        i = s[0]
        j = s[1]
        circuit_coll_test,cbits = compare_n(circuit_coll_test,n,m,i,j,0,L,debug)
        x_1 = cbits[0]
        y_1 = cbits[1]
        coll_anc = get_first_coll_ctrl(n,m,L) + c
        cbits = [x_1,y_1,coll_anc]

        circuit_coll_test_reverse = circuit_coll_test.inverse()
        
        circuit = circuit + circuit_coll_test
        circuit = bit_compare(circuit,cbits,'01',debug)
        circuit = circuit + circuit_coll_test_reverse
        c+=1 

    for s in sets_b:
        circuit_coll_test = initialize_circuit(n,m,L)
        i = s[0]
        j = s[1]
        circuit_coll_test,cbits = compare_n(circuit_coll_test,n,m,i,j,0,L,debug)
        x_1 = cbits[0]
        y_1 = cbits[1]
        coll_anc = get_first_coll_ctrl(n,m,L) + c
        cbits = [x_1,y_1,coll_anc]

        circuit_coll_test_reverse = circuit_coll_test.inverse()
        
        circuit = circuit + circuit_coll_test
        circuit = bit_compare(circuit,cbits,'01',debug)
        circuit = circuit + circuit_coll_test_reverse
        c+=1
    
    return circuit

#apply X gate on last qubit, conditioned on all other coll_ancillas being 1 (which means that all elctron registers are different)
def collision_test(circuit,n,m,L,debug):
    coll_ctrl_0 = get_first_coll_ctrl(n,m,L)
    control = ''
    qubits = []

    for i in range(m-1):
        control = control + '1'
        qubits.append(coll_ctrl_0+i)

    qubits.append(coll_ctrl_0+m-1)
    circuit.append(MCXGate(m-1,ctrl_state=control),qubits)

    return circuit

#not necessary
#returns True if output contains only unique elements; returns False otherwise (if two or more elements are the same)
def collision_check_old(output):
    if len(output) == len(set(output)):
        return True
    else:
        return False

#Perform measurement on last qubit in coll_register
def measure_collisions(circuit,n,m,L):
    #add classical register to store measurement result 
    c_q = QuantumRegister(0)                            
    c_reg = ClassicalRegister(1,'collision_check')
    c = QuantumCircuit(c_q,c_reg)                       
    circuit = circuit.combine(c)
    #perform measurements on each electron register and store in separate memorey
    circuit.measure(get_first_coll_ctrl(n,m,L) + m - 1, 0)

    return circuit

#Add classical registers and apply measurements on the main electron register 
def measure_electrons(circuit,n,m):
    circuit.barrier()
    for g in range(m):
        #Add classicla register to store measurement outcomes
        c_q = QuantumRegister(0)                            
        c_reg = ClassicalRegister(n,'mem_{}'.format(asc[g]))
        c = QuantumCircuit(c_q,c_reg)                       
        circuit = circuit.combine(c)
        #perform measurements on each electron register and store in separate memorey
        circuit.measure(np.arange(g*n,(g+1)*n),np.arange(g*n + 1,(g+1)*n + 1))
    return circuit

#Build the circuit with all gates and measurements
@timeis
def build_circuit(n,m,input,sn,L,debug=True):
    #Initialize the circuit with the right number of qubits and ancillas
    circuit = initialize_circuit(n,m,L)
    
    #Apply Hadamard gates to each qubit in the first register   
    circuit = Hadamard(circuit,n,m)

    #Apply the sorting network sn 
    phase = False
    circuit = apply_sorting_network(circuit,n,m,sn,L,phase,debug)
    
    #apply comparisons between all adjacent electron registers and store outcome in coll_register
    circuit = collision_compare(circuit,n,m,L,debug)

    #check if outcome of all comparisons is "not_equal"; flip last qubit in coll_register if this is the case
    circuit = collision_test(circuit,n,m,L,debug)

    #measure last qubit in coll_register, which stores (no collisions = 1) or (collisions = 0); result is kept until the end of the simulation and result accepted if (no collisions == True)
    circuit = measure_collisions(circuit,n,m,L)
    
    #Measurements: classical register 0 stores the random sorted array that can still include collisions
    #circuit = measure_electrons(circuit,n,m)

    #Reset main electron register
    circuit = reset_electrons(circuit,n,m)

    #Initialize main electron register in given input product state
    circuit = binary_init(circuit,n,m,input)
    
    #Apply the reverse of 'apply_sorting_network' and add a conditioned phase shift after each swap (this antisymmetrizes the input state)
    phase = True
    circuit = apply_reverse_sorting_network(circuit,n,m,sn,L,phase,debug)

    #Reset all ancilla qubits and only keep the main electron register (disable for testing final state for antisymmetry)
    #circuit = reset_ancillas(circuit,n,m,L)

    #Measure electron register (for testing)
    #circuit = measure_electrons(circuit,n,m)

    return circuit

#Simulate circuit using specified backend and return simulation result
@timeis
def simulate(circuit,backend,shots):
    simulator = Aer.get_backend(backend)
    #transpile the circuit into the supported set of gates 
    circuit = transpile(circuit,backend=simulator)
    result = simulator.run(circuit,shots=shots).result()

    return result

#turns simulation result 'counts' into list of decimal numbers corresponding to the electron registers; only use if shots=1 or all outcomes are the same
def convert_output_to_decimal(counts,n,m):
    output_list = list(counts.keys())[0][::-1]
    coll_test = output_list[0]
    output_list = output_list[2:]
    output = []
    offset = 0
    for g in range(m):
        start = g*n + offset
        end = (g+1)*n + offset
        g_out = int(output_list[start:end],2)
        output.append(g_out)
        offset += 1
    output_0 = output[0:m]
    return coll_test,output_0

#draw the circuit using size,name as input if plot==True
@timeis
def draw_circuit(circuit,plot_scale,fname):
    circuit.draw(output='mpl',fold=-1,scale=plot_scale,plot_barriers=True)
    plt.savefig(fname,dpi=700)
    return 0
def plot_circuit(circuit,plot_scale,fname,plot=True):
    if plot:
        draw_circuit(circuit,plot_scale,fname)
        plt.show()
        return 0
    print("Plot disabled")
    return 0

#plot sorting network by itself, using cnot as directed comparator (only for visualizationo)
def plot_sorting_network(sn,m):

    circuit_sn = QuantumCircuit(m)

    for s in sn:
        if s[2] == 0:
            i,j = s[0],s[1]
        else:
            i,j = s[1],s[0]

        circuit_sn.cz(i,j)
    
    circuit_sn.draw(output='mpl')
    plt.show()

    return 0

#Generate a bitonic sorting network for m electrons; dir=0 (descending), dir=1 (ascending)
def sorting_network_bitonic(m,dir):
    
    sn = []
    def compAndSwap(i,j,dir):
        sn.append([i,j,dir])
        
    def bitonic_sort(low, cnt, dir):
        if cnt>1:
            k = cnt//2
            dir_n = (dir + 1) % 2
            bitonic_sort(low, k, dir_n)#n_dir
            bitonic_sort(low + k, cnt-k, dir)#dir
            bitonic_merge(low, cnt, dir)
            
            
    def bitonic_merge(low, cnt, dir):
        if cnt>1:
            k = greatestPowerOfTwoLessThan(cnt)
            i = low
            while i < low+cnt-k:
                compAndSwap(i, i+k, dir)
                i+=1
            bitonic_merge(low,k,dir)
            bitonic_merge(low+k,cnt-k,dir)
    
    def greatestPowerOfTwoLessThan(cnt):
        i=1
        while (2**i)<cnt:
            i+=1
        return 2**(i-1)

    bitonic_sort(0,m,dir)
    L = len(sn)
    return sn,L

#Test if sorting network correctly sorts all possible inputs
def test_sn(sn,n,m):
    all_inputs = list(product(range(2**n),repeat=m))
    fail = 0
    count = 0
    for input in all_inputs:
        input = np.array(input)
        temp = np.copy(input)
        for s in sn:
            if s[2]==0:
                i = s[0]
                j = s[1]
            if s[2]==1:
                i = s[1]
                j = s[0]
            if input[i]<input[j]:
                input[i],input[j] = input[j],input[i]
        
        should_be = np.sort(temp)[::-1]
      
        if (input == should_be).all():
            fail += 0
        else:
            fail += 1
        print(f"Testing sorting network {count}/{len(all_inputs)}",end="\r")
        count+=1

    print("                                          ", end = "\r")
    if fail == 0:
        print("Sorting network correct\n")
        return 1
    else:
        print("Error in sorting network\n")
        return 0

#Returns all steps of sorting network with corresponding ancilla registers (for testing)
def test_sn_anc(sn,n,m):
    for s in sn:
        i = s[0]
        j = s[1]
        anc = get_anc(n,m,i,j)
        anc_reg = int((anc-n*m)/(n-1))
        print(f"[{i},{j}] anc_reg={anc_reg}")

    return 0

#Output density matrix of electron register (target) and compute purity, doesnt actually test antisymmetry yet!
def test_antisymmetry(result,n,m,L):
    sv = result.get_statevector()
    trace_out = list(np.arange(n*m,get_first_coll_ctrl(n,m,L)+m))
    #print(f"Tracing out qubits: {trace_out}")
    rho_e = partial_trace(sv,trace_out)
    if rho_e.is_valid():
        print("Target state is valid density matrix\n")
    else:
        print("Target state is not valid density matrix")
    #print(rho_e)
    p = purity(rho_e)
    print(f"Purity of target state = {p}\n")
    return p

 

###################MAINPART############################################################################################################

#Parameters
#n: number of qubits per electron; N = 2^n orbitals
n=3    
#m: number of electrons
m=4    
#input: list of orbitals the electrons are initialized in; needs to be in descending order, without repetitions
input = [5,4,3,2]
#dir: ordering descending (dir=0) or ascending (dir=1)
dir = 0
#plot and save the circuit
plot = True
#include barriers between comparators in the circuit for visualization
debug = False
#measure time of functions: {build_circuit, simulate, draw_circuit}
measure_time = True
#size of the plot
plot_scale = 0.2
#simulation method 
backend = 'statevector_simulator'#'aer_simulator'
#number of circuit repetitions in 'simulate' 
shots = 1

#check valid inputs
check_inputs(n,m)

#Generate sorting network
sn,L = sorting_network_bitonic(m,dir)

#Test sorting network
test_sn(sn,n,m)

#Plot sorting network
plot_sorting_network(sn,m)


#Build circuit
circuit = build_circuit(n,m,input,sn,L,debug)


#Simulate
result = simulate(circuit,backend,shots)
counts = result.get_counts(circuit)
print(f"Counts: {counts}\n")

#Test if final state is antisymmetric
test_antisymmetry(result,n,m,L)
 

output_list = list(counts.keys())[0][::-1]
coll_test = output_list[0]

if coll_test == '1':
    print("No collisions detected - continue\n")
else:
    print("Collisions detected - repeat\n")

#plot circuit
plot_circuit(circuit,plot_scale,f"Plots/Circuit_m{m}_n{n}_debug{debug}",plot) 


