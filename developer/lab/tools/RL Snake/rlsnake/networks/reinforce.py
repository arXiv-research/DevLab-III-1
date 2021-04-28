import os
import tensorflow.keras as keras
from tensorflow.keras.layers import Dense 

class ReinforceNetwork(keras.Model):
    """
    `ReinforceNetwork` is a network for REINFORCE algorithm.
    """
    def __init__(self, n_actions, fc1_dims=256, name='reinforce'):
        super(ReinforceNetwork, self).__init__()
        self.n_actions = n_actions
        
        self.fc1_dims = fc1_dims
        
        self.model_name = name
        
        self.layer1 = Dense(fc1_dims, activation='relu')
        self.output_layer = Dense(n_actions, activation='softmax')

    def call(self, inputs, training=None, mask=None):
        x = self.layer1(inputs, training=training)
        return self.output_layer(x, training=training)
