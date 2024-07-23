# -*- coding: utf-8 -*-
"""
Created on Sat Dec 24 09:39:52 2022

@author: Daisuke Ito
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import differential_evolution
from qiskit import QuantumCircuit
import itertools
import requests
import json
import sys
sys.path.append("..")
from kosakaq_job import KosakaQExperimentJob

class randomized_benchmarking:
    def __init__(self,  backend, length_vector = [1, 10, 20, 50, 75, 100, 125, 150, 175, 200], repetition =30, shots = 4096, seed = None, interleaved = ""):
        self.backend = backend
        self.length_vector = length_vector
        self.rep = repetition
        self.shots = shots
        self.seed = seed
        self.interleaved = interleaved
        if not (interleaved == ""):
            if interleaved == "X":
                self.interleaved_gate = 1
            elif interleaved == "Y":
                self.interleaved_gate = 2
            elif interleaved == "Z":
                self.interleaved_gate = 3
            else:
                raise    
        self.gate_sequence = []
        self.circuits = []
        self.result_data = None
        self.ops = None
        self.Cliford_trans = \
        np.array([[  0.,   1.,   2.,   3.,   4.,   5.,   6.,   7.,   8.,   9.,  10.,
         11.,  12.,  13.,  14.,  15.,  16.,  17.,  18.,  19.,  20.,  21.,
         22.,  23.],
       [  1.,   0.,   3.,   2.,   6.,   7.,   4.,   5.,  11.,  10.,   9.,
          8.,  13.,  12.,  18.,  19.,  22.,  23.,  14.,  15.,  21.,  20.,
         16.,  17.],
       [  2.,   3.,   0.,   1.,   7.,   6.,   5.,   4.,  10.,  11.,   8.,
          9.,  20.,  21.,  15.,  14.,  23.,  22.,  19.,  18.,  12.,  13.,
         17.,  16.],
       [  3.,   2.,   1.,   0.,   5.,   4.,   7.,   6.,   9.,   8.,  11.,
         10.,  21.,  20.,  19.,  18.,  17.,  16.,  15.,  14.,  13.,  12.,
         23.,  22.],
       [  4.,   7.,   5.,   6.,  11.,   8.,   9.,  10.,   2.,   3.,   1.,
          0.,  22.,  17.,  21.,  12.,  14.,  18.,  13.,  20.,  23.,  16.,
         15.,  19.],
       [  5.,   6.,   4.,   7.,  10.,   9.,   8.,  11.,   1.,   0.,   2.,
          3.,  23.,  16.,  12.,  21.,  19.,  15.,  20.,  13.,  22.,  17.,
         18.,  14.],
       [  6.,   5.,   7.,   4.,   8.,  11.,  10.,   9.,   3.,   2.,   0.,
          1.,  16.,  23.,  20.,  13.,  18.,  14.,  12.,  21.,  17.,  22.,
         19.,  15.],
       [  7.,   4.,   6.,   5.,   9.,  10.,  11.,   8.,   0.,   1.,   3.,
          2.,  17.,  22.,  13.,  20.,  15.,  19.,  21.,  12.,  16.,  23.,
         14.,  18.],
       [  8.,   9.,  11.,  10.,   1.,   3.,   2.,   0.,   7.,   4.,   5.,
          6.,  19.,  14.,  22.,  16.,  20.,  12.,  23.,  17.,  15.,  18.,
         13.,  21.],
       [  9.,   8.,  10.,  11.,   2.,   0.,   1.,   3.,   6.,   5.,   4.,
          7.,  14.,  19.,  23.,  17.,  13.,  21.,  22.,  16.,  18.,  15.,
         20.,  12.],
       [ 10.,  11.,   9.,   8.,   3.,   1.,   0.,   2.,   4.,   7.,   6.,
          5.,  18.,  15.,  17.,  23.,  12.,  20.,  16.,  22.,  14.,  19.,
         21.,  13.],
       [ 11.,  10.,   8.,   9.,   0.,   2.,   3.,   1.,   5.,   6.,   7.,
          4.,  15.,  18.,  16.,  22.,  21.,  13.,  17.,  23.,  19.,  14.,
         12.,  20.],
       [ 12.,  13.,  21.,  20.,  18.,  19.,  14.,  15.,  22.,  17.,  23.,
         16.,   1.,   0.,   4.,   5.,   8.,  10.,   6.,   7.,   2.,   3.,
         11.,   9.],
       [ 13.,  12.,  20.,  21.,  14.,  15.,  18.,  19.,  16.,  23.,  17.,
         22.,   0.,   1.,   6.,   7.,  11.,   9.,   4.,   5.,   3.,   2.,
          8.,  10.],
       [ 14.,  19.,  15.,  18.,  22.,  16.,  23.,  17.,  20.,  21.,  12.,
         13.,   8.,   9.,   2.,   0.,   6.,   4.,   1.,   3.,  10.,  11.,
          7.,   5.],
       [ 15.,  18.,  14.,  19.,  17.,  23.,  16.,  22.,  12.,  13.,  20.,
         21.,  10.,  11.,   0.,   2.,   5.,   7.,   3.,   1.,   8.,   9.,
          4.,   6.],
       [ 16.,  23.,  22.,  17.,  12.,  21.,  20.,  13.,  19.,  14.,  15.,
         18.,   5.,   6.,   8.,  11.,   3.,   0.,  10.,   9.,   7.,   4.,
          1.,   2.],
       [ 17.,  22.,  23.,  16.,  21.,  12.,  13.,  20.,  14.,  19.,  18.,
         15.,   4.,   7.,   9.,  10.,   0.,   3.,  11.,   8.,   6.,   5.,
          2.,   1.],
       [ 18.,  15.,  19.,  14.,  16.,  22.,  17.,  23.,  21.,  20.,  13.,
         12.,  11.,  10.,   3.,   1.,   4.,   6.,   0.,   2.,   9.,   8.,
          5.,   7.],
       [ 19.,  14.,  18.,  15.,  23.,  17.,  22.,  16.,  13.,  12.,  21.,
         20.,   9.,   8.,   1.,   3.,   7.,   5.,   2.,   0.,  11.,  10.,
          6.,   4.],
       [ 20.,  21.,  13.,  12.,  19.,  18.,  15.,  14.,  17.,  22.,  16.,
         23.,   3.,   2.,   7.,   6.,  10.,   8.,   5.,   4.,   0.,   1.,
          9.,  11.],
       [ 21.,  20.,  12.,  13.,  15.,  14.,  19.,  18.,  23.,  16.,  22.,
         17.,   2.,   3.,   5.,   4.,   9.,  11.,   7.,   6.,   1.,   0.,
         10.,   8.],
       [ 22.,  17.,  16.,  23.,  13.,  20.,  21.,  12.,  15.,  18.,  19.,
         14.,   7.,   4.,  11.,   8.,   2.,   1.,   9.,  10.,   5.,   6.,
          0.,   3.],
       [ 23.,  16.,  17.,  22.,  20.,  13.,  12.,  21.,  18.,  15.,  14.,
         19.,   6.,   5.,  10.,   9.,   1.,   2.,   8.,  11.,   4.,   7.,
          3.,   0.]])
    

    def make_sequence(self):
        self.gate_sequence = []
        for i in range(self.rep):
            self.gate_sequence.append([])
            for gate_num in self.length_vector:
                if self.seed is not None:
                    np.random.seed(self.seed)
                    gate_sequence_fwd = np.random.randint(0,23,gate_num).tolist()
                else:  
                    gate_sequence_fwd = np.random.randint(0,23,gate_num).tolist()
                
                if self.interleaved:
                    temp = [[x,self.interleaved_gate] for x in gate_sequence_fwd]
                    gate_sequence_fwd = list(itertools.chain.from_iterable(temp))
                    
                n_gate = 0
                for m in gate_sequence_fwd:
                    n_gate = int(self.Cliford_trans[m,n_gate])
                self.Cliford_last = n_gate
                self.Cliford_last_dag = np.where(self.Cliford_trans[:,self.Cliford_last] == 0)[0][0]
                self.gate_sequence[i].append(gate_sequence_fwd+[self.Cliford_last_dag.item()])
        self._make_circuit()
    
    
    def run(self):
        access_token = self.backend.provider.access_token
        data = {
            "length_vector":self.length_vector,
            "gate_sequence":self.gate_sequence,
            "rep":self.rep,
            "shots":self.shots,
            "seed":self.seed,
            "interleaved":self.interleaved
                }
        data = json.dumps(data)
        kosakaq_json ={
                'experiment': 'experiment',
                'data': data,
                'access_token': access_token,
                'repetitions': 1,
                'backend': self.backend.name,
        }
        header = {
            "Authorization": "token " + access_token,
        }
        res = requests.post("http://192.168.11.85/job/", data=kosakaq_json, headers=header)
        response = res.json()
        res.raise_for_status()
        self.job = KosakaQExperimentJob(self.backend, response['id'], access_token=self.backend.provider.access_token, qobj=data)
    
    
    def result(self):
        access_token = self.backend.provider.access_token
        # get result
        header = {
            "Authorization": "Token " + access_token
        }
        result = requests.get(
            self.backend.url + ('/job/'),
            headers=header,
            params={"jobid": self.job._job_id}
        ).json()
        if result["qobjlist"][0][0]["result"] is None:
            data = []
        else:
            data = [d.split() for d in result["qobjlist"][0][0]["result"].split("\n")]
            data.pop(-1)
        length = len(self.length_vector)
        rep = len(data)//length
        rem = len(data)%length
        if (result['joblist'][0]['jobstatus'] == "ERROR") or (result['joblist'][0]['jobstatus'] == "QUEUED"):
            raise
        if not (rep == self.rep) and (result['joblist'][0]['jobstatus'] == "RUNNING"):
            print("This job is running.")
        result_data = []
        for i in range(rep):
            result_data.append([data[j] for j in range(i*length,(i+1)*length)])
        result_data.append([data[j] for j in range(rep*length,rep*length+rem)])
        self.result_data = result_data
            
        # fitting
        if rep>0:
            
            # data
            time = self.length_vector
            self.sum_data = []
            self.ave_data = []
            print(length)
            print(rep)
            print(result_data)
            for i in range(length):
                sum_rep = 0
                for j in range(rep):
                    sum_rep += int(result_data[j][i][0])
                self.sum_data.append(sum_rep/self.shots)
                self.ave_data.append(sum_rep/(self.shots*rep))
              
            # fitting func
            def exp_curve(parameter):
                a, b, p = parameter
                return a * (p**(time)) + b

            def fit_func(parameter):
                ycal = exp_curve(parameter)
                residual = ycal - ave_data
                return sum(abs(residual))
            
            # optimize
            ave_data = self.ave_data
            bound = [(0,1),(0,10),(0.001,50)]
            opts = differential_evolution(fit_func, bounds = bound)
            self.opt = opts.x
            print(f'a = {self.opt[0]}')
            print(f'b = {self.opt[1]}')
            print(f'p = {self.opt[2]}')
            if self.interleaved == "":
                print(f'F = {(self.opt[2]+1)/2}')
            else:
                print("interleavedの場合、フィデリティの計算には、interleavedではない時のデータが必要")

    
    def plot(self):
        time = np.linspace(0.01, self.length_vector[-1], 1000)
        def exp_curve(parameter):
            a, b, p = parameter
            return a * (p**(time)) + b
        plt.figure(dpi=1000)
        plt.plot(time, exp_curve(self.opt), color = 'blue', label='fitting')
        for i in range(len(self.result_data)):
            for j in range(len(self.result_data[i])):
                if i == 0 and j ==0:
                    pass
                else:
                    plt.plot(self.length_vector[j], int(self.result_data[i][j][0])/self.shots, marker='.', ls='', color = 'gray')
        plt.plot(self.length_vector[0], int(self.result_data[0][0][0])/self.shots, marker='.', ls='', color = 'gray', label='data')
        plt.plot(self.length_vector, self.ave_data, marker='x', color = 'orange', ls='--', label='average')
        plt.legend()
        plt.title('randomized benchmarking')
        plt.ylabel('Ground State Population')
        plt.xlabel('Clifford Length')
        plt.ylim(-0.1,1.1)
        plt.show()
    
    
    def set_job(self, job: KosakaQExperimentJob):
        self.job = job
        self.backend = job.backend()
        data = json.loads(job.qobj["data"])
        self.length_vector = data["length_vector"]
        self.rep = data["rep"]
        self.shots = data["shots"]
        self.seed = data["seed"]
        if not (data["interleaved"] == ""):
            if data["interleaved"] == "X":
                self.interleaved_gate = 1
            elif data["interleaved"] == "Y":
                self.interleaved_gate = 2
            elif data["interleaved"] == "Z":
                self.interleaved_gate = 3
            else:
                raise    
        self.gate_sequence = []
        self.circuits = []
        self.result_data = None
        self.ops = None
    
    
    def _make_circuit(self):
        self.circuits = []
        for rep, i in zip(self.gate_sequence,range(self.rep)):
            self.circuits.append([])
            for gates in rep:
                qc = QuantumCircuit(1,1)
                for gate in gates:
                    if gate == 0:
                        qc.i(0)
                    elif gate == 1:
                        qc.x(0)
                    elif gate == 2:
                        qc.y(0)
                    elif gate == 3:
                        qc.z(0)
                    elif gate == 4:
                        qc.h(0)
                        qc.s(0)                        
                        qc.h(0)
                        qc.s(0)                        
                        qc.z(0)
                    elif gate == 5:
                        qc.h(0)
                        qc.s(0)                        
                        qc.h(0)
                        qc.s(0)  
                    elif gate == 6:
                        qc.h(0)
                        qc.s(0)                        
                        qc.h(0)
                        qc.s(0)                        
                        qc.y(0)                    
                    elif gate == 7:
                        qc.h(0)
                        qc.s(0)                        
                        qc.h(0)
                        qc.s(0)                        
                        qc.x(0)
                    elif gate == 8:
                        qc.h(0)
                        qc.s(0)
                        qc.z(0)
                    elif gate == 9:
                        qc.h(0)
                        qc.s(0)                        
                    elif gate == 10:
                        qc.h(0)
                        qc.s(0)
                        qc.x(0)
                    elif gate == 11:
                        qc.h(0)
                        qc.s(0)                        
                        qc.y(0)
                    elif gate == 12:
                        qc.s(0)                        
                        qc.h(0)
                        qc.s(0)
                        qc.x(0)                        
                    elif gate == 13:
                        qc.s(0)                        
                        qc.h(0)
                        qc.s(0)                        
                    elif gate == 14:
                        qc.h(0)
                        qc.z(0)                        
                    elif gate == 15:
                        qc.h(0)
                        qc.x(0)                        
                    elif gate == 16:
                        qc.sx(0)
                        qc.h(0)
                        qc.z(0)                        
                        qc.sxdg(0)                    
                    elif gate == 17:
                        qc.sx(0)
                        qc.h(0)
                        qc.x(0)                        
                        qc.sxdg(0)                    
                    elif gate == 18:
                        qc.h(0)
                        qc.z(0)   
                        qc.x(0)
                    elif gate == 19:
                        qc.h(0)
                        qc.x(0)   
                        qc.x(0)
                    elif gate == 20:
                        qc.sx(0)     
                        qc.y(0)
                    elif gate == 21:
                        qc.sxdg(0)  
                        qc.y(0)
                    elif gate == 22:
                        qc.s(0)
                        qc.x(0)
                    elif gate == 23:
                        qc.sxdg(0)
                        qc.h(0)
                        qc.z(0)
                        qc.sxdg(0)
                    qc.barrier(0)
                qc.measure(0,0)
                self.circuits[i].append(qc)
        