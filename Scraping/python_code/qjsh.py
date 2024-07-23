import qiskit
from qiskit.providers import JobStatus

from QCTest import get_test_qc, get_qc_random_generator
from QuantumPlatform import QuantumPlatform


def get_quantum_circuit():
    return get_test_qc()


def main():
    wait_for_results = True
    try:
        platform_backend = QuantumPlatform(qiskit.Aer, 'aer_simulator')
    except Exception as e:
        print(f'Error during quantum platform initialization: {e}')
        exit(1)

    qc = get_qc_random_generator(1024)
    job = platform_backend.schedule_job(qc, shots=100, dry_run=False,
                                        qc_filename='qc.qasm', qc_image_filename='qc.png',
                                        transpiled_filename = 'transpiled.qasm', transpiled_image_filename='transpiled.png')
    if job is None:
        print('Job is not scheduled!')
        exit(1)
    print(f'Job id={job.job_id}')
    print(f'Job={job}')

    if wait_for_results is False:
        exit(0)

    job.wait_for_final_state()
    print(f'Job status={job.status()}')
    if job.status() == JobStatus.DONE:
        print(f'Job result={job.result()}')
        print(f'Counts={job.result().get_counts(qc)}')


main()