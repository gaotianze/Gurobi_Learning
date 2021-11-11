# From Gurobi Tutorial P142 - Cutting Stock Problem
# Column Generation Tutorial - https://www.cnblogs.com/dengfaheng/p/11249879.html

import gurobipy
from gurobipy import *

TypesDemand = [3, 7, 9, 16]
QuantityDemand = [25, 30, 14, 8]
LengthUsable = 20

MainProbRelax = Model()
SubProb = Model()

# 构建主问题模型，选择的初始切割方案每根钢管只切一种长度
# 添加变量、目标函数
# 添加了4个变量(分别代表4种方案)： z1 z2 z3 z4
Zp = MainProbRelax.addVars(len(TypesDemand), obj=1.0, vtype=GRB.CONTINUOUS, name='z')  # 先将主问题松弛成连续，并创建包含4初始方案的基变量


# 添加约束
# 拿四个初始方案做约束添加进去
# 6*z_1 >= 25; 2*z_2>=30; 2*z_3>=14; 1*z_4>=8;
ColumnIndex = MainProbRelax.addConstrs(
    quicksum(Zp[p] * (LengthUsable // TypesDemand[i]) for p in range(len(TypesDemand)) if p == i) >= QuantityDemand[i]
    for i in range(len(TypesDemand)))
MainProbRelax.optimize()

# 构造子问题模型
# 获得对偶值
# lambda_list=MainProbRelax.getAttr(GRB.Attr.Pi, MainProbRelax.getConstrs())
Dualsolution = MainProbRelax.getAttr(GRB.Attr.Pi, MainProbRelax.getConstrs())
# 添加变量
# 目标函数此时为： max(0.166*c_1 + 0.5*c_2 + 0.5*c_3 + c_4)
Ci = SubProb.addVars(len(TypesDemand), obj=Dualsolution, vtype=GRB.INTEGER, name='c')
# 添加约束
# 3c1+7c2+9c3+16c4 <= 20 单根卷钢长度约束
SubProb.addConstr(quicksum(Ci[i] * TypesDemand[i] for i in range(len(TypesDemand))) <= LengthUsable)
SubProb.setAttr(GRB.Attr.ModelSense, -1) # -1为maximize
SubProb.optimize()

# 判断Reduced Cost是否小于0
while SubProb.objval > 1:
    # 获取变量取值
    columnCoeff = SubProb.getAttr("X", SubProb.getVars())
    column = Column(columnCoeff, MainProbRelax.getConstrs())
    # 读取到新方案 [2,2,0,0]^T ，作为新的一列添加到RMP中
    # 添加变量
    MainProbRelax.addVar(obj=1.0, vtype=GRB.CONTINUOUS, name='CG', column=column)
    MainProbRelax.optimize()
    # 修改目标函数系数
    for i in range(len(TypesDemand)):
        Ci[i].obj = ColumnIndex[i].pi
    SubProb.optimize()

# 将CG后的模型转为整数，并求
for v in MainProbRelax.getVars():
    v.setAttr("VType", GRB.INTEGER)
MainProbRelax.optimize()
print("\nSolotion：")
for v in MainProbRelax.getVars():
    if v.X != 0.0:
        print('%s %g次' % (v.VarName, v.X))
