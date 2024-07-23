# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.


import numpy as np
import textwrap
from typing import Union

from functools import partial

from qiskit import QuantumCircuit
from qiskit.opflow import OperatorBase, ListOp, PrimitiveOp, PauliOp
from qiskit.opflow import I, Z
from qiskit.circuit.library import TwoLocal
from qiskit.algorithms.optimizers import Optimizer
from qiskit.utils import QuantumInstance
from qiskit.providers import BaseBackend

from volta.observables import sample_hamiltonian


class SSVQE(object):
    """Subspace-search variational quantum eigensolver for excited states
    algorithm class.

    Based on https://arxiv.org/abs/1810.09434

    """

    def __init__(
        self,
        hamiltonian: Union[OperatorBase, ListOp, PrimitiveOp, PauliOp],
        ansatz: QuantumCircuit,
        backend: Union[BaseBackend, QuantumInstance],
        optimizer: Optimizer,
        n_excited: int,
        debug: bool = False,
    ) -> None:
        """Initialize the class.

        Args:
            hamiltonian (Union[OperatorBase, ListOp, PrimitiveOp, PauliOp]): Hamiltonian
            constructed using qiskit's aqua operators.
            ansatz (QuantumCircuit): Anstaz that you want to run VQD.
            optimizer (qiskit.aqua.components.optimizers.Optimizer): Classical Optimizers
            from aqua components.
            backend (Union[BaseBackend, QuantumInstance]): Backend for running the algorithm.
        """

        # Input parameters
        self.hamiltonian = hamiltonian
        self.n_qubits = hamiltonian.num_qubits
        self.optimizer = optimizer
        self.backend = backend

        # Helper Parameters
        self.ansatz = ansatz
        self.n_parameters = self._get_num_parameters
        self._debug = debug

        self._ansatz_1_params = None
        self._first_optimization = False
        self._n_excited = n_excited
        # Running inate functions
        self._inate_optimizer_run()

    def _create_blank_circuit(self) -> list:
        return [QuantumCircuit(self.n_qubits) for _ in range(self._n_excited)]

    def _copy_unitary(self, list_states: list) -> list:

        out_states = []
        for state in list_states:
            out_states.append(state.copy())
        return out_states

    def _apply_initialization(self, list_states: list) -> None:

        for ind, state in enumerate(list_states):
            b = bin(ind)[2:]
            if len(b) != self.n_qubits:
                b = "0" * (self.n_qubits - len(b)) + b
            spl = textwrap.wrap(b, 1)
            for qubit, val in enumerate(spl):
                if val == "1":
                    state.x(qubit)

    @property
    def _get_num_parameters(self) -> int:
        """Get the number of parameters in a given ansatz.

        Returns:
            int: Number of parameters of the given ansatz.
        """
        return len(self.ansatz.parameters)

    def _apply_varform_params(self, ansatz, params: list):
        """Get an hardware-efficient ansatz for n_qubits
        given parameters.
        """

        # Define variational Form
        var_form = ansatz

        # Get Parameters from the variational form
        var_form_params = sorted(var_form.parameters, key=lambda p: p.name)

        # Check if the number of parameters is compatible
        assert len(var_form_params) == len(
            params
        ), "The number of parameters don't match"

        # Create a dictionary with the parameters and values
        param_dict = dict(zip(var_form_params, params))

        # Assing those values for the ansatz
        wave_function = var_form.assign_parameters(param_dict)

        return wave_function

    def _apply_ansatz(self, list_states: list, name: str = None) -> None:
        for states in list_states:
            if name:
                self.ansatz.name = name
            states.append(self.ansatz, range(self.n_qubits))

    def _construct_states(self):
        circuit = self._create_blank_circuit()

        self._apply_initialization(circuit)

        self._apply_ansatz(circuit)

        return circuit

    def _cost_function_1(self, params: list) -> float:
        """Evaluate the first cost function of SSVQE.

        Args:
            params (list): Parameter values for the ansatz.

        Returns:
            float: Cost function value.
        """

        # Construct states
        states = self._construct_states()

        cost = 0

        w = np.arange(len(states), 0, -1)

        for i, state in enumerate(states):
            qc = self._apply_varform_params(state, params)

            # Hamiltonian
            hamiltonian_eval = sample_hamiltonian(
                hamiltonian=self.hamiltonian, ansatz=qc, backend=self.backend
            )

            cost += w[i] * hamiltonian_eval

        return cost

    def _inate_optimizer_run(self):

        # Random initialization
        params = np.random.rand(self.n_parameters)

        optimal_params, energy, n_iters = self.optimizer.optimize(
            num_vars=self.n_parameters,
            objective_function=self._cost_function_1,
            initial_point=params,
        )

        self._ansatz_1_params = optimal_params
        self._first_optimization = True

    def _cost_excited_state(self, ind: int, params: list):
        cost = 0
        # Construct states
        states = self._construct_states()

        # Define Ansatz
        qc = self._apply_varform_params(states[ind], params)

        # Hamiltonian
        hamiltonian_eval = sample_hamiltonian(
            hamiltonian=self.hamiltonian, ansatz=qc, backend=self.backend
        )
        cost += hamiltonian_eval

        return cost, qc

    def run(self, index: int) -> (float, QuantumCircuit):
        """Run SSVQE for a given index.

        Args:
            index(int): Index of the given excited state.

        Returns:
            Energy: Energy of such excited state.
            State: State for such energy.
        """
        energy, state = self._cost_excited_state(index, self._ansatz_1_params)
        return energy, state


if __name__ == "__main__":
    import qiskit
    from qiskit import BasicAer

    optimizer = qiskit.algorithms.optimizers.COBYLA(maxiter=100)

    backend = QuantumInstance(
        backend=BasicAer.get_backend("qasm_simulator"), shots=10000
    )

    hamiltonian = 1 / 2 * (Z ^ I) + 1 / 2 * (Z ^ Z)
    ansatz = TwoLocal(hamiltonian.num_qubits, ["ry", "rz"], "cx", reps=1)
    algo = SSVQE(hamiltonian, ansatz, backend, optimizer)
    energy, state = algo.run(1)
    print(energy)
    print(state)
