import gurobipy as gp

m = gp.Model()

x1 = m.addVar(lb=0)
x2 = m.addVar(lb=0)

m.update()

m.setObjective(-3 * x1 - 2 * x2, gp.GRB.MINIMIZE)

m.addConstr(x1 + x2 <= 40)
m.addConstr(2 * x1 + x2 <= 60)

m.optimize()
print("Obj:", m.objVal)
