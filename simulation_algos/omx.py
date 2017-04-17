"""
TODO: Rename this file with <name>.py where <name> is your team name *all* in lower case with underscores
e.g. awesome_theory_of_om.py
"""
from simulation_game.buyer import Buyer
from simulation_game.seller import Seller

from cvxpy import *
import numpy as np
import math
import numpy as np
import numpy.random as rn
import gurobipy

# TODO: Replace the string "TeamName" below with your own team's name in camel case. For e.g. "AwesomeTheoryOfOM"
TEAM_NAME = "OMX"


class OMXBuyer(Buyer):
    """
    Implementation of your buyer bot
    TODO: rename this class as <Name>Buyer where <Name> is your team name in camel case e.g. AwesomeTheoryOfOMBuyer
    """
    def get_name(self):
        """
        :return: name of the team
        """
        return TEAM_NAME

    def _get_decision_impl(self, t, inventory_h, price_h, reserve_price, b_t_1_n, horizon, num_buyers):
        """
        TODO: Fill in your code here -- right now this skeleton code makes the decision to never buy
        """        
        return 1 if price_h[t]< reserve_price else 0
        

class OMXSeller(Seller):
    """
    Implementation of your seller bot
    TODO: rename this class as <Name>Seller where <Name> is your team name in camel case e.g. AwesomeTheoryOfOMSeller
    """
    def get_name(self):
        """
        :return: name of the team
        """
        return TEAM_NAME

    def _get_price_impl(self, t, inventory_h, price_h, price_scale, horizon, num_buyers):
        """
        TODO: Fill in your code here -- right now this skeleton code always gives an arbitrary price
        """
        price = self.decision(num_buyers, horizon, inventory_h[t],price_scale,10000,10)
        #print type(price)
        return price

    def decision(self,N,T,x0,l,M,s):
        p = Variable(T)
        y = Int(T,N+1)
        z = Variable(T,N+1)
        beta = Variable(s,T)
        w = Int(s-1,T)
        Nt = np.ones(T)*(N-(x0-xt))-sales*np.array([range(1,T+1)])
        Nt = Nt.clip(0)

        aux = np.array(range(100,0,-10))/100.
        aux2 = np.log(1.0/aux)*l
        aux4 = np.array(range(100,0,-10))/100.

        objective = Maximize(sum_entries(z*index))

        constraints = [sum_entries(y*index)<=x0, 
                       z>=0,
                       y*np.ones((N+1,1)) == 1,
                       p == beta.T*aux2,
                       beta[0,:] <= w[0,:],
                       beta[1,:] <= w[0,:]+w[1,:],
                       beta[2,:] <= w[1,:]+w[2,:],
                       beta[3,:] <= w[2,:]+w[3,:],
                       beta[4,:] <= w[3,:]+w[4,:],
                       beta[5,:] <= w[4,:]+w[5,:],
                       beta[6,:] <= w[5,:]+w[6,:],
                       beta[7,:] <= w[6,:]+w[7,:],
                       beta[8,:] <= w[7,:]+w[8,:],
                       beta[9,:] <= w[8,:],
                       sum_entries(beta, axis=0) == 1,
                       p[1:] <= p[:-1],
                       p>=0, y>=0,
                       beta >= 0,
                       w >= 0,
                       w <= 1]

        for t in range(T):
            for i in range(N+1):
                constraints.append(z[t,i] <= p[t])
                constraints.append(z[t,i]<=M*y[t,i])
                constraints.append(i*y[t,i] <= Nt[0,t]*(beta[:,t].T*aux4)) 
        prob = Problem(objective, constraints)
        result = prob.solve(solver = GUROBI, verbose = True)
        return p.value.item(0)
