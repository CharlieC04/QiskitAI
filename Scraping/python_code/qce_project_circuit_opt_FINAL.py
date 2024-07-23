#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 27 11:07:17 2022

@author: angel
"""
# http://lampx.tugraz.at/~hadley/ss1/bzones/fcc.php
# https://aiida-tutorials.readthedocs.io/en/tutorial-2020-intro-week/source/sections/bands.html


from jarvis.db.figshare import get_wann_electron, get_wann_phonon, get_hk_tb
from jarvis.io.qiskit.inputs import HermitianSolver, get_bandstruct, get_dos
from jarvis.core.kpoints import generate_kgrid
import numpy as np
import qiskit
from qiskit import Aer
from jarvis.core.circuits import QuantumCircuitLibrary
import matplotlib.pyplot as plt
# JVASP-816 Al   
# JVASP-1002 Si
# JVASP-35680 PbS
#########################
##### Download WTBH #####
wtbh, Ef, atoms = get_wann_electron(jid="JVASP-1002")
# wtbh, atoms = get_wann_phonon(jid="JVASP-1002",  factor=34.3)
#########################

kpt = [0.5, 0., 0.5] #X-point jarvis
# kpt = [0., 0., 0.] #gamma-point

################################################
##### Transform WTBH into Hermitian matrix #####

# kpt = [0.5, 0., 0.5] #X-point jarvis
kpt = [0., 0., 0.] #gamma-point
##########
hk = get_hk_tb(w=wtbh, k=kpt)
HS = HermitianSolver(hk)
n_qubits = HS.n_qubits()
reps = 1
circ = QuantumCircuitLibrary(n_qubits=n_qubits, reps=reps).circuit6()
backend = Aer.get_backend("statevector_simulator")

###########
### VQE ### 
en, vqe_result, vqe = HS.run_vqe(mode='min_val',var_form=circ,backend=backend)
vals, vecs = HS.run_numpy()
params = vqe.optimal_params
circuit = vqe.construct_circuit(params)
print('Classical, VQE (eV)', (vals[0] - Ef),(en - Ef))
print('Classical, VQE (eV)', (vals[0]),(en))
print(Ef)
###########


##### PbS X Plot Example #######
y = [-5.527449487783215, -8.057364907488996, -8.262343159928434, -8.247681114397821, -8.30798759954503, -8.310212504542353  ]
x = [1, 2, 3, 4, 5, 6]
plt.plot(x,y, color='black', marker = 'o')
plt.axhline(y=-8.310902072462328, color='b', linestyle='-.', linewidth=1)
plt.xlabel('Repetitions')
plt.ylabel('Energy (eV)')
plt.title('PbS X-point (Circuit 6)')
plt.xlim(0.5, 6.5)
plt.ylim(-10, -5)
plt.savefig('PbSX6.png', dpi=150, format=None, metadata=None,
        bbox_inches='tight')



