# 复现说明（给未来的你/队友/评审）

## 1. 运行环境
- 推荐：Windows + Conda
- 建议环境名：`mm-opt`
- 你的本机环境路径：`D:\Anaconda\envs\mm-opt`
- Python 版本：`3.10+`

## 2. 安装依赖
```bash
conda create -n mm-opt python=3.10 -y
conda activate mm-opt
pip install -U pip
pip install numpy pandas matplotlib pulp
```

## 3. 运行命令
- 线性规划最小示例（会产出 csv + 图）：
```bash
python src/lp_demo.py
```
- 三维场景示意图（独立脚本，可选）：
```bash
python muthercup/main.py
```

## 4. 输出文件位置
- 结果表：`outputs/tables/solution.csv`
- 指标表：`outputs/tables/metrics.csv`
- 约束检查：`outputs/tables/constraints.csv`
- LP 可视化：`outputs/figures/fig_solution.png`
- 运行日志：`outputs/lp_demo.log`
- 场景图（运行 `main.py` 后）：`scene_plot.png`

## 5. 常见问题
- 若 `pulp` 求解报错，先确认当前环境已安装 `pulp`。
- 若中文乱码，确认系统有 `Microsoft YaHei/SimHei` 字体（`muthercup/main.py` 已做兼容设置）。
