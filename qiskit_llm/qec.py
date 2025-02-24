import qec_util
import qec_functions

from keras.models import load_model
from rl.memory import SequentialMemory
from rl.policy import GreedyQPolicy, LinearAnnealedPolicy, EpsGreedyQPolicy
from rl.agents.dqn import DQNAgent
from rl.callbacks import FileLogger
from keras.optimizers import Adam
import numpy as np

from matplotlib import pyplot as plt

class DecoderModel():
    def __init__(self, **kwargs):
        """
        This function takes the following arguments:
        - fixed_configs: fixed configuration settings for the DQN agent
        - var_configs: variable configuration settings for the DQN agent
        """
        self.fixed_configs = kwargs.get("fixed_configs", qec_util.fixed_configs)
        self.var_configs = kwargs.get("var_configs", qec_util.variable_configs)

        # Set all configurations of DQN agent
        self.all_configs = {}
        for key in self.fixed_configs:
            self.all_configs[key] = self.fixed_configs[key]
        for key in self.var_configs:
            self.all_configs[key] = self.var_configs[key]

        self.logging_dir = os.path.join(os.getcwd(), "logging_dir/")
        static_decoder_path = os.path.join(os.getcwd(), "referee_decoders/nn_d5_X_p5")

        logging_path = os.path.join(logging_directory,"training_history.json")
        self.logging_callback = FileLogger(filepath = logging_path,interval = self.all_configs["print_freq"])

        self.static_decoder = load_model(static_decoder_path)

        # Set up RL environment
        self.env = qec_util.Surface_Code_Environment_Multi_Decoding_Cycles(
            d=self.all_configs["d"],
            p_phys=self.all_configs["p_phys"],
            p_meas=self.all_configs["p_meas"],
            error_model=self.all_configs["error_model"],
            use_Y=self.all_configs["use_Y"],
            volume_depth=self.all_configs["volume_depth"],
            static_decoder=self.static_decoder
        )

    # Function to load pretrained model
    def set_model(self, model_weights_path):
        """
        This function takes the following arguments:
        - model_weights_path: path to model weights
        """

        model = qec_functions.build_convolutional_nn(self.all_configs["c_layers"], self.all_configs["ff_layers"],
            self.env.observation_space.shape, self.env.num_actions)
        
        memory = SequentialMemory(limit=self.all_configs["buffer_size"], window_length=1)
        policy = GreedyQPolicy(masked_greedy=True)
        test_policy = GreedyQPolicy(masked_greedy=True)

        self.dqn = DQNAgent(model=model,
            nb_actions=self.env.num_actions,
            memory=memory,
            nb_steps_warmup=self.all_configs["learning_starts"],
            target_model_update=self.all_configs["target_network_update_freq"],
            policy=policy,
            test_policy=test_policy,
            gamma=self.all_configs["gamma"],
            enable_dueling_network=self.all_configs["dueling"])

        self.dqn.compile(Adam(lr=self.all_configs["learning_rate"]))

        self.dqn.model.load_weights(model_weights_path)

    # Function to predict corrections needed to resolve errors
    def predict_correction(self, faulty_syndromes = None, p_phys = None, p_meas = None):
        """
        This function takes the following arguments:
        - faulty_syndroms: real faulty syndroms generated (otherwise function will generate random errors based on the error model)
        - p_phys: physical error probability
        - p_meas: measurement error probability
        """

        if not self.dqn:
            raise AttributeError("DQN Agent has not been assigned, either call train_model or set_model") 

        d = self.all_configs["d"]
        if not p_phys:
            p_phys = self.all_configs["p_phys"]
        if not p_meas:
            p_meas = self.all_configs["p_meas"]

        if not faulty_syndromes:
            qubits = qec_functions.generateSurfaceCodeLattice(d)

            hidden_state = np.zeros((d, d), int)

            faulty_syndromes = []
            for j in range(d):
                error = qec_functions.generate_error(d, p_phys, self.all_configs["error_model"])
                hidden_state = qec_functions.obtain_new_error_configuration(hidden_state, error)
                current_true_syndrome = qec_functions.generate_surface_code_syndrome_NoFT_efficient(hidden_state, qubits)
                current_faulty_syndrome = qec_functions.generate_faulty_syndrome(current_true_syndrome, p_meas)
                faulty_syndromes.append(current_faulty_syndrome)

        input_state = np.zeros((d+1, 2*d + 1, 2*d + 1), int)
        for j in range(d):
            input_state[j, :, :] = self.env.padding_syndrome(faulty_syndromes[j])

        corrections = []
        still_decoding = True
        
        while still_decoding:
            action = self.dqn.forward(input_state)

            if action not in corrections and action != self.env.identity_index:
                corrections.append(action)
                input_state[d, :, :] = self.env.padding_actions(corrections)
            else:
                still_decoding = False

        return corrections

    # This function will train a DQN agent
    # WARNING: This can take more than 12 hours depending on GPU resources
    def train_model(showTrainingHistory = False):
        
        memory = SequentialMemory(limit=self.all_configs["buffer_size"], window_length=1)
        policy = LinearAnnealedPolicy(EpsGreedyQPolicy(masked_greedy=self.all_configs["masked_greedy"]),
            attr="eps", 
            value_max=self.all_configs["max_eps"],
            value_min=self.all_configs["final_eps"],
            value_test=0.0,
            nb_steps=self.all_configs["exploration_fraction"])
        test_policy = GreedyQPolicy(masked_greedy=True)

        model = qec_functions.build_convolutional_nn(self.all_configs["c_layers"],
            self.all_configs["ff_layers"],
            self.env.observation_space.shape,
            self.env.num_actions)

        self.dqn = DQNAgent(model=model,
            nb_actions=self.env.num_actions,
            nb_steps_warmup=self.all_configs["learning_starts"],
            target_model_update=self.all_configs["target_network_update_freq"],
            policy=policy,
            test_policy=test_policy,
            gamma=self.all_configs["gamma"],
            enable_dueling_network=self.all_configs["dueling"])

        self.dqn.compile(Adam(lr=self.all_configs["learning_rate"]))

        history = self.dqn.fit(self.env, 
            nb_steps=self.all_configs["max_timesteps"], 
            action_repetition=1, 
            callbacks=[self.logging_callback], 
            verbose=2,
            visualize=False, 
            nb_max_start_steps=0, 
            start_step_policy=None, 
            log_interval=self.all_configs["print_freq"],
            nb_max_episode_steps=None, 
            episode_averaging_length=self.all_configs["rolling_average_length"], 
            success_threshold=self.all_configs["success_threshold"],
            stopping_patience=self.all_configs["stopping_patience"],
            min_nb_steps=self.all_configs["exploration_fraction"],
            single_cycle=False)

        weights_file = os.path.join(self.logging_dir, "dqn_weights.h5f")
        self.dqn.save_weights(weights_file, overwrite=True)
        
        if showTrainingHistory:
            training_history = history.history["episode_lifetimes_rolling_avg"]

            plt.plot(training_history)
            plt.x_label("Episode")
            plt.y_label("Rolling Average Qubit Lifetime")
            plt.title("Training History")
            plt.show()
