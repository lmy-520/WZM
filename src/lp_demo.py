"""
最小 LP Demo
目标：最小化 x + y
约束：x + 2y >= 10，x, y >= 0
输出结果写成 DataFrame 并保存为 outputs/tables/solution.csv
"""

import logging
import os
import time
import pandas as pd
import pulp

# ── 日志配置 ──────────────────────────────────────────────────────────────────
LOG_DIR = os.path.join(os.path.dirname(__file__), "..", "outputs")
os.makedirs(LOG_DIR, exist_ok=True)
log_path = os.path.join(LOG_DIR, "lp_demo.log")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(log_path, encoding="utf-8"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)

# ── 构建模型 ──────────────────────────────────────────────────────────────────
logger.info("开始构建 LP 模型")
start_time = time.time()

prob = pulp.LpProblem("min_x_plus_y", pulp.LpMinimize)

x = pulp.LpVariable("x", lowBound=0)
y = pulp.LpVariable("y", lowBound=0)

# 目标函数
prob += x + y, "Objective"

# 约束
prob += x + 2 * y >= 10, "constraint_1"

logger.info("模型构建完成，变量：x, y；约束：x + 2y >= 10")

# ── 求解 ──────────────────────────────────────────────────────────────────────
logger.info("开始求解...")
status = prob.solve(pulp.PULP_CBC_CMD(msg=0))
elapsed = time.time() - start_time

logger.info(f"求解完成，状态：{pulp.LpStatus[status]}，耗时：{elapsed:.4f}s")

# ── 结果整理 ──────────────────────────────────────────────────────────────────
result = {
    "variable": ["x", "y", "objective"],
    "value": [pulp.value(x), pulp.value(y), pulp.value(prob.objective)],
}
df = pd.DataFrame(result)

logger.info(f"\n{df.to_string(index=False)}")

# ── 保存 CSV ──────────────────────────────────────────────────────────────────
out_dir = os.path.join(os.path.dirname(__file__), "..", "outputs", "tables")
os.makedirs(out_dir, exist_ok=True)
csv_path = os.path.join(out_dir, "solution.csv")
df.to_csv(csv_path, index=False, encoding="utf-8-sig")

logger.info(f"结果已保存至：{os.path.normpath(csv_path)}")
logger.info("任务完成")
