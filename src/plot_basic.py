import os
import pandas as pd
import matplotlib.pyplot as plt

# 设置中文字体（避免中文乱码，Windows 系统适用；Mac/Linux 需调整字体名）
plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False

# 获取脚本目录与项目根目录。
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

# 读取 src 目录下的 solution.csv。
solution_path = os.path.join(SCRIPT_DIR, "solution.csv")
df = pd.read_csv(solution_path)

# 过滤有效数据行（排除“总计”行）。
product_data = df[df["产品"] != "总计"].copy()

# 强制将“生产数量”“贡献利润”转为数值，避免字符串参与计算。
product_data["生产数量"] = pd.to_numeric(product_data["生产数量"], errors="coerce").fillna(0.0)
product_data["贡献利润"] = pd.to_numeric(product_data["贡献利润"], errors="coerce").fillna(0.0)

# 假设每单位资源消耗：ProductA=2，ProductB=3；未映射产品按 0 处理。
resource_consume_per_unit = {"ProductA": 2.0, "ProductB": 3.0}
consume_unit = product_data["产品"].map(resource_consume_per_unit).fillna(0.0)
product_data["资源消耗"] = consume_unit * product_data["生产数量"]

# 创建输出目录（项目根目录下 outputs/figures）。
fig_dir = os.path.join(PROJECT_ROOT, "outputs", "figures")
os.makedirs(fig_dir, exist_ok=True)

# ====================== 图1：柱状图（资源使用） ======================
fig1, ax1 = plt.subplots(figsize=(8, 5))
ax1.bar(
    product_data["产品"],
    product_data["资源消耗"],
    color=["#1f77b4", "#ff7f0e"],
    width=0.6,
)
ax1.set_title("资源使用情况", fontsize=14, pad=20)
ax1.set_xlabel("产品", fontsize=12)
ax1.set_ylabel("资源X消耗总量", fontsize=12)

for i, v in enumerate(product_data["资源消耗"]):
    value = float(v)
    ax1.text(i, value + 1.0, f"{value:.0f}", ha="center", fontsize=10)

plt.tight_layout()
plt.savefig(os.path.join(fig_dir, "resource_usage.png"), dpi=300, bbox_inches="tight")
plt.close()

# ====================== 图2：饼图（利润/成本构成） ======================
pie_data = product_data["贡献利润"]
pie_labels = product_data["产品"]

fig2, ax2 = plt.subplots(figsize=(8, 6))
ax2.pie(
    pie_data,
    labels=pie_labels,
    autopct="%1.1f%%",
    colors=["#1f77b4", "#ff7f0e"],
    startangle=90,
    textprops={"fontsize": 12},
)
ax2.set_title("利润构成", fontsize=14, pad=20)
plt.tight_layout()
plt.savefig(os.path.join(fig_dir, "profit_composition.png"), dpi=300, bbox_inches="tight")
plt.close()

# ====================== 图3：条形图（利润构成） ======================
fig3, ax3 = plt.subplots(figsize=(8, 5))
ax3.barh(product_data["产品"], product_data["贡献利润"], color=["#1f77b4", "#ff7f0e"])
ax3.set_title("利润构成（条形图）", fontsize=14, pad=20)
ax3.set_xlabel("贡献利润（元）", fontsize=12)

for i, v in enumerate(product_data["贡献利润"]):
    value = float(v)
    ax3.text(value + 2.0, i, f"{value:.0f}", va="center", fontsize=10)

plt.tight_layout()
plt.savefig(os.path.join(fig_dir, "profit_composition_bar.png"), dpi=300, bbox_inches="tight")
plt.close()

print("图表生成完成！已保存：")
print("1. 资源使用柱状图：outputs/figures/resource_usage.png")
print("2. 利润构成饼图：outputs/figures/profit_composition.png")
print("3. 利润构成条形图：outputs/figures/profit_composition_bar.png")