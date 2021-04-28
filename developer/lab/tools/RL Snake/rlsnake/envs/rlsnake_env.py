import gym
from gym import spaces

from rlsnake.game.snake import Snake

class RlSnakeEnv(gym.Env):
    """
    `RlSnakeEnv` (V0) is an gym environment for the game Snake.
    """
    metadata = {'render.modes': ['human']}

    last_info = []

    def __init__(self, n_x, n_y):
        self.game = Snake(n_x, n_y)

        self.action_space = spaces.Discrete(self.game.get_actions())

    def step(self, action):
        old_score = self.game.get_score()
        obs, game_over, info = self.game.step(action)
        if game_over:
            if self.game.get_score() == self.game.max_score:
                reward = 0
            else:
                reward = -1
        else:
            reward = 1*(self.game.get_score() - old_score)

        self.last_info = info

        return obs, reward, game_over, info

    def reset(self):
        return self.game.reset()
    def render(self, mode='human'):
        ...
    def close(self):
        ...
