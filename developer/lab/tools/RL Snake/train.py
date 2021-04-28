import argparse
import os
import random
import shutil
import sys

from typing import List, Tuple

import tensorflow as tf
from tensorflow import keras

import numpy as np

import tqdm

from rlsnake.envs.rlsnake_env_v1 import RlSnakeEnvV1
from rlsnake.networks.actor_critic import ActorCriticNetwork

parser = argparse.ArgumentParser(description='A trainer for actor-critic model to play Snake')
parser.add_argument('--x', type=int, default=4, metavar='X',
                help='number of tiles in horizontal direction (default: 4)')
parser.add_argument('--y', type=int, default=4, metavar='Y',
                help='number of tiles in vertical direction (default: 4)')
parser.add_argument('--visibility-range', type=int, default=4, metavar='VR',
                help='visibility range in each direction for the snake (default: 4)')
parser.add_argument('--episodes', type=int, default=1000, metavar='E',
                help='number of episodes to train (default: 1000)')
parser.add_argument('--max-steps', type=int, default=100, metavar='MS',
                    help='how many maximal steps per episode (default: 100)')
parser.add_argument('--gamma', type=float, default=0.99, metavar='G',
                    help='discount factor (default: 0.99)')
parser.add_argument('--neurons', type=int, default=256, metavar='NE',
                    help='how many neurons in each layer (default: 256)')
parser.add_argument('--learning-rate', type=float, default=1e-4, metavar='L',
                    help='learning rate (default: 1e-4)')
parser.add_argument('--seed', type=int, default=42, metavar='N',
                    help='random seed (default: 42)')
parser.add_argument('--run-id', type=str, required=True, metavar='RUN_ID',
                    help='the identifier for the training run.')
parser.add_argument('--force', dest='force', action='store_const',
                    const=True, default=False,
                    help='force overwrite already existing results')
parser.add_argument('--from-checkpoint', type=str, metavar='CHECKPOINT_FILE',
                    help='start training from a previous checkpoint file')
args = parser.parse_args()

results_path = 'results/' + args.run_id
if ((os.path.isdir(results_path) or os.path.isfile(results_path)) and not args.force):
    print(results_path + " already exists. Exiting...")
    exit(1)
elif ((os.path.isdir(results_path) or os.path.isfile(results_path)) and args.force == True):
    shutil.rmtree(results_path)

writer = tf.summary.create_file_writer(results_path)

env = RlSnakeEnvV1(args.x, args.y, args.visibility_range)

env.seed(args.seed)
np.random.seed(args.seed)
tf.random.set_seed(args.seed)
random.seed(args.seed)

network = ActorCriticNetwork(env.action_space.n, fc1_dims=args.neurons, fc2_dims=args.neurons)

eps = np.finfo(np.float32).eps.item()

# Hyperparameters
n_iterations = args.episodes
n_max_steps = args.max_steps
discount_factor = args.gamma

network.compile(keras.optimizers.Adam(lr=args.learning_rate))

def env_step(action: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Returns state, reward and done flag given an action."""

    state, reward, done, _ = env.step(action)
    return (state.astype(np.float32),
            np.array(reward, np.float32),
            np.array(done, np.int32))

def tf_env_step(action: tf.Tensor) -> List[tf.Tensor]:
    return tf.numpy_function(env_step, [action],
                            [tf.float32, tf.float32, tf.int32])

def run_episode(
        initial_state: tf.Tensor,
        model: tf.keras.Model,
        max_steps: int) -> List[tf.Tensor]:
    """Runs a single episode to collect training data."""
    action_probs = tf.TensorArray(dtype=tf.float32, size=0, dynamic_size=True)
    values = tf.TensorArray(dtype=tf.float32, size=0, dynamic_size=True)
    rewards = tf.TensorArray(dtype=tf.float32, size=0, dynamic_size=True)

    initial_state_shape = initial_state.shape
    state = initial_state

    for t in tf.range(n_max_steps):
        # Convert state into a batched tensor (batch size = 1)
        state = tf.expand_dims(state, 0)

        action_logits_t, value = model(state)

        # Sample next action from the action probability distribution
        action = tf.random.categorical(action_logits_t, 1)[0, 0]
        action_probs_t = tf.nn.softmax(action_logits_t)

        # Store critic values
        values = values.write(t, tf.squeeze(value))

        # Store log probability of the action chosen
        action_probs = action_probs.write(t, action_probs_t[0, action])

        # Apply action to the environment to get next state and reward
        state, reward, done = tf_env_step(action)
        state.set_shape(initial_state_shape)

        rewards = rewards.write(t, reward)

        if tf.cast(done, tf.bool):
            break

    action_probs = action_probs.stack()
    values = values.stack()
    rewards = rewards.stack()

    return action_probs, values, rewards

def get_expected_return(
    rewards: tf.Tensor,
    gamma: float,
    standardize: bool = True) -> tf.Tensor:
    """Compute expected returns per timestep."""

    n = tf.shape(rewards)[0]
    returns = tf.TensorArray(dtype=tf.float32, size=n)

    # Start from the end of `rewards` and accumulate reward sums
    # into the `returns` array
    rewards = tf.cast(rewards[::-1], dtype=tf.float32)
    discounted_sum = tf.constant(0.0)
    discounted_sum_shape = discounted_sum.shape
    for i in tf.range(n):
        reward = rewards[i]
        discounted_sum = reward + gamma * discounted_sum
        discounted_sum.set_shape(discounted_sum_shape)
        returns = returns.write(i, discounted_sum)
    returns = returns.stack()[::-1]

    if standardize:
        returns = ((returns - tf.math.reduce_mean(returns)) /
                    (tf.math.reduce_std(returns) + eps))

    return returns

def save_model(file_path):
    network.save_weights(file_path)
    print('Saved model in ' + file_path)

def load_weights():
    network.load_weights(args.from_checkpoint)
    print('Loaded previously trained model checkpoint')

def writeSettings():
    # TODO: Make the settings machine readable and reuse in validation runs or when start training from checkpoint
    f = open(results_path + '/settings.txt', 'w')
    f.write('x: ' + str(args.x) + "\n")
    f.write('y: ' + str(args.y) + "\n")
    f.write('run-id: ' + str(args.run_id) + "\n")
    f.write('episodes: '+ str(args.episodes) + "\n")
    f.write('max steps: ' + str(n_max_steps) + "\n")
    f.write('gamma: ' + str(args.gamma) + "\n")
    f.write('seed: ' + str(args.seed) + "\n")
    f.write('learning-rate: ' + str(args.learning_rate) + "\n")
    f.write('network-name: ' + str(network.model_name) + "\n")
    f.write('neurons: ' + str(network.fc1_dims) + "\n")
    f.close()

huber_loss = tf.keras.losses.Huber(reduction=tf.keras.losses.Reduction.SUM)

def compute_loss(
    action_probs: tf.Tensor,
    values: tf.Tensor,
    returns: tf.Tensor) -> tf.Tensor:
    """Computes the combined actor-critic loss."""

    advantage = returns - values

    action_log_probs = tf.math.log(action_probs)
    actor_loss = -tf.math.reduce_sum(action_log_probs * advantage)

    critic_loss = huber_loss(values, returns)

    return actor_loss + critic_loss

def format_num(n):
    f = '{: 06.2f}'.format(n)
    return f

@tf.function
def train_step(
    initial_state: tf.Tensor,
    model: tf.keras.Model,
    gamma: float) -> tf.Tensor:
    """Runs a model training step."""

    with tf.GradientTape() as tape:
        # Run the model for one episode to collect training data
        action_probs, values, rewards = run_episode(
            initial_state, model, n_max_steps)

        # Calculate expected returns
        returns = get_expected_return(rewards, gamma)

        # Convert training data to appropriate TF tensor shapes
        action_probs, values, returns = [
            tf.expand_dims(x, 1) for x in [action_probs, values, returns]]

        # Calculating loss values to update our network
        loss = compute_loss(action_probs, values, returns)

    # Compute the gradients from the loss
    grads = tape.gradient(loss, model.trainable_variables)

    # Apply the gradients to the model's parameters
    model.optimizer.apply_gradients(zip(grads, model.trainable_variables))

    episode_reward = tf.math.reduce_sum(rewards)

    # tf.summary.scalar("loss", loss, step=iteration)

    return episode_reward

def main():
    if args.from_checkpoint:
        load_weights()

    writeSettings()
    running_reward = 0

    with writer.as_default():
        with tqdm.trange(n_iterations) as t:
            for iteration in t:
                initial_state = tf.constant(env.reset(), dtype=tf.float32)
                episode_reward = float(train_step(
                    initial_state, network, args.gamma))

                running_reward = episode_reward*0.01 + running_reward*.99

                total_moves = env.last_info[0]

                t.set_description(f'Episode {iteration}')
                t.set_postfix(
                    episode_reward=tf.squeeze(episode_reward).numpy(),
                    running_reward=tf.squeeze(running_reward).numpy(),
                    total_moves=total_moves)

                # train(all_values, all_states, total_rewards, all_actions, iteration)
                tf.summary.scalar("total rewards", episode_reward, step=iteration)
                tf.summary.scalar("running reward", running_reward, step=iteration)
                tf.summary.scalar("total moves", total_moves, step=iteration)
                writer.flush()

                if iteration > 0 and iteration % 5000 == 0:
                    save_model(results_path + '/model_checkpoint_' + str(iteration))

    print("\n")

    save_model(results_path + '/final_model')

    return 0

if __name__ == "__main__":
    sys.exit(main())
