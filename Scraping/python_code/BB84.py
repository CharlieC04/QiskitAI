import numpy as np
from qiskit import *
from qiskit.visualization import plot_histogram
from matplotlib.pyplot import plot, draw, show

def SendState(qc1, qc2, qc1_name):
    '''
    This function takes the output of circuit qc1 
    (made up of only H and X gates)
    and initialises another circuit qc2 with the same state 
    '''
    qs = qc1.qasm().split(sep=';')[4:-1]
    
    # process the code to get the instructions
    for i, instruction in enumerate(qs):
        qs[i] = instruction.lstrip()

    # parse the instructions and apply to new circuit
    for instruction in qs:
        instruction_gate  = instruction[0]
        instruction_qubit_list = []
        i = 0
        while instruction[i] != '[':
            i += 1
        i += 1
        while instruction[i] != ']':
            instruction_qubit_list.append(instruction[i])
            i += 1

        instruction_qubit = 0
        for i, dec in enumerate(reversed(instruction_qubit_list)):
                instruction_qubit += int(dec)*10**i
        
        if(instruction_gate == 'x'):
            old_qr = int(instruction_qubit)
            qc2.x(qr[old_qr])
        elif instruction_gate == 'h':
            old_qr = int(instruction_qubit)
            qc2.h(qr[old_qr])
        elif instruction_gate == 'm':
            # exclude measuring
            pass
        else:
            raise Exception('Unable to parse instruction')


# declare classical and quantum register
n = 16 # for local backend 'n' can go up to 23, 
      #after which a memery error is raised
qr = QuantumRegister(n, name='q')
cr = ClassicalRegister(n, name='c')

# create Alice's circuit
alice = QuantumCircuit(qr, cr, name='Alice')

# generate a random number expressible by the available qubits
alice_key = np.random.randint(0,high=2**n)

# cast key to binary representation
alice_key = np.binary_repr(alice_key,n)

# encode key as alice qubits
for i, digit in enumerate(alice_key):
    if(digit == '1'):
        alice.x(qr[i])
# switch randomly about half qubits to Hadamard basis
alice_table = []
for qubit in qr:
    if(np.random.rand()>0.5):
        alice.h(qubit)
        alice_table.append('H') # indicate the Hadamard-basis 
    else:
        alice_table.append('Z') # indicate the Z-basis

# create Bob's circuit
bob = QuantumCircuit(qr, cr, name='Bob')
SendState(alice,bob, 'Alice')
# Bob does not know which basis to use
bob_table = []
for qubit in qr:
    if(np.random.rand()>0.5):
        bob.h(qubit)
        bob_table.append('H') # indicate the Hadamard-basis 
    else:
        bob_table.append('Z') # indicate the Z-basis

# measure all qubits
for i, qubit in enumerate(qr):
    bob.measure(qubit, cr[i])
backend = BasicAer.get_backend('qasm_simulator')

# Bob has only one chance of measuring correctly
result = execute(bob, backend=backend, shots=1).result()
#plot_histogram(result.get_counts(bob))
#draw()
#show(block=True)

# result of the measurement is Bob's key candidate
bob_key = list(result.get_counts(bob))[0]

# key is reversed so that first qubit is the first element of the list
bob_key = bob_key[::-1]

# compare basis and discard qubits not measured in the same basis
keep = []
discard = []

print('\n', "Compare Bob's and Alice's basis (without eavesdropping): ")
for qubit, basis in enumerate(zip(alice_table,bob_table)):
    if(basis[0] == basis[1]):
        print("Same choice for qubit: {}, basis: {}".format(qubit, basis[0]))
        keep.append(qubit)
    else:
        print("Different choice for qubit: {}, Alice has {}, Bob has {}".format(qubit, basis[0], basis[1]))
        discard.append(qubit)

# measure the percentage of qubits to be discarded
acc = 0
for bit in zip(alice_key, bob_key):
    if(bit[0]==bit[1]):
        acc += 1
print('\n Percentage of qubits to be discarded according to table comparison: ',
        len(keep)/n)
print('Measurement convergence by additional chance: ', acc/n)

new_alice_key = [alice_key[qubit] for qubit in keep]
new_bob_key = [bob_key[qubit] for qubit in keep]

acc = 0
for bit in zip(new_alice_key, new_bob_key):
    if(bit[0] == bit[1]):
        acc += 1
print('Percentage of similarity between the keys: ', acc/len(new_alice_key))

if(acc//len(new_alice_key) == 1):
    print('Key exchange has been succesfull')
    print("New Alice's key: ", new_alice_key)
    print("New Bob's key: ", new_bob_key)
else:
    print('Key exchange has been tampered! ---> Check for eavesdropper or try again')
    print("New Alice's key is invalid: ", new_alice_key)
    print("New Bob's key is invalid: ", new_bob_key)

# let's intrude a eavesdropper Eve (which is initialised to Alice's state)
eve = QuantumCircuit(qr, cr, name='Eve')
SendState(alice, eve, 'Alice')

eve_table = []
for qubit in qr:
    if(np.random.rand()>0.5):
        eve.h(qubit)
        eve_table.append('H')
    else:
        eve_table.append('Z')
for i, qubit in enumerate(qr):
    eve.measure(qubit,cr[i])

# Execute (build and run) the quantum circuit
backend = BasicAer.get_backend('qasm_simulator')
result = execute(eve, backend=backend, shots=1).result()

# Result of the measurement is Eve's key
eve_key = list(result.get_counts(eve))[0]
eve_key = eve_key[::-1]

# Update states to new eigenstates (of wrongly chosen basis)
print('\n', "Compare Eve's and Alice's basis: ")
for i, basis in enumerate(zip(alice_table,eve_table)):
    if(basis[0] == basis[1]):
        print("Same choice for qubit: {}, basis: {}".format(qubit, basis[0]))
        keep.append(i)
    else:
        print("Different choice for qubit: {}, Alice has {}, Eve has {}".format(qubit, basis[0], basis[1]))
        discard.append(i)
    if eve_key[i] == alice_key[i]:
        eve.h(qr[i])
    else:
        if (basis[0] == 'H' and basis[1] == 'Z'):
            alice.h(qr[i])
            eve.x(qr[i])
        else:
            eve.x(qr[i])
            eve.h(qr[i])

# Eve's state is now sent to Bob
SendState(eve, bob, 'Eve')
bob_table = []
for qubit in qr:
    if(np.random.rand()>0.5):
        bob.h(qubit)
        bob_table.append('H')
    else:
        bob_table.append('Z')
for i, qubit in enumerate(qr):
    bob.measure(qubit, cr[i])
result = execute(bob, backend, shots=1).result()
#plot_histogram(result.get_counts(bob))
#draw()
#show(block=True)

bob_key = list(result.get_counts(bob))[0]
bob_key = bob_key[::-1]

# Now Alice and Bob will share their table data and perform checking operations
keep = []
discard = []

print('\n', "Compare Bob's and Alice's basis (with eavesdropping by Eve): ")
for qubit, basis in enumerate(zip(alice_table, bob_table)):
    if(basis[0] == basis[1]):
        print("Same choice for qubit: {}, basis: {}".format(qubit, basis[0]))
        keep.append(qubit)
    else:
        print("Different choice for qubit: {}, Alice has {}, Bob has {}".format(qubit, basis[0], basis[1]))
        discard.append(qubit)

# measure the percentage of qubits to be discarded
acc = 0
for bit in zip(alice_key, bob_key):
    if(bit[0]==bit[1]):
        acc += 1
print('Percentage of qubits to be discarded according to table comparison: ',
        len(keep)/n)
print('Measurement convergence by additional chance: ', acc/n)

new_alice_key = [alice_key[qubit] for qubit in keep]
new_bob_key = [bob_key[qubit] for qubit in keep]

acc = 0
for bit in zip(new_alice_key, new_bob_key):
    if(bit[0] == bit[1]):
        acc += 1
print('\n Percentage of similarity between the keys: ', acc/len(new_alice_key))

if(acc//len(new_alice_key) == 1):
    print('Key exchange has been succesfull')
    print("New Alice's key: ", new_alice_key)
    print("New Bob's key: ", new_bob_key)
else:
    print('Key exchange has been tampered! --->',
          'Check for eavesdropper or try again')
    print("New Alice's key is invalid: ", new_alice_key)
    print("New Bob's key is invalid: ", new_bob_key)

