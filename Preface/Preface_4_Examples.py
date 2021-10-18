import gurobipy as gp

# 一般线性规划问题
c = [8, 10, 7, 6, 11, 9]
p = [[12, 9, 25, 20, 17, 13],
     [35, 42, 18, 31, 56, 49],
     [37, 53, 28, 24, 29, 20]]
r = [60, 150, 125]
MODEL = gp.Model("Example")

# 创建变量
x = MODEL.addVars(6, lb=0, ub=1, name='x')

# 更新变量环境
MODEL.update()

# 创建目标函数
MODEL.setObjective(x.prod(c), gp.GRB.MINIMIZE)

# 创建约束条件
MODEL.addConstrs(x.prod(p[i]) >= r[i] for i in range(3))

# 执行线性规划模型
MODEL.optimize()
print("Obj:", MODEL.objVal)

for v in MODEL.getVars():
    print(f"{v.varName}：{round(v.x, 3)}")
