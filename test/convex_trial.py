from cvxpy import *
import numpy as np
import math
import numpy as np
import numpy.random as rn
import gurobipy

# Problem data.
N = 10
T = 30
x0 = 10.
xt = 8
l = 4
M = 100000
s = 10 #number of splines

index = np.array(range(N+1))
# Construct the problem.

#Variables

p = Variable(T)
y = Int(T,N+1)
z = Variable(T,N+1)
beta = Variable(s,T)
sales = (x0-xt)/T
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
result = prob.solve(solver = GUROBI)
