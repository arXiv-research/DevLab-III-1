import tensorflow as tf
import tensorflow_probability as tfp

import numpy as np

class TfAgent():
    def __init__(self, network):
        self.network = network

    def load_weights(self, weights_path):
        self.network.load_weights(weights_path)

    def get_action(self, state):
        if self.network.model_name == "reinforce":
            probs = self.network(np.array([state]))
            action_probabilities = tfp.distributions.Categorical(probs=probs)
            action = action_probabilities.sample()
            return int(action.numpy())
        else:
            action_logits_t, _ = self.network(np.array([state]))
            action = tf.random.categorical(action_logits_t, 1)[0, 0]
            return int(action.numpy())
