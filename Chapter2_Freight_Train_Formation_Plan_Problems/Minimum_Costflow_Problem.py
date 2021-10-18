# 参考文档： http://www.360doc.com/content/21/0212/15/13328254_961769070.shtml Python+Gurobi求解最大流问题
import gurobipy as gp
from gurobipy import GRB

# Input the information of the network

# 添加了虚拟供应节点与虚拟需求节点
dict_capacity = {(0, 1): 99999,
                 (1, 2): 70, (1, 3): 100, (1, 4): 90,
                 (2, 6): 80,
                 (3, 4): 40, (3, 5): 70,
                 (4, 5): 40, (4, 6): 100,
                 (5, 6): 90,
                 (6, 7): 99999
                 }

arc, capacity = gp.multidict(dict_capacity)

# Construct the model
m = gp.Model("MCP")

# Decision variables
X = m.addVars(arc, name='X')

# Add constraints
for i, j in arc:
    # The volume of flow cannot exceed the capacity of the arc
    m.addConstr(X[i, j] <= capacity[i, j])
    if i == 0 or j == 7:
        continue
    else:
        # Flow balance constraint
        m.addConstr(X.sum(i, '*') == X.sum('*', i))

# Define the objective function
m.setObjective(X.sum(1, '*'), sense=GRB.MAXIMIZE)

# Solve the model
m.optimize()

# Output the results
print('*' * 60)
print("The objective value is：", m.objVal)
print('The flow in each arc is:')
for i, j in arc:
    print("Node %d --&gt; Node %d: %d" % (i, j, X[i, j].x))