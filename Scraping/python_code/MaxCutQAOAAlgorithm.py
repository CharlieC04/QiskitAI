import requests
from qiskit import QuantumCircuit
import json


def get_circuit(**kwargs):
    adj_matrix = kwargs["adj_matrix"]
    betas = kwargs["betas"]
    gammas = kwargs["gammas"]
    data = json.dumps({"adj_matrix": adj_matrix, "betas": betas, "gammas": gammas, })
    headers = {"Content-Type": "application/json"}
    response = requests.post('http://quantum-circuit-generator:5073/algorithms/qaoa/maxcut', data=data, headers=headers)
    response_dict = json.loads(response.text)

    if response_dict['circuit'] is not None:
        circuit = QuantumCircuit.from_qasm_str(response_dict['circuit'])
        return circuit

    else:
        return None


def post_processing(**kwargs):
    adj_matrix = kwargs["adj_matrix"]
    counts = kwargs["counts"]
    data = json.dumps({"adj_matrix": adj_matrix, "counts": counts, "objFun": "Expectation", "visualization": "True"})
    headers = {"Content-Type": "application/json"}
    response = requests.post('http://objective-evaluation-service:5072/objective/max-cut', data=data, headers=headers)
    return json.dumps(response.text)
