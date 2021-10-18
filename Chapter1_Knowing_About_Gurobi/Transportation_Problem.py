import gurobipy as gp

m = gp.Model("TP")

a_i = [350, 600]
b_j = [325, 300, 275]
c_ij = [[2.5, 1.7, 1.8], [2.5, 1.8, 1.4]]
f = 90 / 1000  # 价值系数

x = m.addVars(2, 3, vtype=gp.GRB.INTEGER, lb=0, name='x')

m.setObjective(gp.quicksum(c_ij[i][j] * f * x[i, j] for i in range(len(c_ij)) for j in range(len(c_ij[0]))),
               gp.GRB.MINIMIZE)

m.addConstrs(gp.quicksum(x[i, j] for j in range(len(c_ij[0]))) <= a_i[i] for i in range(len(c_ij)))
m.addConstrs(gp.quicksum(x[i, j] for i in range(len(c_ij))) >= b_j[j] for j in range(len(c_ij[0])))

m.optimize()
print("\n###########################\nObj:", m.objVal,'\nVar:',m.getVars())
