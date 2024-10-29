import numpy as np
import keras
import tensorflow
import gym

import rl as rl
from rl.agents.dqn import DQNAgent
from rl.policy import BoltzmannQPolicy, EpsGreedyQPolicy, LinearAnnealedPolicy, GreedyQPolicy
from rl.memory import SequentialMemory
from rl.callbacks import FileLogger

from Function_Library import *
from Environments import *

import json
import copy
import sys
import os
import shutil 
import datetime
import pickle

from matplotlib import pyplot as plt

from keras.src.saving import serialization_lib
serialization_lib.enable_unsafe_deserialization()

fixed_configs = {
    "d": 5, # Lattice Width
    "use_Y": False, # true => agent performs Pauli Y, false => only X and Z
    "train_freq": 1, # number of interaction steps between W updates
    "batch_size": 32,
    "print_freq": 250,
    "rolling_average_length": 500,
    "stopping_patience": 500,
    "error_model": "X", # Noise model: X flips or DP (depolarising noise)
    "c_layers": [[64, 3, 2], [32, 2, 1], [32, 2, 1]], # conv. layers of deeqQ net
    "ff_layers": [[512, 0.2]], # layers of ff net
    "max_timesteps": 100000,
    "volume_depth": 5, # number of syndrome measures for each extraction
    "testing_length": 101,
    "buffer_size": 50000,
    "dueling": True,
    "masked_greedy": False,
    "static_decoder": True # Should be True when within fault tolerant setting
}

variable_configs = {
    "p_phys": 0.001, # phys error prob
    "p_meas": 0.001, # meas error prob
    "success_threshold": 10000, # qubit lifetime at which success
    "learning_starts": 1000,
    "learning_rate": 0.00001,
    "exploration_fraction": 100000,
    "max_eps": 1.0,
    "target_network_update_freq": 5000, # clone target network off deepQ agent (generates target Qfunc)
    "gamma": 0.99, # discount rate for calc Qvals
    "final_eps": 0.02
}

logging_dir = os.path.join(os.getcwd(), "logging_dir/")
static_decoder_path = os.path.join(os.getcwd(), "referee_decoders/nn_d5_X_p5")

all_configs = {}

for key in fixed_configs.keys():
  all_configs[key] = fixed_configs[key]
for key in variable_configs.keys():
  all_configs[key] = variable_configs[key]

static_decoder = load_model(static_decoder_path)
log_path = os.path.join(logging_dir, "training_history.json")
logging_callback = FileLogger(filepath = log_path, interval = all_configs["print_freq"])

env = Surface_Code_Environment_Multi_Decoding_Cycles(d=all_configs["d"],
  p_phys=all_configs["p_phys"],
  p_meas=all_configs["p_meas"],
  error_model=all_configs["error_model"],
  use_Y=all_configs["use_Y"],
  volume_depth=all_configs["volume_depth"],
  static_decoder=static_decoder)

memory = SequentialMemory(limit=all_configs["buffer_size"], window_length=1)
policy = LinearAnnealedPolicy(EpsGreedyQPolicy(masked_greedy=all_configs["masked_greedy"]),
  attr="eps", value_max=all_configs["max_eps"],
  value_min=all_configs["final_eps"],
  value_test=0.0,
  nb_steps=all_configs["exploration_fraction"])

test_policy = GreedyQPolicy(masked_greedy=True)

model = build_convolutional_nn(all_configs["c_layers"],
  all_configs["ff_layers"],
  env.observation_space.shape,
  env.num_actions)

dqn = DQNAgent(model=model,
  nb_actions=env.num_actions,
  memory=memory,
  nb_steps_warmup=all_configs["learning_starts"],
  target_model_update=all_configs["target_network_update_freq"],
  policy=policy,
  test_policy=test_policy,
  gamma=all_configs["gamma"],
  enable_dueling_network=all_configs["dueling"])

dqn.compile(Adam(lr=all_configs["learning_rate"]))

now = datetime.datetime.now()
started_file = os.path.join(logging_dir, "started_at.p")
pickle.dump(now, open(started_file, "wb"))

history = dqn.fit(env,
  nb_steps=all_configs["max_timesteps"],
  action_repetition=1,
  callbacks=[logging_callback],
  verbose=2,
  visualize=False,
  nb_max_start_steps=0,
  start_step_policy=None,
  log_interval=all_configs["print_freq"],
  nb_max_episode_steps=None,
  episode_averaging_length=all_configs["rolling_average_length"],
  success_threshold=all_configs["success_threshold"],
  stopping_patience=all_configs["stopping_patience"],
  min_nb_steps=all_configs["exploration_fraction"],
  single_cycle=False)

weights_file = os.path.join(logging_dir, "dqn_weights.h5f")
dqn.save_weights(weights_file, overwrite=True)

training_history = history.history["episode_lifetime_rolling_avg"]
plt.plot(training_history)
plt.xlabel("Episode")
plt.ylabel("Rolling Avg Qubit Lifetime")
_ = plt.title("Training History")