import gurobipy as gp

m = gp.Model("MCP")

c_uv = [[0, 1, 2, 0, 0],
        [0, 0, 1, 2, 2],
        [0, 0, 0, 1, 2],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 3, 0],
        [0, 0, 0, 0, 0]]

w_uv = [[9999, 300, 300, 9999, 9999],
        [9999, 9999, 500, 400, 300],
        [9999, 9999, 9999, 100, 200],
        [9999, 9999, 9999, 9999, 9999],
        [9999, 9999, 9999, 300, 9999],
        [9999, 9999, 9999, 9999, 9999]]

x = m.addVars(16, 16, vtype=gp.GRB.BINARY, name='x')

m.setObjective(gp.quicksum(C_ij[i][j] * x[i, j] for i in range(16) for j in range(16)),
               gp.GRB.MINIMIZE)

m.addConstrs(
    (gp.quicksum(x[i, j] - x[j, i] for j in range(16)) == 1) for i in range(1))
m.addConstrs(
    (gp.quicksum(x[i, j] - x[j, i] for j in range(16)) == -1) for i in range(15, 16))
m.addConstrs(
    (gp.quicksum(x[i, j] - x[j, i] for j in range(16)) == 0) for i in range(1, 15))
m.optimize()
print("\n###########################\nObj:", m.objVal)
