#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 19 19:13:26 2023

@author: abdullahalshihry
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 18 19:15:12 2023

@author: abdullahalshihry
"""

import qiskit as qs
import qiskit.visualization as qv
import random
import qiskit.circuit as qf


def Deutsch_Jozsa(circuit):
    qr = qs.QuantumRegister(5,'q')
    cr = qs.ClassicalRegister(4,'c')
    qc = qs.QuantumCircuit(qr,cr)
    qc.x(qr[4])
    qc.barrier(range(5))
    qc.h(qr[0])
    qc.h(qr[1])
    qc.h(qr[2])
    qc.h(qr[3])
    qc.h(qr[4])
    qc.barrier(range(5))
    qc = qc.compose(circuit)
    qc.barrier(range(5))
    qc.h(qr[0])
    qc.h(qr[1])
    qc.h(qr[2])
    qc.h(qr[3])
    qc.barrier(range(5))
    qc.measure(0,0)
    qc.measure(1,1)
    qc.measure(2,2)
    qc.measure(3,3)
    job1 = qs.execute(qc, qs.Aer.get_backend('aer_simulator'), shots = 1024)
    output1 = job1.result().get_counts()
    print(output1)
    qc.draw('mpl')
    

def Oracle():
    qr = qs.QuantumRegister(5,'q')
    cr = qs.ClassicalRegister(4,'c')
    qc = qs.QuantumCircuit(qr,cr)
    qq = qs.QuantumCircuit(5,name='Uf')
    
    v = random.randint(1, 2)
    
    if v == 1:

        qc.cx(0,4)
        qc.cx(1,4)
        qc.cx(2,4)
        qc.cx(3,4)

        print('Balanced (1)')
    elif v == 2:
        qq.i(qr[0])
        qq.i(qr[1])
        qq.i(qr[2])
        qq.i(qr[3])
        print('Constant (0)')

    
    qq =qq.to_gate()
    qc.append(qq,[0,1,2,3,4])
    return qc
    

    
Deutsch_Jozsa(Oracle())

