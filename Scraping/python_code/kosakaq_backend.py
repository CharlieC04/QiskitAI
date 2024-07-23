# -*- coding: utf-8 -*-
"""
Created on Thu Nov 17 15:00:00 2022
@author: Yokohama National University, Kosaka Lab
"""
import warnings

import requests

from qiskit import qobj as qobj_mod
from qiskit.circuit.parameter import Parameter
from qiskit.circuit.library import IGate, XGate, YGate, ZGate, HGate, SGate, SdgGate, SXGate, SXdgGate
from qiskit.circuit.measure import Measure
from qiskit.providers import BackendV2 as Backend
from qiskit.providers import Options
from qiskit.transpiler import Target
from qiskit.providers.models import BackendConfiguration
from qiskit.exceptions import QiskitError

import kosakaq_job
import circuit_to_kosakaq

class KosakaQBackend(Backend):

    def __init__(
            self, 
            provider,
            name,
            url,
            version,
            n_qubits,
            max_shots=4096,
            max_experiments=1,
            ):
        super().__init__(provider=provider, name=name)
        self.url = url
        self.version = version
        self.n_qubits = n_qubits
        self.max_shots = max_shots
        self.max_experiments = max_experiments
        self._configuration = BackendConfiguration.from_dict({
            'backend_name': name,
            'backend_version': version,
            'url': self.url,
            'simulator': False,
            'local': False,
            'coupling_map': None,
            'description': 'KosakaQ Diamond device',
            'basis_gates': ['i', 'x', 'y', 'z', 'h', 's', 'sdg', 'sx', 'sxdg'], #後で修正が必要
            'memory': False,
            'n_qubits': n_qubits,
            'conditional': False,
            'max_shots': max_shots,
            'max_experiments': max_experiments,
            'open_pulse': False,
            'gates': [
                {
                    'name': 'TODO',
                    'parameters': [],
                    'qasm_def': 'TODO'
                }
            ]
        })
        self._target = Target(num_qubits=n_qubits)
        # theta = Parameter('θ')
        # phi = Parameter('ϕ')
        # lam = Parameter('λ')

        self._target.add_instruction(IGate())
        self._target.add_instruction(XGate())
        self._target.add_instruction(YGate())
        self._target.add_instruction(ZGate())
        self._target.add_instruction(HGate())
        self._target.add_instruction(SGate())
        self._target.add_instruction(SdgGate())
        self._target.add_instruction(SXGate())
        self._target.add_instruction(SXdgGate())
        self._target.add_instruction(Measure())
        self.options.set_validator("shots", (1,max_shots))

    def configuration(self):
        warnings.warn("The configuration() method is deprecated and will be removed in a "
                      "future release. Instead you should access these attributes directly "
                      "off the object or via the .target attribute. You can refer to qiskit "
                      "backend interface transition guide for the exact changes: "
                      "https://qiskit.org/documentation/apidoc/providers.html#backendv1-backendv2",
                      DeprecationWarning)
        return self._configuration

    def properties(self):
        warnings.warn("The properties() method is deprecated and will be removed in a "
                      "future release. Instead you should access these attributes directly "
                      "off the object or via the .target attribute. You can refer to qiskit "
                      "backend interface transition guide for the exact changes: "
                      "https://qiskit.org/documentation/apidoc/providers.html#backendv1-backendv2",
                      DeprecationWarning)

    @property
    def max_circuits(self):
        return 1

    @property
    def target(self):
        return self._target

    @classmethod
    def _default_options(cls):
        return Options(shots=4096)

    def run(self, circuit, **kwargs):
        if isinstance(circuit, qobj_mod.PulseQobj):
            raise QiskitError("Pulse jobs are not accepted")
        for kwarg in kwargs:
            if kwarg != 'shots':
                warnings.warn(
                    "Option %s is not used by this backend" % kwarg,
                    UserWarning, stacklevel=2)
        out_shots = kwargs.get('shots', self.options.shots)
        if out_shots > self.configuration().max_shots:
            raise ValueError('Number of shots is larger than maximum '
                             'number of shots')
        kosakaq_json = circuit_to_kosakaq.circuit_to_KosakaQ(circuit, self._provider.access_token, shots=out_shots, backend=self.name)[0]
        header = {
            "Authorization": "token " + self._provider.access_token,
            "SDK": "qiskit"
        }
        res = requests.post(self.url+r"/job/", data=kosakaq_json, headers=header)
        res.raise_for_status()
        response = res.json()
        if 'id' not in response:
            raise Exception
        job = kosakaq_job.KosakaQJob(self, response['id'], access_token=self.provider.access_token, qobj=circuit)

        return job
