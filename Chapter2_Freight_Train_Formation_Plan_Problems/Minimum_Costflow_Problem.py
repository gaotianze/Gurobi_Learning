import gurobipy as gp
from gurobipy import GRB

dict_capacity_cost = {
    (1, 2): [1, 300], (1, 3): [2, 300],
    (2, 3): [1, 500], (2, 4): [2, 400], (2, 5): [2, 300],
    (3, 4): [1, 100], (3, 5): [2, 200],
    (4, 6): [5, 500],
    (5, 4): [3, 300], (5, 6): [1, 100]
}

arc, capacity, cost = gp.multidict(dict_capacity_cost)

# Construct the model
m = gp.Model("MCP")

# Decision variables
X = m.addVars(arc, vtype=GRB.INTEGER, name='X')

# Add constraints
for i, j in arc:
    # 最大流量约束
    m.addConstr(X[i, j] <= capacity[i, j])
    if i == 1 or j == 6:
        continue
    else:
        # 流平衡约束
        m.addConstr(X.sum(i, '*') == X.sum('*', i))

# m.addConstr(gp.quicksum(X[1, j] for (i, j) in arc.select(1, "*")) == 3)
m.addConstr(gp.quicksum(X[1, j] for j in range(2,7) if (1,j) in arc.select(1, "*")) == 3)
m.addConstr(gp.quicksum(X[i, 6] for i in range(1,6) if (i, 6) in arc.select('*', 6)) == 3)

# Define the objective function
m.setObjective(gp.quicksum(X[i, j] * cost[i, j] for (i, j) in arc), GRB.MINIMIZE)

# Solve the model
m.optimize()

# Output the results
print('\n', '*' * 60)
print("The objective value is：", m.objVal)
print('The x in each arc is:')
for i, j in arc:
    print("Node %d --&gt; Node %d: %d" % (i, j, X[i, j].x))
