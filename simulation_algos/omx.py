"""
TODO: Rename this file with <name>.py where <name> is your team name *all* in lower case with underscores
e.g. awesome_theory_of_om.py
"""
from simulation_game.buyer import Buyer
from simulation_game.seller import Seller

from cvxpy import *
import numpy as np
import math
import numpy.random as rn
import gurobipy
from scipy.special import comb

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

    def decide_prices(self,N,T,t,x0,xt,l,M,s,p0):

        index = np.array(range(N+1))
        # Construct the problem.

        #Variables

        p = Variable(T)
        y = Int(T,N+1)
        z = Variable(T,N+1)
        beta = Variable(s,T)
        w = Int(s-1,T)
        #sales = (x0-xt)/(t+1)
        sales = 0.8
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
                       p[0]<=p0,
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
        result = prob.solve(solver = GUROBI)
        prices = p.value
        return prices, Nt 


    def _get_decision_impl(self, t, inventory_h, price_h, reserve_price, b_t_1_n, horizon, num_buyers):
        """
        TODO: Fill in your code here -- right now this skeleton code makes the decision to never buy
        """    
 
        N = num_buyers
        T = horizon - t+1
        x0 = inventory_h[0]
        xt = inventory_h[t]
        M = 10000
        s = 10
        Y = np.zeros(t+1)
        Nt = np.zeros(t+1)
        lambdas = np.zeros(t+1)
        lambdas[0] = reserve_price
        Nt[0] = N

        if reserve_price < price_h[t]:
            return 0
        else:
            if t == 0:
                l = reserve_price
            elif t==horizon and sum(b_t_1_n<1):
                return 1
            else:
                for ts in range(1,t+1):
                    Y[ts-1] = inventory_h[ts-1]-inventory_h[ts]
                    Nt[ts] = Nt[ts-1] - Y[ts-1]
                    if Y[ts-1] == 0 or Nt[ts-1] == 0:
                        lambdas[ts] = lambdas[ts-1]/2
                    else:
                        lambdas[ts] = -price_h[ts-1]/(math.log(Y[ts-1]/Nt[ts-1]))
                l = np.mean(lambdas)
            prices, NT = self.decide_prices(N,T,t,x0,xt,l,M,s,price_h[t])

            
            suma = np.zeros((T,1))
            for ts in range(T):
                if inventory_h[t]>1: 
                    print "here"
                    #print math.floor(inventory_h[t]-(x0-xt)*ts/t)
                    #print "cap", cap
                    for s in range(inventory_h[]):
                        if NT[0,ts]-1> s:
                            suma[ts] += comb(math.ceil(NT[0,ts])-1,s)*math.exp(-(prices[ts]*s)/l)*math.pow(1-math.exp(-prices[ts]/l),math.ceil(NT[0,ts])-1-s)
            values = reserve_price-prices
            expected_revenues = np.multiply(values, suma)
            print expected_revenues

            if np.argmax(expected_revenues) <=  3: # and expected_revenues[0]>=0:
                return 1
            else:
                return 0
    

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

    def decision(self,N,T,t,x0,xt,l,M,s):

        index = np.array(range(N+1))
        # Construct the problem.

        #Variables

        p = Variable(T)
        y = Int(T,N+1)
        z = Variable(T,N+1)
        beta = Variable(s,T)
        w = Int(s-1,T)
        if t==0:
            sales = math.exp(-1)
        else:
            sales = (x0-xt)/t
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
        result = prob.solve(solver = GUROBI)
        prices = p.value
        return prices

    def _get_price_impl(self, t, inventory_h, price_h, price_scale, horizon, num_buyers):
        """
        TODO: Fill in your code here -- right now this skeleton code always gives an arbitrary price
        """
        T = horizon - t+1
        N = num_buyers
        x0 = inventory_h[0]
        xt = inventory_h[t]
        l = price_scale
        M = 10000
        s = 10

        p = self.decision(N,T,t,x0,xt,l,M,s)
        return p.item(0)
        



        