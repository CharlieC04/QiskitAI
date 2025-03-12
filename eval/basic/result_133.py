import datetime
from qiskit_ibm_runtime import QiskitRuntimeService
def find_recent_jobs():
    """ Find and return jobs submitted in the last three months using QiskitRuntimeService.
    """
    service = QiskitRuntimeService()
    now = datetime.datetime.now()
    three_months_ago = now - datetime.timedelta(days=90)
    jobs = service.jobs(start_datetime=three_months_ago)
    return jobs

jobs = find_recent_jobs()
print(f"Found {len(jobs)} jobs")

for job in jobs:
    print(f"Job ID: {job.job_id}")
    print(f"Job Status: {job.status}")
    print(f"Job Submission Time: {job.created_at}")
    print(f"Job Completion Time: {job.completed_at}")
    print(f"Job Result: {job.result()}")
    print()

# Find and return jobs submitted in the last three months using QiskitRuntimeService.
service = QiskitRuntimeService()
now = datetime.datetime.now()
three_months_ago = now - datetime.timedelta(days=90)
jobs = service.jobs(start_datetime=three_months_ago)
print(f"Found {len(jobs)} jobs")

for job in jobs: