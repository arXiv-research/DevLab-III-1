import os
import tensorflow.keras as keras
from tensorflow.keras.layers import Dense 

class ActorCriticNetwork(keras.Model):
    """
    `ActorCriticNetwork` is a network for actor-critic algorithm.
    """
    def __init__(self, n_actions, fc1_dims=256, fc2_dims=256, name='actorcritic'):
        super(ActorCriticNetwork, self).__init__()
        self.n_actions = n_actions
        
        self.fc1_dims = fc1_dims
        
        self.model_name = name

        self.fc1 = Dense(self.fc1_dims, activation='relu')
        self.actor = Dense(n_actions)
        self.critic = Dense(1, activation=None)

    def call(self, inputs, training=None, mask=None):
        value = self.fc1(inputs, training=training)

        return self.actor(value, training=training), self.critic(value, training=training)
