'''
This program stores the API token of IBM Quantum (can be found in the 
account settings) for later use in a qiskitrc-file, loads your IBMQ account
and it lists all the versions of your qiskit installation.
'''

import qiskit 
from qiskit import IBMQ

IBMQ.save_account('***********')
IBMQ.load_account
print(qiskit.__qiskit_version__)