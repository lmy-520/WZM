# 1. 导入 PuLP 库
import pulp

# 2. 创建线性规划问题实例
# LpProblem(问题名, 优化方向)：LpMaximize（最大化）/ LpMinimize（最小化）
problem = pulp.LpProblem("ResourceAllocationProblem", pulp.LpMaximize)

# 3. 定义决策变量
# LpVariable(变量名, 下界, 上界, 变量类型)
# 变量类型：LpInteger（整数）/ LpContinuous（连续，默认）/ LpBinary（0-1）
x_a = pulp.LpVariable("ProductA", lowBound=0, cat=pulp.LpInteger)  # 产品A的生产数量（非负整数）
x_b = pulp.LpVariable("ProductB", lowBound=0, cat=pulp.LpInteger)  # 产品B的生产数量（非负整数）

# 4. 设定目标函数（最大化总利润）
# 利润 = 5*A + 7*B，直接用 += 把目标函数加入问题
problem += 5 * x_a + 7 * x_b, "TotalProfit"

# 5. 添加约束条件
# 资源X约束：2*A + 3*B ≤ 100
problem += 2 * x_a + 3 * x_b <= 100, "ResourceXLimit"

# 6. 求解问题
# solve() 方法执行求解，返回求解状态（1 表示求解成功）
status = problem.solve()
# 打印求解状态（可选，验证是否成功）
print("求解状态：", pulp.LpStatus[status])  # 输出 "Optimal" 表示找到最优解

# 7. 提取并输出结果
print("=== 最优解 ===")
print(f"产品A生产数量：{pulp.value(x_a)}")
print(f"产品B生产数量：{pulp.value(x_b)}")
print(f"最大总利润：{pulp.value(problem.objective)} 元")

# 8. 导出结果到 solution.csv（对应你的任务要求）
import csv
with open("solution.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["产品", "生产数量", "单位利润", "贡献利润"])
    writer.writerow(["ProductA", pulp.value(x_a), 5, 5*pulp.value(x_a)])
    writer.writerow(["ProductB", pulp.value(x_b), 7, 7*pulp.value(x_b)])
    writer.writerow(["总计", "-", "-", pulp.value(problem.objective)])