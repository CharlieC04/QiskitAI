import os
import qiskit.ignis.verification.randomized_benchmarking as rb

#Number of seeds (random sequences)
nseeds = 2
#Number of Cliffords in the sequence
nCliffs = [1, 10, 20, 50]
#2Q RB on Q0,Q2 and 1Q RB on Q1 etc., also defines the width of the circuit
# rb_pattern = [[0,2],[1],[3,4]]
rb_pattern = [[0,1],[2],[3,4]]
rb_pattern_string = '_'.join(['-'.join([str(r) for r in rb]) for rb in rb_pattern])
#Do three times as many 1Q Cliffords
#length_multiplier = [1,3,1,2]

rb_opts = {}
rb_opts['length_vector'] = nCliffs
rb_opts['nseeds'] = nseeds
rb_opts['rb_pattern'] = rb_pattern
#rb_opts['length_multiplier'] = length_multiplier
rb_circs, xdata = rb.randomized_benchmarking_seq(**rb_opts)

# store generated circuits in desired directory
count = 0
indexListElem = 0
for listElem in rb_circs:
    indexListElem += 1
    listElem_string = str(indexListElem)
    count += len(listElem)
    for indexElem, elem in enumerate(listElem):
        print("----------------------------------------")
        print(f"depth: {elem.depth()}")
        print(f"number of multi-qubit gates: {elem.num_nonlocal_gates()}")
        nCliffs_string = str(nCliffs[indexElem])
        file_name = 'pattern' + rb_pattern_string + 'nCliffs' + nCliffs_string + 'seed' + listElem_string + '.qasm'
        save_dir = '/Users/mariesalm/Downloads/temp/' # enter your directory here
        with open(os.path.join(save_dir, file_name), 'w') as file:
            file.write(elem.qasm())

print("****************************************")
print (f"Generated {count} circuits")
