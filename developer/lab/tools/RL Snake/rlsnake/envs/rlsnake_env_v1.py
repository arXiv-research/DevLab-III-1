import gym
from gym import spaces

from rlsnake.game.snake import Snake

class RlSnakeEnvV1(gym.Env):
    """
    `RlSnakeEnvV1` is an gym environment for the game Snake.
    """
    metadata = {'render.modes': ['human']}

    last_info = []

    def __init__(self, n_x, n_y, visibility_range=4):
        self.game = Snake(n_x, n_y)
        self.game.set_visibility_range(visibility_range)

        self.action_space = spaces.Discrete(self.game.get_actions())

    def step(self, action):
        old_score = self.game.get_score()
        _, game_over, info = self.game.step(action)
        if game_over:
            if self.game.get_score() == self.game.max_score:
                reward = 0
            else:
                reward = -1
        else:
            reward = 1*(self.game.get_score() - old_score) - 0.01

        self.last_info = info

        return self.game.get_view_obs(), reward, game_over, info

    def reset(self):
        self.game.reset()
        return self.game.get_view_obs()
    def render(self, mode='human'):
        ...
    def close(self):
        ...
