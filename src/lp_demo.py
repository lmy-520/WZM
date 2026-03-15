"""
最小 LP Demo - 可复现版本
目标：最小化 x + y
约束：x + 2y >= 10，x, y >= 0
输出：
  - outputs/tables/solution.csv （决策变量与最优值）
  - outputs/tables/metrics.csv （目标值、约束统计、运行时间）
  - outputs/tables/constraints.csv （约束满足情况）
  - outputs/figures/fig_solution.png （可视化结果）
"""

# 导入日志模块，用于记录运行过程。
import logging
# 导入系统模块，用于修改模块搜索路径。
import sys
# 导入时间模块，用于统计求解耗时。
import time
# 导入操作系统模块，用于路径拼接和文件名处理。
import os

# 导入 pandas，用于保存表格结果。
import pandas as pd
# 导入 numpy，用于数值计算和绘图采样。
import numpy as np
# 导入 matplotlib.pyplot，用于绘图。
import matplotlib.pyplot as plt
# 导入 pulp，用于构建并求解线性规划。
import pulp

# 将当前脚本所在目录加入模块搜索路径，确保可导入同目录下的 config。
sys.path.insert(0, os.path.dirname(__file__))

# 从配置文件导入运行参数与输出路径。
from config import (
    SEED,
    OUTPUT_DIR,
    SOLUTION_PATH,
    METRICS_PATH,
    CONSTRAINT_PATH,
    FIGURE_PREFIX,
    SOLVER_MSG,
    get_figure_path,
)

# 固定随机种子，保证可复现性（虽然本例基本不依赖随机性）。
np.random.seed(SEED)

# 构建日志文件路径。
log_path = os.path.join(OUTPUT_DIR, "lp_demo.log")
# 配置日志：同时输出到文件与控制台。
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(log_path, encoding="utf-8"),
        logging.StreamHandler(),
    ],
)
# 获取当前模块的日志记录器。
logger = logging.getLogger(__name__)

# 输出开始分隔线。
logger.info("=" * 70)
# 输出任务标题。
logger.info("最小 LP Demo - 可复现版本")
# 输出关键配置。
logger.info(f"配置：SEED={SEED}")
# 输出结束分隔线。
logger.info("=" * 70)

# 记录开始阶段：构建模型。
logger.info("\n[1/5] 构建 LP 模型...")
# 记录起始时间，用于统计总耗时。
start_time = time.time()

# 创建线性规划问题，名称为 min_x_plus_y，目标为最小化。
prob = pulp.LpProblem("min_x_plus_y", pulp.LpMinimize)
# 创建变量 x，设置下界为 0。
x = pulp.LpVariable("x", lowBound=0)
# 创建变量 y，设置下界为 0。
y = pulp.LpVariable("y", lowBound=0)

# 添加目标函数：min x + y。
prob += x + y, "Objective"
# 添加约束：x + 2y >= 10。
prob += x + 2 * y >= 10, "constraint_1"

# 输出模型构建完成提示。
logger.info("✓ 模型构建完成")
# 输出变量约束说明。
logger.info("  决策变量：x, y ≥ 0")
# 输出目标函数说明。
logger.info("  目标函数：min(x + y)")
# 输出约束说明。
logger.info("  约束：x + 2y ≥ 10")

# 记录开始阶段：求解模型。
logger.info("\n[2/5] 求解模型...")
# 调用 CBC 求解器并求解，显式转 bool 避免类型检查误报。
status = prob.solve(pulp.PULP_CBC_CMD(msg=bool(SOLVER_MSG)))
# 计算耗时。
elapsed = time.time() - start_time

# 输出求解状态。
logger.info(f"✓ 求解完成，状态：{pulp.LpStatus[status]}")
# 输出运行时间。
logger.info(f"  运行时间：{elapsed:.4f}s")

# 从求解结果读取 x 的值（可能为 None）。
x_raw = pulp.value(x)
# 从求解结果读取 y 的值（可能为 None）。
y_raw = pulp.value(y)
# 从求解结果读取目标值（可能为 None）。
obj_raw = pulp.value(prob.objective)

# 判断是否为最优状态。
is_optimal = status == pulp.LpStatusOptimal
# 判断结果数值是否都已返回。
has_values = (x_raw is not None) and (y_raw is not None) and (obj_raw is not None)
# 综合判断可行性（本例用“最优且有值”作为可行判定）。
is_feasible = bool(is_optimal and has_values)

# 若可行则转为 float，否则写入 NaN 以避免后续运算报错。
x_val = float(x_raw) if x_raw is not None else float("nan")
# 若可行则转为 float，否则写入 NaN。
y_val = float(y_raw) if y_raw is not None else float("nan")
# 若可行则转为 float，否则写入 NaN。
obj_val = float(obj_raw) if obj_raw is not None else float("nan")

# 记录开始阶段：可行性检查。
logger.info("\n[3/5] 可行性检查...")
# 输出可行性描述。
logger.info(f"✓ 问题状态：{'可行' if is_feasible else '不可行'}")
# 输出目标值（若不可行可能为 nan）。
logger.info(f"  目标值：{obj_val:.6f}")
# 输出 x 值。
logger.info(f"  x = {x_val:.6f}")
# 输出 y 值。
logger.info(f"  y = {y_val:.6f}")

# 记录开始阶段：约束满足检查。
logger.info("\n[4/5] 约束满足检查...")
# 用列表保存每条约束的检查结果，后续写入 CSV。
constraints_info = []

# 仅在可行时进行数值化约束检查。
if is_feasible:
    # 计算约束 1 左侧值：x + 2y。
    lhs_1 = x_val + 2 * y_val
    # 判断约束 1 是否满足（加入微小容差）。
    satisfied_1 = lhs_1 >= 10 - 1e-6
    # 计算约束 1 违反量。
    violation_1 = max(0.0, 10 - lhs_1)

    # 判断 x 非负约束是否满足。
    satisfied_x = x_val >= -1e-6
    # 判断 y 非负约束是否满足。
    satisfied_y = y_val >= -1e-6
    # 计算 x 非负约束违反量。
    violated_x = max(0.0, -x_val)
    # 计算 y 非负约束违反量。
    violated_y = max(0.0, -y_val)
else:
    # 不可行时左侧值设为 NaN。
    lhs_1 = float("nan")
    # 不可行时约束 1 视为不满足。
    satisfied_1 = False
    # 不可行时违反量记为 NaN。
    violation_1 = float("nan")

    # 不可行时 x 非负约束视为不满足。
    satisfied_x = False
    # 不可行时 y 非负约束视为不满足。
    satisfied_y = False
    # 不可行时违反量记为 NaN。
    violated_x = float("nan")
    # 不可行时违反量记为 NaN。
    violated_y = float("nan")

# 输出约束 1 标题。
logger.info("  约束 1 (x + 2y ≥ 10):")
# 输出约束 1 左侧值。
logger.info(f"    左侧值：{lhs_1:.6f}")
# 输出约束 1 是否满足。
logger.info(f"    满足：{'是' if satisfied_1 else '否'}")
# 输出约束 1 违反量。
logger.info(f"    违反量：{violation_1:.6f}")

# 将约束 1 检查结果加入列表。
constraints_info.append(
    {
        "constraint": "x + 2y ≥ 10",
        "lhs_value": lhs_1,
        "rhs_value": 10,
        "satisfied": satisfied_1,
        "violation": violation_1,
    }
)

# 输出约束 2（x >= 0）检查结果。
logger.info(
    f"  约束 2 (x ≥ 0): 值：{x_val:.6f}，满足：{'是' if satisfied_x else '否'}，违反量：{violated_x:.6f}"
)
# 输出约束 3（y >= 0）检查结果。
logger.info(
    f"  约束 3 (y ≥ 0): 值：{y_val:.6f}，满足：{'是' if satisfied_y else '否'}，违反量：{violated_y:.6f}"
)

# 将约束 2 结果加入列表。
constraints_info.append(
    {
        "constraint": "x ≥ 0",
        "lhs_value": x_val,
        "rhs_value": 0,
        "satisfied": satisfied_x,
        "violation": violated_x,
    }
)
# 将约束 3 结果加入列表。
constraints_info.append(
    {
        "constraint": "y ≥ 0",
        "lhs_value": y_val,
        "rhs_value": 0,
        "satisfied": satisfied_y,
        "violation": violated_y,
    }
)

# 计算总违反量（不可行时记为 NaN）。
total_violation = (
    violation_1 + violated_x + violated_y
    if is_feasible
    else float("nan")
)
# 输出总违反量。
logger.info(f"  总违反量：{total_violation:.6f}")

# 记录开始阶段：保存结果。
logger.info("\n[5/5] 保存结果...")

# 构建解向量表：变量与目标值。
solution_df = pd.DataFrame(
    {
        "variable": ["x", "y", "objective"],
        "value": [x_val, y_val, obj_val],
    }
)
# 保存解向量表到 CSV。
solution_df.to_csv(SOLUTION_PATH, index=False, encoding="utf-8-sig")
# 输出保存提示。
logger.info(f"✓ 决策变量已保存：{os.path.basename(SOLUTION_PATH)}")

# 构建性能指标表。
metrics_df = pd.DataFrame(
    {
        "metric": [
            "objective_value",
            "solve_time_sec",
            "feasibility",
            "total_constraint_violation",
        ],
        "value": [obj_val, elapsed, int(is_feasible), total_violation],
    }
)
# 保存性能指标表到 CSV。
metrics_df.to_csv(METRICS_PATH, index=False, encoding="utf-8-sig")
# 输出保存提示。
logger.info(f"✓ 性能指标已保存：{os.path.basename(METRICS_PATH)}")

# 将约束检查列表转为 DataFrame。
constraints_df = pd.DataFrame(constraints_info)
# 保存约束检查表到 CSV。
constraints_df.to_csv(CONSTRAINT_PATH, index=False, encoding="utf-8-sig")
# 输出保存提示。
logger.info(f"✓ 约束检查已保存：{os.path.basename(CONSTRAINT_PATH)}")

# 尝试绘图并保存。
try:
    # 创建 1 行 2 列子图画布。
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # 生成绘图用 x 轴采样点。
    x_range = np.linspace(0, 15, 200)
    # 依据边界方程 x + 2y = 10 计算 y。
    y_line = (10 - x_range) / 2

    # 左图：可行域与最优解。
    ax_left = axes[0]
    # 填充可行域（示意）。
    ax_left.fill_between(
        x_range,
        y_line,
        15,
        where=(y_line <= 15),
        alpha=0.3,
        color="blue",
        label="Feasible Region",
    )
    # 绘制边界直线。
    ax_left.plot(x_range, y_line, "b-", linewidth=2, label="x + 2y = 10")
    # 仅当可行时绘制最优点。
    if is_feasible:
        # 绘制最优解红色星形标记。
        ax_left.plot(x_val, y_val, "r*", markersize=20, label=f"Optimal: ({x_val:.2f}, {y_val:.2f})")

    # 设置左图坐标范围。
    ax_left.set_xlim(-0.5, 15)
    # 设置左图坐标范围。
    ax_left.set_ylim(-0.5, 8)
    # 设置左图 x 轴名称。
    ax_left.set_xlabel("x")
    # 设置左图 y 轴名称。
    ax_left.set_ylabel("y")
    # 设置左图标题。
    ax_left.set_title("LP 问题可行域与最优解")
    # 显示左图图例。
    ax_left.legend()
    # 显示左图网格。
    ax_left.grid(True, alpha=0.3)

    # 右图：目标函数等高线。
    ax_right = axes[1]
    # 构造 x 网格点。
    x_grid = np.linspace(-1, 15, 100)
    # 构造 y 网格点。
    y_grid = np.linspace(-1, 15, 100)
    # 生成二维网格。
    X, Y = np.meshgrid(x_grid, y_grid)
    # 计算目标函数值 Z = X + Y。
    Z = X + Y

    # 绘制等高线。
    contour = ax_right.contour(X, Y, Z, levels=20, alpha=0.6)
    # 给等高线加标签。
    ax_right.clabel(contour, inline=True, fontsize=8)
    # 叠加可行域示意。
    ax_right.fill_between(x_range, y_line, 15, where=(y_line <= 15), alpha=0.2, color="blue")
    # 叠加边界线。
    ax_right.plot(x_range, y_line, "b-", linewidth=2)
    # 仅当可行时绘制最优点。
    if is_feasible:
        # 绘制最优解标记。
        ax_right.plot(x_val, y_val, "r*", markersize=20, label="最优解")

    # 设置右图坐标范围。
    ax_right.set_xlim(-1, 15)
    # 设置右图坐标范围。
    ax_right.set_ylim(-1, 15)
    # 设置右图 x 轴名称。
    ax_right.set_xlabel("x")
    # 设置右图 y 轴名称。
    ax_right.set_ylabel("y")
    # 设置右图标题。
    ax_right.set_title("目标函数等高线")
    # 显示右图图例。
    ax_right.legend()
    # 显示右图网格。
    ax_right.grid(True, alpha=0.3)

    # 自动调整布局，防止文字重叠。
    plt.tight_layout()
    # 获取图像输出路径。
    fig_path = get_figure_path("solution")
    # 保存图像文件。
    plt.savefig(fig_path, dpi=150, bbox_inches="tight")
    # 关闭图像释放内存。
    plt.close()
    # 输出保存提示。
    logger.info(f"✓ 图表已保存：{os.path.basename(fig_path)}")
except Exception as e:
    # 若绘图失败，记录警告但不中断主流程。
    logger.warning(f"⚠ 图表生成失败：{e}")

# 输出结束分隔线。
logger.info("\n" + "=" * 70)
# 输出完成提示。
logger.info("任务完成！")
# 输出结束分隔线。
logger.info("=" * 70)
