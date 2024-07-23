from datetime import datetime
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit, BasicAer, execute, IBMQ, transpile
from qiskit.providers import BaseJob
from qiskit.providers.ibmq import least_busy, IBMQJobManager
from qiskit.providers.ibmq.managed import ManagedJobSet
from qiskit.visualization import plot_histogram

import constants
from QCLG_lvl3.classical.bernstein_vazirani_classical import BersteinVaziraniClassical
from QCLG_lvl3.classical.classical_xor import ClassicalXor
from QCLG_lvl3.classical.random_binary import RandomBinary
from QCLG_lvl3.quantum_algorithms.bernstein_vazirani import BernsteinVazirani
from QCLG_lvl3.quantum_algorithms.deutsch_josza import DeutschJosza
from credentials import account_details


class Tools:
    @classmethod
    def calculate_elapsed_time(cls, first_step: datetime, last_step: datetime):
        difference = last_step - first_step
        return difference.total_seconds()

    @classmethod
    def run_on_simulator(cls, circuit: QuantumCircuit):
        # use local simulator
        backend = BasicAer.get_backend('qasm_simulator')
        shots = 1024
        results = execute(circuit, backend=backend, shots=shots).result()
        answer = results.get_counts()
        max_value = 0
        max_key = ""
        for key, value in answer.items():
            if value > max_value:
                max_value = value
                max_key = key
        return max_key[::-1]

    @classmethod
    def run_on_real_device(cls, circuit: QuantumCircuit, least_busy_backend):

        from qiskit.tools.monitor import job_monitor
        shots = int(input("Number of shots (distinct executions to run this experiment: )"))
        job = execute(circuit, backend=least_busy_backend, shots=shots, optimization_level=3)
        job_monitor(job, interval=2)
        return job

    @classmethod
    def find_least_busy_backend_from_open(cls, n):
        if account_details.account_token_open is None:
            account_token = input("Insert your account token: ")
        else:
            account_token = account_details.account_token_open
        if IBMQ.active_account() is None:
            IBMQ.enable_account(account_token)
        provider = IBMQ.get_provider(hub='ibm-q')
        return least_busy(provider.backends(filters=lambda x: x.configuration().n_qubits >= (n + 1) and
                                                              not x.configuration().simulator and x.status().operational == True))

    @classmethod
    def find_least_busy_backend_from_research(cls, n):
        if account_details.account_token_research is None \
                or account_details.hub is None \
                or account_details.group is None \
                or account_details.project is None:
            account_token = input("Insert your account token: ")
            hub = input("Insert your hub: ")
            group = input("Insert your group: ")
            project = input("Insert your project: ")
        else:
            account_token = account_details.account_token_research
            hub = account_details.hub
            group = account_details.group
            project = account_details.project

        IBMQ.enable_account(account_token)
        provider = IBMQ.get_provider(hub=hub, group=group, project=project)
        print(provider)
        return least_busy(provider.backends(filters=lambda x: x.configuration().n_qubits >= (n + 1) and
                                                              not x.configuration().simulator and x.status().operational == True))

    @classmethod
    def print_simul(cls, answer_of_simul, algorithm: str):
        print(constants.algorithms[int(algorithm)])
        print("\nMeasurements: ", answer_of_simul)
        return

    @classmethod
    def print_real(cls, job: BaseJob, least_busy_backend, algorithm: str):
        results = job.result()
        answer = results.get_counts()
        print("\nTotal counts are:", answer)
        elapsed = results.time_taken
        print(f"The time it took for the experiment to complete after validation was {elapsed} seconds")
        plot_histogram(data=answer, title=f"{constants.algorithms[int(algorithm)]} on {least_busy_backend}")
        plt.show()
        return

    @classmethod
    def execute_classically(cls, algorithm):
        if algorithm == "0":
            return cls.execute_deutsch_josza_classically()
        elif algorithm == "1":
            return cls.execute_bernstein_vazirani_classically()

    @classmethod
    def execute_in_simulator(cls, algorithm):
        dj_circuit = None
        if algorithm == "0":
            bits = str(input("Enter a bit sequence for the quantum circuit:"))
            dj_circuit = DeutschJosza.deutsch_josza(bits, eval_mode=False)
        elif algorithm == "1":
            decimals = int(input("Give the upper limit of the random number: "))
            random_binary = RandomBinary.generate_random_binary(decimals)
            dj_circuit = BernsteinVazirani.bernstein_vazirani(random_binary, eval_mode=False)
        return cls.run_on_simulator(dj_circuit)

    @classmethod
    def execute_in_real_device(cls, algorithm):

        if algorithm == "0":
            answer = cls.execute_dj_in_real_device()
            return answer
        elif algorithm == "1":
            decimals = int(input("Give the upper limit of the random number: "))
            random_binary = RandomBinary.generate_random_binary(decimals)
            answer = cls.execute_bv_in_real_device(random_binary)
            return answer

    @classmethod
    def execute_dj_in_real_device(cls):
        bits = str(input("Enter a bit sequence for the quantum circuit:"))
        least_busy_backend = Tools.choose_from_provider(len(bits) + 1)
        dj_circuit = DeutschJosza.deutsch_josza(bits, eval_mode=False)
        answer_of_real = Tools.run_on_real_device(dj_circuit, least_busy_backend)
        print(f"least busy is {least_busy_backend}")
        return answer_of_real

    @classmethod
    def execute_bv_in_real_device(cls, random_binary: str):
        dj_circuit = BernsteinVazirani.bernstein_vazirani(random_binary, eval_mode=False)
        least_busy_backend = Tools.choose_from_provider(dj_circuit.qubits)
        answer_of_real = Tools.run_on_real_device(dj_circuit, least_busy_backend)
        print(f"least busy is {least_busy_backend}")
        return answer_of_real

    @classmethod
    def choose_from_provider(cls, size: int):
        least_busy_backend = None
        research = input("Do you want to run this experiment on the research backends? (Y/N)")
        while research != "Y" and research != "N":
            research = input("Do you want to run this experiment on the research backends? (Y/N)")
        if research == "N":
            least_busy_backend = Tools.find_least_busy_backend_from_open(size)
        elif research == "Y":
            least_busy_backend = Tools.find_least_busy_backend_from_research(size)
        return least_busy_backend

    @classmethod
    def execute_deutsch_josza_classically(cls):
        number_of_bits = int(input("Enter number of bits for a the classical solution:"))
        return ClassicalXor.execute_classical_xor(bits=number_of_bits)

    @classmethod
    def execute_bernstein_vazirani_classically(cls):
        decimals = int(input("Give the upper limit of the random number: "))
        random_binary = RandomBinary.generate_random_binary(decimals)
        return BersteinVaziraniClassical.guess_number(random_binary)

    @classmethod
    def print_classical_answer(cls, classical_answer, algorithm):
        time_to_generate_worst_input = classical_answer[0]
        execution_time = classical_answer[1]
        bits = classical_answer[2]
        function_nature = classical_answer[3]
        print(f"Results of classical implementation for the {constants.algorithms[int(algorithm)]} Algorithm:")
        print(f"Function is {function_nature}")
        print(f"Time to generate worse input for {bits} bits took {time_to_generate_worst_input} seconds.")
        print(f"Determining if xor is balanced for {bits} bits took {execution_time} seconds.")
        print(classical_answer)

    @classmethod
    def execute_both(cls, algorithm):
        answer = []
        if algorithm == "0":
            classical = cls.execute_deutsch_josza_classically()
            real = cls.execute_dj_in_real_device()
            answer.append(classical)
            answer.append(real)
        elif algorithm == " 1":
            classical = cls.execute_bernstein_vazirani_classically()
            real = cls.execute_bv_in_real_device(classical)
            answer.append(classical)
            answer.append(real)
        return answer

    # #################################################################################################################
    # Evaluation methods

    @classmethod
    def prepare_dj(cls, bits: int):
        bit_sequence = "0" * bits
        dj_circuit = DeutschJosza.deutsch_josza(bit_sequence, eval_mode=True)
        return dj_circuit

    @classmethod
    def prepare_bv(cls, random_binary: str):
        bj_circuit = BernsteinVazirani.bernstein_vazirani(random_binary, eval_mode=True)
        return bj_circuit

    @classmethod
    def deutsch_josza_classical(cls, bits: int):
        return ClassicalXor.execute_classical_xor(bits=bits)

    @classmethod
    def bernstein_vazirani_classical(cls, bits: int):
        random_binary = RandomBinary.generate_random_binary_v2(bits)
        return BersteinVaziraniClassical.guess_number(random_binary)

    @classmethod
    def run_batch_job(cls, circuits: list, least_busy_backend) -> ManagedJobSet:
        transpiled_circuits = transpile(circuits, backend=least_busy_backend)
        # Use Job Manager to break the circuits into multiple jobs.
        job_manager = IBMQJobManager()
        job_set_eval = job_manager.run(transpiled_circuits, backend=least_busy_backend, name='eval',
                                       max_experiments_per_job=1) # max_experiments_per_job =1 very important to get
        # individual execution times
        return job_set_eval

