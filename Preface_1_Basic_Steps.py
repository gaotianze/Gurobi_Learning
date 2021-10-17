# 可参考的教程：
# https://zhuanlan.zhihu.com/p/52371462
# https://github.com/wurmen/Gurobi-Python

# 在利用 Python+Gurobi 建立数学规划模型时，通常会按照设置变量、更新变量空间、设置目标函数、设置约束条件、执行最优化的顺序进行。
import gurobipy

# 创建模型
MODEL = gurobipy.Model()

# 创建变量
X = MODEL.addVar(vtype=gurobipy.GRB.INTEGER,name="X")

# 更新变量环境
MODEL.update()

# 创建目标函数
MODEL.setObjective('目标函数表达式', gurobipy.GRB.MINIMIZE)

# 创建约束条件
MODEL.addConstr('约束表达式，逻辑运算')

# 执行线性规划模型
MODEL.optimize()

# 输出模型结果
print("Obj:", MODEL.objVal)
for x in X:
    print(f"{x.varName}：{round(x.X,3)}")