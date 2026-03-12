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

import logging
import sys
import time
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pulp

# ── 导入配置 ──────────────────────────────────────────────────────────────────
sys.path.insert(0, os.path.dirname(__file__))
from config import (
    SEED, OUTPUT_DIR, SOLUTION_PATH, METRICS_PATH, CONSTRAINT_PATH,
    FIGURE_PREFIX, SOLVER_MSG, get_figure_path
)

# ── 固定随机种子 ──────────────────────────────────────────────────────────────
np.random.seed(SEED)

# ── 日志配置 ──────────────────────────────────────────────────────────────────
log_path = os.path.join(OUTPUT_DIR, "lp_demo.log")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(log_path, encoding="utf-8"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)

logger.info("="*70)
logger.info("最小 LP Demo - 可复现版本")
logger.info(f"配置：SEED={SEED}")
logger.info("="*70)

# ── 构建模型 ──────────────────────────────────────────────────────────────────
logger.info("\n[1/5] 构建 LP 模型...")
start_time = time.time()

prob = pulp.LpProblem("min_x_plus_y", pulp.LpMinimize)
x = pulp.LpVariable("x", lowBound=0)
y = pulp.LpVariable("y", lowBound=0)

# 目标函数
prob += x + y, "Objective"

# 约束
prob += x + 2 * y >= 10, "constraint_1"

logger.info("✓ 模型构建完成")
logger.info("  决策变量：x, y ≥ 0")
logger.info("  目标函数：min(x + y)")
logger.info("  约束：x + 2y ≥ 10")

# ── 求解 ──────────────────────────────────────────────────────────────────────
logger.info("\n[2/5] 求解模型...")
status = prob.solve(pulp.PULP_CBC_CMD(msg=SOLVER_MSG))
elapsed = time.time() - start_time

logger.info(f"✓ 求解完成，状态：{pulp.LpStatus[status]}")
logger.info(f"  运行时间：{elapsed:.4f}s")

# ── 检查可行性 ────────────────────────────────────────────────────────────────
x_val = pulp.value(x)
y_val = pulp.value(y)
obj_val = pulp.value(prob.objective)
is_feasible = (status == 1)  # 1 = Optimal

logger.info("\n[3/5] 可行性检查...")
logger.info(f"✓ 问题状态：{'可行' if is_feasible else '不可行'}")
logger.info(f"  目标值：{obj_val:.6f}")
logger.info(f"  x = {x_val:.6f}")
logger.info(f"  y = {y_val:.6f}")

# ── 详细约束检查 ──────────────────────────────────────────────────────────────
logger.info("\n[4/5] 约束满足检查...")
constraints_info = []

# 约束1：x + 2y >= 10
lhs_1 = x_val + 2 * y_val
satisfied_1 = lhs_1 >= 10 - 1e-6
violation_1 = max(0, 10 - lhs_1)

logger.info(f"  约束 1 (x + 2y ≥ 10):")
logger.info(f"    左侧值：{lhs_1:.6f}")
logger.info(f"    满足：{'是' if satisfied_1 else '否'}")
logger.info(f"    违反量：{violation_1:.6f}")

constraints_info.append({
    "constraint": "x + 2y ≥ 10",
    "lhs_value": lhs_1,
    "rhs_value": 10,
    "satisfied": satisfied_1,
    "violation": violation_1
})

# 非负性约束
satisfied_x = x_val >= -1e-6
satisfied_y = y_val >= -1e-6
violated_x = max(0, -x_val)
violated_y = max(0, -y_val)

logger.info(f"  约束 2 (x ≥ 0):")
logger.info(f"    值：{x_val:.6f}，满足：{'是' if satisfied_x else '否'}，违反量：{violated_x:.6f}")

logger.info(f"  约束 3 (y ≥ 0):")
logger.info(f"    值：{y_val:.6f}，满足：{'是' if satisfied_y else '否'}，违反量：{violated_y:.6f}")

constraints_info.append({"constraint": "x ≥ 0", "lhs_value": x_val, "rhs_value": 0, "satisfied": satisfied_x, "violation": violated_x})
constraints_info.append({"constraint": "y ≥ 0", "lhs_value": y_val, "rhs_value": 0, "satisfied": satisfied_y, "violation": violated_y})

total_violation = violation_1 + violated_x + violated_y
logger.info(f"  总违反量：{total_violation:.6f}")

# ── 保存结果 ──────────────────────────────────────────────────────────────────
logger.info("\n[5/5] 保存结果...")

# 1. 决策变量与最优值 (solution.csv)
solution_df = pd.DataFrame({
    "variable": ["x", "y", "objective"],
    "value": [x_val, y_val, obj_val]
})
solution_df.to_csv(SOLUTION_PATH, index=False, encoding="utf-8-sig")
logger.info(f"✓ 决策变量已保存：{os.path.basename(SOLUTION_PATH)}")

# 2. 性能指标 (metrics.csv)
metrics_df = pd.DataFrame({
    "metric": ["objective_value", "solve_time_sec", "feasibility", "total_constraint_violation"],
    "value": [obj_val, elapsed, int(is_feasible), total_violation]
})
metrics_df.to_csv(METRICS_PATH, index=False, encoding="utf-8-sig")
logger.info(f"✓ 性能指标已保存：{os.path.basename(METRICS_PATH)}")

# 3. 约束检查 (constraints.csv)
constraints_df = pd.DataFrame(constraints_info)
constraints_df.to_csv(CONSTRAINT_PATH, index=False, encoding="utf-8-sig")
logger.info(f"✓ 约束检查已保存：{os.path.basename(CONSTRAINT_PATH)}")

# 4. 绘制可视化 (fig_solution.png)
try:
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    
    # 左图：可行域与最优解
    ax = axes[0]
    x_range = np.linspace(0, 15, 200)
    y_line = (10 - x_range) / 2  # x + 2y = 10
    
    ax.fill_between(x_range, y_line, 15, where=(y_line <= 15), alpha=0.3, color='blue', label='Feasible Region')
    ax.plot(x_range, y_line, 'b-', linewidth=2, label='x + 2y = 10')
    ax.plot(x_val, y_val, 'r*', markersize=20, label=f'Optimal: ({x_val:.2f}, {y_val:.2f})')
    
    ax.set_xlim(-0.5, 15)
    ax.set_ylim(-0.5, 8)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_title('LP 问题可行域与最优解')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # 右图：目标函数等高线
    ax = axes[1]
    x_grid = np.linspace(-1, 15, 100)
    y_grid = np.linspace(-1, 15, 100)
    X, Y = np.meshgrid(x_grid, y_grid)
    Z = X + Y  # 目标函数 x + y
    
    contour = ax.contour(X, Y, Z, levels=20, alpha=0.6)
    ax.clabel(contour, inline=True, fontsize=8)
    ax.fill_between(x_range, y_line, 15, where=(y_line <= 15), alpha=0.2, color='blue')
    ax.plot(x_range, y_line, 'b-', linewidth=2)
    ax.plot(x_val, y_val, 'r*', markersize=20, label=f'最优解')
    
    ax.set_xlim(-1, 15)
    ax.set_ylim(-1, 15)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_title('目标函数等高线')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    fig_path = get_figure_path("solution")
    plt.savefig(fig_path, dpi=150, bbox_inches='tight')
    plt.close()
    logger.info(f"✓ 图表已保存：{os.path.basename(fig_path)}")
except Exception as e:
    logger.warning(f"⚠ 图表生成失败：{e}")

logger.info("\n" + "="*70)
logger.info("任务完成！")
logger.info("="*70)
