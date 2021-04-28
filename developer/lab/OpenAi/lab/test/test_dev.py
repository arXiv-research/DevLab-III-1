import unittest
import pytest
from os import environ
from rl.experiment import run
from . import conftest
import pandas as pd


class DevTest(unittest.TestCase):

    @classmethod
    def test_clean_import(cls):
        print(dir())
        assert 'keras' not in dir(
        ), 'keras import should be contained within classes'
        assert 'matplotlib' not in dir(
        ), 'matplotlib import should be contained within classes'

    @classmethod
    def test_gym_tour(cls):
        data_df = run('dummy')
        assert isinstance(data_df, pd.DataFrame)

    @classmethod
    def test_q_table(cls):
        data_df = run('q_table')
        assert isinstance(data_df, pd.DataFrame)

    @unittest.skipIf(environ.get('CI'),
                     "Causing build to crash since it's unstable.")
    @classmethod
    def test_dqn_pass(cls):
        data_df = run('test_dqn_pass')
        max_total_rewards = data_df['max_total_rewards_stats_mean'][0]
        print(max_total_rewards)
        assert max_total_rewards > 50, 'dqn failed to hit max_total_rewards'

    # TODO cant run searches with these shits together, will hang everything wtf
    # @classmethod
    # def test_dqn_grid_search(cls):
    #     data_df = run('test_dqn_grid_search', param_selection=True)
    #     assert isinstance(data_df, pd.DataFrame)

    # TODO cant run searches with these shits together, will hang everything wtf
    # @classmethod
    # def test_dqn_random_search(cls):
    #     data_df = run('test_dqn_random_search', param_selection=True)
    #     assert isinstance(data_df, pd.DataFrame)
