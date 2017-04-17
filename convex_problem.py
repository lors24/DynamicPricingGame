from cvxpy import *
import numpy as np

# Problem data.
N = 5
T = 10
x0 = 4
l = 3

# Construct the problem.
p = Variable(T)
y = Variable(T)

objective = Maximize(Minimize(-y.T*p))
constraints = [y >= 0, p >= 0, sum(y)<= x0, y <= 1 - l*p] 
#The optimal objective is returned by prob.solve().
prob = Problem(objective, constraints)
result = prob.solve()
# The optimal value for x is stored in x.value.
print p.value
# The optimal Lagrange multiplier for a constraint
# is stored in constraint.dual_value.
#print constraints[0].dual_value