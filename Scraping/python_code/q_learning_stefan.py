import copy
import random
from collections import deque, namedtuple

import numpy as np
import matplotlib.pyplot as plt
import gym
import torch

from qiskit import Aer
from qiskit import QuantumCircuit
from qiskit.utils import QuantumInstance
from qiskit.circuit import Parameter
from qiskit.opflow import StateFn, PauliSumOp, ListOp, AerPauliExpectation, Gradient

from qiskit_machine_learning.neural_networks import OpflowQNN
from qiskit_machine_learning.connectors import TorchConnector

from torch import Tensor
from torch.nn import Parameter as TorchParameter
from torch.optim import Adam

from time import time


def build_quantum_model(n_qubits, n_layers, is_target_model=False):
    name_prefix = ''
    if is_target_model:
        name_prefix = 'target_'

    circuit = QuantumCircuit(n_qubits)
    data_params = [
        Parameter(f'{name_prefix}x_{i}_{j}') for i in range(n_qubits) for j in range(n_layers)]
    data_params_copy = copy.deepcopy(data_params)[::-1]
    data_weight_params = [
        Parameter(f'{name_prefix}d_{i}_{j}') for i in range(n_qubits) for j in range(n_layers)]
    trainable_params = []

    for layer in range(n_layers):
        for qubit in range(n_qubits):
            circuit.rx(data_params.pop(), qubit)
            var_param_y = Parameter(f't_y_{layer}_{qubit}')
            var_param_z = Parameter(f't_z_{layer}_{qubit}')
            trainable_params += [var_param_y, var_param_z]
            circuit.ry(var_param_y, qubit)
            circuit.rz(var_param_z, qubit)

        for qubit in range(n_qubits):
            circuit.cz(qubit, (qubit+1) % n_qubits)

        circuit.barrier()

    # print(circuit)
    # exit()

    return circuit, trainable_params, data_params_copy, data_weight_params


def build_readout_ops(agent):
    action_left = PauliSumOp.from_list([('ZZII', 1.0)])
    action_right = PauliSumOp.from_list([('IIZZ', 1.0)])

    readout_op = ListOp([
        ~StateFn(action_left) @ StateFn(agent),
        ~StateFn(action_right) @ StateFn(agent)
    ])

    return readout_op, action_left, action_right


def compute_q_vals(states, model, observable_weights, data_weights, n_layers, grad=True):
    input_states = []
    for state in states:
        extended_state = torch.arctan(Tensor(state).repeat(1, n_layers) * data_weights)
        input_states.append(extended_state)

    states_tensor = torch.reshape(torch.stack(input_states), (len(input_states), n_layers*4))
    if grad:
        res = model(states_tensor)
    else:
        with torch.no_grad():
            res = model(states_tensor)

    q_vals = (res + 1) / 2

    q_vals[:, 0] *= observable_weights[0]
    q_vals[:, 1] *= observable_weights[1]

    return q_vals


def train_step(
        memory,
        model,
        target_model,
        batch_size,
        observable_weights,
        data_weights,
        target_observable_weights,
        target_data_weights,
        model_optimizer,
        observables_optimizer,
        data_weights_optimizer,
        loss,
        gamma,
        n_layers):
    transitions = random.sample(memory, batch_size)
    batch_memories = Transition(*zip(*transitions))
    batch_states = batch_memories.state
    batch_actions = batch_memories.action
    batch_next_states = batch_memories.next_state
    batch_done = batch_memories.done
    batch_rewards = np.ones(batch_size)

    action_masks = []
    one_hot_actions = {0: [1, 0], 1: [0, 1]}
    for action in batch_actions:
        action_masks.append(one_hot_actions[action])

    model_optimizer.zero_grad()
    observables_optimizer.zero_grad()
    data_weights_optimizer.zero_grad()

    q_vals = compute_q_vals(
        batch_states, model, observable_weights, data_weights, n_layers)
    q_vals_next = compute_q_vals(
        batch_next_states, target_model, target_observable_weights, target_data_weights, n_layers, grad=False)

    target_q_vals = torch.Tensor(batch_rewards) + torch.Tensor(
        np.ones(batch_size) * gamma) * torch.max(q_vals_next, 1).values * (1 - torch.Tensor(batch_done))
    reduced_q_vals = torch.sum(q_vals * torch.Tensor(action_masks), dim=1)

    error = loss(reduced_q_vals, target_q_vals)
    print('start backward()')
    error.backward()
    print('end backward()')
    model_optimizer.step()
    observables_optimizer.step()
    data_weights_optimizer.step()


# set up Qiskit backend and Gym
backend = Aer.get_backend('statevector_simulator')
quantum_instance = QuantumInstance(backend)
env = gym.make("CartPole-v0")

# set hyperparameters for deep Q-learning
n_qubits = 4
n_layers = 5

gamma = 0.99  # Q-learning discount factor
epsilon = 1.0  # epsilon greedy policy initial value
epsilon_min = 0.01  # minimum value of epsilon
epsilon_decay = 0.99  # decay rate of epsilon

n_episodes = 3000
batch_size = 16
update_qnet_after = 1  # agent update interval
update_target_after = 1  # target network update interval

# set up replay memory
Transition = namedtuple('Transition', (
    'state', 'action', 'next_state', 'done'))
max_memory_len = 10000
replay_memory = deque(maxlen=max_memory_len)

grad_method='param_shift'
# grad_method='fin_diff'

# set up model
agent, params, data_params, data_weight_params = build_quantum_model(
    n_qubits, n_layers)

observable_weights = TorchParameter(Tensor([1, 1]))
data_weights = TorchParameter(Tensor(np.ones(shape=n_qubits*n_layers)))

readout_op, action_left, action_right = build_readout_ops(agent)
qnn_opflow = OpflowQNN(
    readout_op, data_params, params, exp_val=AerPauliExpectation(),
    gradient=Gradient(grad_method),
    quantum_instance=quantum_instance, input_gradients=False)

model = TorchConnector(qnn_opflow)


# set up target model that is used to compute target Q-values
# (not trained, only updated with Q-model's parameters at fixed intervals)
target_agent, target_params, target_data_params, target_data_weight_params = build_quantum_model(
    n_qubits, n_layers, is_target_model=True)
target_observable_weights = Tensor([1, 1])
target_data_weights = TorchParameter(Tensor(np.ones(shape=n_qubits*n_layers)))
target_readout_op, _, _ = build_readout_ops(target_agent)
target_qnn = OpflowQNN(
    target_readout_op, target_data_params, target_params, exp_val=AerPauliExpectation(),
    gradient=Gradient(grad_method),
    quantum_instance=quantum_instance)

target_qnn.input_gradients = False
target_model = TorchConnector(target_qnn)
target_model.load_state_dict(model.state_dict())

# set up optimizers
model_optimizer = Adam(model.parameters(), lr=0.001)
observables_optimizer = Adam([observable_weights], lr=0.1)
data_weights_optimizer = Adam([data_weights], lr=0.1)
loss = torch.nn.MSELoss()

episode_rewards = []

print('start training')
t_start_training = time()

for episode in range(n_episodes):
    t_start_episode = time()
    episode_reward = 0
    state = env.reset()
    for time_step in range(200):
        # env.render()

        print(f'episode {episode}, time_step {time_step}')

        # choose action based on epsilon greedy policy
        if random.random() > epsilon:
            with torch.no_grad():
                q_vals = compute_q_vals([state], model, observable_weights, data_weights, n_layers)
                action = int(torch.argmax(q_vals).numpy())
        else:
            action = np.random.choice(2)

        # take step in environment and collect reward
        next_state, reward, done, _ = env.step(action)
        episode_reward += 1

        # store transition in memory (without reward as it is always 1)
        replay_memory.append(Transition(state, action, next_state, int(done)))
        state = next_state

        # perform one step of parameter updates
        if len(replay_memory) > batch_size and time_step % update_qnet_after == 0:
            train_step(
                replay_memory,
                model,
                target_model,
                batch_size,
                observable_weights,
                data_weights,
                target_observable_weights,
                target_data_weights,
                model_optimizer,
                observables_optimizer,
                data_weights_optimizer,
                loss,
                gamma,
                n_layers)

        # update target model parameters
        if time_step % update_target_after == 0:
            with torch.no_grad():
                target_model.load_state_dict(model.state_dict())
                target_observable_weights = copy.deepcopy(observable_weights.data)
                target_data_weights = copy.deepcopy(data_weights.data)

        if done:
            break

    episode_rewards.append(episode_reward)
    epsilon = max(epsilon_min, epsilon * epsilon_decay)

    t_end_episode = time()
    print('episode time:', (t_end_episode - t_start_episode))

    if episode > 0:
        print(f'Episode {episode}, episode reward: {episode_reward}, average reward: {np.mean(episode_rewards[-100:])}')
    else:
        print(f'Episode {episode}, episode reward: {episode_reward}')

t_end_training = time()
print('training time:', (t_end_training - t_start_training))

plt.plot(episode_rewards)
plt.ylabel("Score")
plt.xlabel("Episode")
plt.show()
