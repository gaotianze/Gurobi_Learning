# 可参考的教程：
# https://zhuanlan.zhihu.com/p/52371462

# 在利用 Python+Gurobi 建立数学规划模型时，这几个辅助函数能简化模型构建过程。
import gurobipy

# ①列表推导式/列表解析式
# -- if 在后 —— 过滤元素
#
# [expression for exp1 in sequence1 if condition1
#             for exp2 in sequence2 if condition2
#             ...
#             for exp2 in sequence2 if conditionn]
# 符合 condition 条件的值会被储存在列表中，不符合的不保存 (类似于 pass 和 filter 函数)

evens = [i for i in range(10) if i % 2 == 0]
print(evens)

# -- if 在前 —— 分段映射
#
# [expression1 if condition1 else expression2 for exp1 in sequence1
#                                             for exp2 in sequence2
#                                             ...
#                                             for exp2 in sequence2]

evens2 = [i if i % 2 == 0 else i + 1 for i in range(10)]
print(evens2)

# ②quicksum()
MODEL = gurobipy.Model()
for i in I:
    MODEL.addConstr(quicksum(x[i, j] for j in J) <= 5)

# ③multidict()
# 扩展字典，便于处理同一个对象的不同属性约束。
EMPLOYEE, MIN, MAX, COST, START, END = gurobipy.multidict({
    "SMITH": [6, 8, 30, 6, 20], "JOHNSON": [6, 8, 50, 0, 24], 'WILLIAMS': [6, 8, 30, 0, 24],
    'JONES': [6, 8, 30, 0, 24], 'BROWN': [6, 8, 40, 0, 24], 'DAVIS': [6, 8, 50, 0, 24],
    'MILLER': [6, 8, 45, 6, 18], 'WILSON': [6, 8, 30, 0, 24], 'MOORE': [6, 8, 35, 0, 24],
    'TAYLOR': [6, 8, 40, 0, 24], 'ANDERSON': [2, 3, 60, 0, 6], 'THOMAS': [2, 4, 40, 0, 24],
    'JACKSON': [2, 4, 60, 8, 16], 'WHITE': [2, 6, 55, 0, 24], 'HARRIS': [2, 6, 45, 0, 24],
    'MARTIN': [2, 3, 40, 0, 24], 'THOMPSON': [2, 5, 50, 12, 24], 'GARCIA': [2, 4, 50, 0, 24],
    'MARTINEZ': [2, 4, 40, 0, 24], 'ROBINSON': [2, 5, 50, 0, 24]})

# EMPLOYEE 变成了list，而 MIN、MAX 等等则变成了字典
# EMPLOYEE = [“SMITH”, "JOHNSON",...]
# MIN = {“SMITH”: 6, "JOHNSON": 6,...}

# ④tuplelist()
# 扩展列表元组，可以使用通配符筛选变量组。若使用 tuplelist 创建变量：

Cities= [('A','B'), ('A','C'), ('B','C'),('B','D'),('C','D')]
Routes = gurobipy.tuplelist(Cities)

Routes.select('A','*') # 选出所有第一个元素为 "A" 的元组

# 此外, 对于addVars创建的变量, x.select("*", i, j) 也可以进行筛选(详见案例3.6)
# 可以将 '*' 理解为切片操作(列表的 list[:])


# ⑤prod() 和 sum() 下标聚合
gurobipy.quicksum(cost[i,j] * x[i,j] for i,j in arcs)
# 等价于 x.prod(cost)
# 效果为对应元素相乘再相加