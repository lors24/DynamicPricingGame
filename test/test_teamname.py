"""
You can use this file to test your code (also if you want to write automated/unit-tests that might be a good idea)
"""
from simulation_algos.omx import OMXBuyer, OMXSeller
from simulation_game.buyer import MyopicBuyer
from simulation_game.seller import DummySeller
from simulation_game.simulation import simulate

import numpy.random as rn

# Set these parameters how you want for testing
price_scale = 20
mc_trials = 10
x_0 = 4
horizon = 10


def test_my_teams_performance():
    """
    This function is where you can write a test for your buyer and seller bot, and evaluate performance
    """
    rn.seed(1234)
    buyer1 = OMXBuyer()
    seller1 = OMXSeller()
    buyer2 = MyopicBuyer("Steve")
    seller2 = DummySeller("Steve")
    teams = [(buyer1, seller1), (buyer2, seller2), (buyer2, seller2), (buyer2, seller2), (buyer2, seller2),(buyer2, seller2),(buyer2, seller2)]
    mean_revenue, mean_cs = simulate(teams, horizon, x_0, mc_trials, price_scale)
    print mean_revenue, mean_cs

test_my_teams_performance()