from qiskit_ibm_runtime.fake_provider import FakeOsaka, FakeSherbrooke, FakeBrisbane
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit.circuit.library import QFT
def backend_with_lowest_complexity():
    """ Transpile the 4-qubit QFT circuit using preset passmanager with optimization level 3 and seed transpiler = 1234 in FakeOsaka, FakeSherbrooke and FakeBrisbane. Compute the cost of the instructions by penalizing the two qubit gate with a cost of 5, rz gates with a cost 1 and other gates with a cost 2 and return the value of the highest cost among these backends.
    """
    qft = QFT(4)
    pass_manager = generate_preset_pass_manager(optimization_level=3, seed_transpiler=1234)
    transpiled_circuits = pass_manager.run(qft)
    cost_osaka = 0
    cost_sherbrooke = 0
    cost_brisbane = 0
    for circuit in transpiled_circuits:
        for instruction in circuit.data:
            if instruction.name == 'rz':
                cost_osaka += 1
                cost_sherbrooke += 1
                cost_brisbane += 1
            elif instruction.name == 'cx':
                cost_osaka += 5
                cost_sherbrooke += 5
                cost_brisbane += 5
            else:
                cost_osaka += 2
                cost_sherbrooke += 2
                cost_brisbane += 2
    return max(cost_osaka, cost_sherbrooke, cost_brisbane)

backend_with_lowest_complexity()