from slm_lab.env.base import BaseEnv
from slm_lab.env.wrapper import make_gym_env
from slm_lab.env.vec_env import make_gym_venv
from slm_lab.env.registration import try_register_env
from slm_lab.lib import logger, util
from slm_lab.lib.decorator import lab_api
import gym
import numpy as np
import pydash as ps
import roboschool
import pybullet_envs


logger = logger.get_logger(__name__)


class OpenAIEnv(BaseEnv):
    '''
    Wrapper for OpenAI Gym env to work with the Lab.

    e.g. env_spec
    "env": [{
        "name": "PongNoFrameskip-v4",
        "frame_op": "concat",
        "frame_op_len": 4,
        "normalize_state": false,
        "reward_scale": "sign",
        "num_envs": 8,
        "max_t": null,
        "max_frame": 1e7
    }],
    '''

    def __init__(self, spec):
        super().__init__(spec)
        try_register_env(spec)  # register if it's a custom gym env
        seed = ps.get(spec, 'meta.random_seed')
        episode_life = util.in_train_lab_mode()
        if self.is_venv:  # make vector environment
            self.u_env = make_gym_venv(name=self.name, num_envs=self.num_envs, seed=seed, frame_op=self.frame_op, frame_op_len=self.frame_op_len, image_downsize=self.image_downsize, reward_scale=self.reward_scale, normalize_state=self.normalize_state, episode_life=episode_life)
        else:
            self.u_env = make_gym_env(name=self.name, seed=seed, frame_op=self.frame_op, frame_op_len=self.frame_op_len, image_downsize=self.image_downsize, reward_scale=self.reward_scale, normalize_state=self.normalize_state, episode_life=episode_life)
        if self.name.startswith('Unity'):
            # Unity is always initialized as singleton gym env, but the Unity runtime can be vec_env
            self.num_envs = self.u_env.num_envs
            # update variables dependent on num_envs
            self._infer_venv_attr()
            self._set_clock()
        self._set_attr_from_u_env(self.u_env)
        self.max_t = self.max_t or self.u_env.spec.max_episode_steps
        assert self.max_t is not None
        logger.info(util.self_desc(self))

    def seed(self, seed):
        self.u_env.seed(seed)

    @lab_api
    def reset(self):
        self.done = False
        state = self.u_env.reset()
        if self.to_render:
            self.u_env.render()
        return state

    @lab_api
    def step(self, action):
        if not self.is_discrete and self.action_dim == 1:  # guard for continuous with action_dim 1, make array
            action = np.expand_dims(action, axis=-1)
        state, reward, done, info = self.u_env.step(action)
        self._update_total_reward(info)
        if self.to_render:
            self.u_env.render()
        if not self.is_venv and self.clock.t > self.max_t:
            done = True
        self.done = done
        return state, reward, done, info

    @lab_api
    def close(self):
        self.u_env.close()
