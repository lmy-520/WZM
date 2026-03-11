import matplotlib
import matplotlib.pyplot as plt
import numpy as np


matplotlib.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "Arial Unicode MS", "DejaVu Sans"]
matplotlib.rcParams["axes.unicode_minus"] = False


def plot_scene():
    fig = plt.figure(figsize=(11, 7))
    ax = fig.add_subplot(111, projection="3d")

    missile_points = {
        "M1": (20000, 0, 2000),
        "M2": (19000, 600, 2100),
        "M3": (18000, -600, 1900),
    }
    drone_points = {
        "FY1": (17800, 0, 1800),
        "FY2": (12000, 1400, 1400),
        "FY3": (6000, -3000, 700),
        "FY4": (11000, 2000, 1800),
        "FY5": (13000, -2000, 1300),
    }

    decoy_center = np.array([0, 0, 0])
    true_target_center = np.array([0, 200, 0])

    radius = 7
    height = 10
    theta = np.linspace(0, 2 * np.pi, 120)
    z = np.linspace(0, height, 40)
    theta_grid, z_grid = np.meshgrid(theta, z)
    x_grid = radius * np.cos(theta_grid)
    y_grid = radius * np.sin(theta_grid)
    ax.plot_surface(x_grid, y_grid, z_grid, alpha=0.35, color="orange", linewidth=0)

    ax.scatter(*decoy_center, color="orange", s=70, marker="x", label="假目标原点")
    ax.scatter(*true_target_center, color="red", s=60, marker="*", label="真目标底面圆心")

    for name, point in missile_points.items():
        ax.scatter(*point, color="blue", s=65)
        ax.text(point[0], point[1], point[2] + 80, name, color="blue")

    for name, point in drone_points.items():
        ax.scatter(*point, color="green", s=45)
        ax.text(point[0], point[1], point[2] + 80, name, color="green")

    ax.plot(
        [missile_points["M1"][0], decoy_center[0]],
        [missile_points["M1"][1], decoy_center[1]],
        [missile_points["M1"][2], decoy_center[2]],
        "--",
        color="gray",
        alpha=0.8,
        label="M1 指向假目标(示意)",
    )

    all_points = list(missile_points.values()) + list(drone_points.values())
    xs = [p[0] for p in all_points] + [decoy_center[0], true_target_center[0]]
    ys = [p[1] for p in all_points] + [decoy_center[1], true_target_center[1]]
    zs = [p[2] for p in all_points] + [decoy_center[2], true_target_center[2]]

    x_min, x_max = min(xs), max(xs)
    y_min, y_max = min(ys), max(ys)
    z_min, z_max = min(zs), max(zs)
    x_pad = (x_max - x_min) * 0.06
    y_pad = (y_max - y_min) * 0.08
    z_pad = (z_max - z_min) * 0.08

    ax.set_xlim(x_min - x_pad, x_max + x_pad)
    ax.set_ylim(y_min - y_pad, y_max + y_pad)
    ax.set_zlim(0, z_max + z_pad)

    ax.set_xlabel("X (m)")
    ax.set_ylabel("Y (m)")
    ax.set_zlabel("Z (m)")
    ax.set_title("导弹-无人机-目标三维空间近似示意图")
    ax.grid(True, linestyle="--", alpha=0.3)

    try:
        ax.set_box_aspect([x_max - x_min, y_max - y_min, z_max - z_min + 1e-6])
    except Exception:
        pass

    ax.legend(loc="upper right")
    plt.tight_layout()
    if plt.get_backend().lower().endswith("agg"):
        output_file = "scene_plot.png"
        plt.savefig(output_file, dpi=200, bbox_inches="tight")
        print(f"当前后端为 {plt.get_backend()}，已保存图像到 {output_file}")
    else:
        plt.show()


if __name__ == "__main__":
    plot_scene()
