import gurobipy as gp
from gurobipy import GRB

# Base data
commodities = [1, 2]
dict = {
    (1, 1, 2): [1, 300], (1, 1, 3): [2, 300],
    (1, 2, 3): [1, 500], (1, 2, 4): [2, 400], (1, 2, 5): [2, 300],
    (1, 3, 4): [1, 100], (1, 3, 5): [2, 200],
    (1, 4, 6): [5, 500],
    (1, 5, 4): [3, 300], (1, 5, 6): [1, 100],

    (2, 1, 2): [1, 300], (2, 1, 3): [2, 300],
    (2, 2, 3): [1, 500], (2, 2, 4): [2, 400], (2, 2, 5): [2, 300],
    (2, 3, 4): [1, 100], (2, 3, 5): [2, 200],
    (2, 4, 6): [5, 500],
    (2, 5, 4): [3, 300], (2, 5, 6): [1, 100]
}

arcs, capacity, cost = gp.multidict(dict)

# Create optimization model
m = gp.Model('MCP')

# Create variables
x = m.addVars(arcs, vtype=GRB.INTEGER, name="x")

for k, i, j in arcs:
    # 最大流量约束
    m.addConstr(x[k, i, j] <= capacity[k, i, j])
    if i == 1 or j == 6:
        continue
    else:
        # 流平衡约束
        m.addConstr(x.sum('*', i, '*') == x.sum("*", '*', i))

m.addConstrs(
    gp.quicksum(x[k, 1, j] for j in range(2, 7) if (k, 1, j) in arcs.select(k, 1, "*")) == 3 for k in commodities)
m.addConstrs(
    gp.quicksum(x[k, i, 6] for i in range(1, 6) if (k, i, 6) in arcs.select(k, '*', 6)) == 3 for k in commodities)

m.setObjective(gp.quicksum(cost[k, i, j] * x[k, i, j] for (k, i, j) in arcs), GRB.MINIMIZE)

# Compute optimal solution
m.optimize()

# Print solution
if m.status == GRB.OPTIMAL:
    solution = m.getAttr('x', x)
    for h in commodities:
        print('\nOptimal flows for %s:' % h)
        for h, i, j in arcs:
            if solution[h, i, j] > 0:
                print('%s -> %s: %g' % (i, j, solution[h, i, j]))
