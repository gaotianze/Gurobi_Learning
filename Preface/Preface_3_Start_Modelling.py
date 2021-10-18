import gurobipy as gp
MODEL = gp.Model()

# ################STEP1:添加决策变量####################
#  Model.addVar() 和 Model.addVars()
x = MODEL.addVar(lb=0.0, ub=gp.GRB.INFINITY, vtype=gp.GRB.CONTINUOUS, name="x")
# lb = 0.0：变量的下界，默认为 0
# ub = GRB.INFINITY：变量的上界，默认为无穷大
# vtype = GRB.CONTINUOUS ：变量的类型，默认为连续型，可改为 GRB.BINARY 0-1变量，GRB.INTEGER 整型
# name = ""：变量名，默认为空

# 添加多个决策变量
# x = m.addVars(*indexes, lb=0, ub=gurobipy.GRB.INFINITY, vtype=gurobipy.GRB.CONTINUOUS, name="")

C = MODEL.addVars(3, 4, 5, vtype=gp.GRB.BINARY, name="C") # 创建 3*4*5 个变量，使用 x[1,2,3] 进行访问
# lb，ub，vtype 可以单独设置(同样维度数据)，也可以全部设置(单个值)
# 此外，若使用 m.addVars(iterable1,iterable2,iterable3) ，相当于笛卡尔积，参考案例 4.2
# 这种创建方法可以使用通配符命令，能简化代码

# 添加完变量后需要 m.update() 更新变量空间




# ################STEP2:添加目标函数 ####################
# Model.setObjective() 和 Model.setObjectiveN()
# (1)单目标优化
MODEL.setObjective(8 * x1 + 10 * x2 + 7 * x3 + 6 * x4 + 11 * x5 + 9 * x6, gp.GRB.MINIMIZE)
# m.setObjective(expression, sense=None)
# expression： 表达式，可以是一次或二次函数类型
# sense：求解类型，可以是GRB.MINIMIZE 或 GRB.MAXIMIZE

# (2)多目标优化(默认最小值)
# 1. 合成型 ######################################################
Obj1 = x + y          weight = 1
Obj2 = x - 5 * y      weight = -2
MODEL.setObjectiveN(x + y, index=0, weight=1, name='obj1')
MODEL.setObjectiveN(x -5 * y, index=1, weight=-2, name='obj2')
# 即转化为：(x + y) - 2 * (x - 5 * y) = - x + 11 * y

# 2. 分层优化型(目标约束时使用) #####################################
Obj1 = x + y          priority = 5
Obj2 = x - 5 * y      priority = 1
MODEL.setObjectiveN(x + y, index=0, priority=5, name='obj1')
MODEL.setObjectiveN(x -5 * y, index=1, priority=1, name='obj2')
# 即转化为：先优化 Obj1，再优化 Obj2（按照 priority 的大小关系）

# 3. 混合优化型 ##################################################
MODEL.setObjectiveN(x + y, index=0, weight=1, priority=5, name='obj1')
MODEL.setObjectiveN(x -5 * y, index=1, weight=-2, priority=1, name='obj2')
# 则 先优化 Obj1 再优化 Obj2 最后相加作为目标值

# 4. 执行最优化结束后，获取目标函数值  ###############################
MODEL.setParam(gp.GRB.Param.ObjNumber, i)   # 第 i 个目标
print(MODEL.ObjNVal)  # 打印第 i 个值

# (3) 分段目标 见网址：https://zhuanlan.zhihu.com/p/52371462




# ################STEP3:添加约束条件 ####################
# (1) 创建一个常规一次/二次/等式约束
# m.addConstr(expression, name="")
MODEL.addConstr(12 * x1 + 9 * x2 + 25 * x3 + 20 * x4 + 17 * x5 + 13 * x6 >= 60, "c0")
# expression: 布尔表达式，可以是一次或二次函数类型
# name: 约束式的名称

# (2) 创建多个常规一次/二次/等式约束
# m.addConstrs(expressions, name="")
# addConstrs 用于添加多个约束条件，参数与 addConstr 类似，最大的优势是可以将外层的 for 循环转化为内部迭代器形式
x = MODEL.addVars(20, 8, vtype=gp.GRB.BINARY)
# 写法 1
for i in range(20):
    MODEL.addConstr(x.sum(i, "*") <= 1)
# 写法 2
MODEL.addConstrs(x.sum(i, "*") <= 1 for i in range(20))

# (3) 创建一个范围约束
# m.addRange(expression, min_value, max_value, name="")
# 表达式 min_value<=expression<=max_value 的简写, 但这里的 min_value, max_value 必须是具体的实数值, 不能含有变量

# (4) 创建一个指示变量约束
# m.addGenConstrIndicator(binvar, binval, expression, name="")
# 指示变量 binvar 的值取 binval 时, 进行约束 expression

# %% 方法一
for i in range(3):
    MODEL.addGenConstrIndicator(y[i + 1], 0, x[i + 1] >= 80)
    MODEL.addGenConstrIndicator(y[i + 1], 1, x[i + 1] == 0)

# 以上代码等价于
for i in range(3):
    MODEL.addConstr(x[i + 1] >= 80 * y[i + 1])
    MODEL.addConstr(x[i + 1] <= 1000 * y[i + 1])




# ################STEP4:执行最优化 ####################
# Model.optimize()

MODEL.Params.LogToConsole=True # 显示求解过程
MODEL.Params.MIPGap=0.0001 # 百分比界差
MODEL.Params.TimeLimit=100 # 限制求解时间为 100s

MODEL.optimize()
# 查看模型结果
# (1) 模型是否取得最优解
#
# m.status == gurobipy.GRB.Status.OPTIMAL
#
# True 最优
# False 非最优, 在TimeLimit模式下, 不能用这个方法判断最优解
# (2) 单目标优化 —— 查看目标函数值
#
# # 查看单目标规划模型的目标函数值
# print("Optimal Objective Value", m.objVal)
# (3) 多目标优化 —— 查看目标函数值
#
# # 查看多目标规划模型的目标函数值
# for i in range(m.NumObj):
# 	m.setParam(gurobipy.GRB.Param.ObjNumber, i)
# 	print(f"Obj {i+1} = {m.ObjNVal}")
# (4) 查看变量取值
#
# # 查看变量取值，这个方法用的很少，请看第 4 部分案例
# for var in m.getVars():
#    print(f"{var.varName}: {round(var.X, 3)}")
# (5) LP 问题灵敏度分析
#
# 通过 m.getVars() 得到的变量 var
#
# 使用 var.X 可以获取变量值, var.RC 可以获取 Reduced Cost；
# var.Obj 可以得到在目标函数中的系数
# var.SAObjLow 可以得到 Allowable Minimize
# var.SAObjUp 可以得到 Allowable Maximize
# 通过 m.getConstrs() 得到的约束式 Constr
#
# Constr.Slack 可以得到 Slack or Surplus
# Constr.pi 可以得到 Dual Price
# Constr.RHS 可以得到约束式右侧常值
# Constr.SARHSLow 可以得到 Allowable Minimize
# Constr.SARHSUp 可以得到 Allowable Maximize
