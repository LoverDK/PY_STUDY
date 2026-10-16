#!/usr/bin/env python3
"""L06 Matplotlib 课堂示例：折线与散点。在 L06/ 目录下运行。无 GUI 时用 Agg。"""
from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
OUT = HERE / "out"
OUT.mkdir(exist_ok=True)


def section(title: str) -> None:
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


def demo_plot_basic() -> None:
    section("1. 最简折线 plot + 标签 + 网格")
    x = [1, 2, 3, 4, 5]
    y = [2, 4, 3, 6, 5]
    plt.figure()
    plt.plot(x, y)
    plt.xlabel("Day")
    plt.ylabel("Sales")
    plt.title("Sales over days")
    plt.grid(True)
    path = OUT / "plot_basic.png"
    plt.savefig(path)
    plt.close()
    print("saved:", path)


def demo_plot_styles() -> None:
    section("2. 多系列折线：颜色 / 线型 / 标记")
    x = np.arange(1, 8)
    y1 = np.array([10, 12, 11, 15, 14, 18, 17])
    y2 = np.array([9, 10, 12, 11, 13, 14, 16])
    plt.figure()
    plt.plot(x, y1, color="blue", linestyle="-", marker="o", label="store_A")
    plt.plot(x, y2, color="red", linestyle="--", marker="s", label="store_B")
    plt.xlabel("Day")
    plt.ylabel("Sales")
    plt.title("Two stores")
    plt.grid(True)
    plt.legend()
    path = OUT / "plot_two_series.png"
    plt.savefig(path)
    plt.close()
    print("saved:", path)

    # 格式字符串写法
    plt.figure()
    plt.plot(x, y1, "b-o", label="store_A")
    plt.plot(x, y2, "r--s", label="store_B")
    plt.legend()
    path2 = OUT / "plot_fmt_string.png"
    plt.savefig(path2)
    plt.close()
    print("saved:", path2)


def demo_scatter() -> None:
    section("3. 散点 scatter")
    rng = np.random.default_rng(0)
    x = rng.normal(0, 1, 50)
    y = 2 * x + rng.normal(0, 0.5, 50)
    plt.figure()
    plt.scatter(x, y, color="darkorange", alpha=0.85)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title("Scatter demo")
    plt.grid(True)
    path = OUT / "scatter_basic.png"
    plt.savefig(path)
    plt.close()
    print("saved:", path)

    plt.figure()
    sizes = np.abs(y) * 40
    plt.scatter(x, y, s=sizes, c=y, cmap="viridis", alpha=0.8)
    plt.colorbar()
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title("Scatter with size/color")
    path2 = OUT / "scatter_size_color.png"
    plt.savefig(path2)
    plt.close()
    print("saved:", path2)


def demo_numpy_pandas() -> None:
    section("4. 用 NumPy / Pandas 准备数据")
    t = np.linspace(0, 2 * np.pi, 100)
    plt.figure()
    plt.plot(t, np.sin(t), label="sin")
    plt.plot(t, np.cos(t), label="cos")
    plt.xlabel("t")
    plt.ylabel("value")
    plt.title("sin and cos")
    plt.grid(True)
    plt.legend()
    path = OUT / "plot_sin_cos.png"
    plt.savefig(path)
    plt.close()
    print("saved:", path)

    csv_path = HERE / "sales_daily.csv"
    df = pd.read_csv(csv_path, encoding="utf-8")
    df = df[["day", "sales"]].dropna().sort_values("day")
    plt.figure()
    plt.plot(df["day"], df["sales"], marker="o", color="steelblue")
    plt.xlabel("day")
    plt.ylabel("sales")
    plt.title("From CSV via pandas")
    plt.grid(True)
    path2 = OUT / "plot_from_csv.png"
    plt.savefig(path2)
    plt.close()
    print("saved:", path2)
    print("rows:", len(df))


def demo_pitfalls() -> None:
    section("5. 易错点对照")
    # 长度检查
    x = [1, 2, 3]
    y_bad = [10, 20]
    print("len mismatch?", len(x) != len(y_bad))
    try:
        plt.figure()
        plt.plot(x, y_bad)
        plt.close()
    except ValueError as e:
        print("plot length error (expected):", type(e).__name__)
        plt.close("all")

    # DataFrame 整表 plot vs 指定列
    df = pd.DataFrame({"day": [1, 2, 3], "a": [1, 2, 3], "b": [3, 2, 1]})
    plt.figure()
    plt.plot(df)  # 多列 + 索引为 x —— 演示「可能不是你想要的」
    path = OUT / "pitfall_plot_whole_df.png"
    plt.savefig(path)
    plt.close()
    print("whole df plot saved (often wrong intent):", path)

    plt.figure()
    plt.plot(df["day"], df["a"], marker="o")
    path2 = OUT / "pitfall_plot_explicit_cols.png"
    plt.savefig(path2)
    plt.close()
    print("explicit columns saved:", path2)

    # 无序点：plot 乱连 vs scatter
    xu = [3, 1, 4, 2]
    yu = [2, 5, 1, 4]
    plt.figure()
    plt.plot(xu, yu, "b-o")
    plt.title("Wrong: unordered as line")
    plt.savefig(OUT / "pitfall_unordered_plot.png")
    plt.close()
    plt.figure()
    plt.scatter(xu, yu, color="green")
    plt.title("Right: scatter")
    plt.savefig(OUT / "pitfall_unordered_scatter.png")
    plt.close()
    print("unordered plot vs scatter demos saved")


def demo_exam_style() -> None:
    section("6. 课堂例题串讲")
    days = [1, 2, 3, 4, 5, 6, 7]
    sales = [20, 22, 19, 25, 24, 28, 27]
    plt.figure()
    plt.plot(days, sales, color="steelblue", marker="o")
    plt.xlabel("Day")
    plt.ylabel("Sales")
    plt.title("Weekly sales")
    plt.grid(True)
    plt.savefig(OUT / "exam1_weekly.png")
    plt.close()

    ad = np.array([1, 2, 3, 4, 5, 6], dtype=float)
    sales2 = np.array([10, 12, 15, 14, 18, 20], dtype=float)
    plt.figure()
    plt.scatter(ad, sales2, color="darkorange")
    plt.xlabel("Ad spend")
    plt.ylabel("Sales")
    plt.title("Ad vs Sales")
    plt.grid(True)
    plt.savefig(OUT / "exam2_scatter.png")
    plt.close()

    x = [1, 2, 3, 4, 5]
    a = [10, 11, 13, 12, 15]
    b = [9, 10, 10, 12, 13]
    plt.figure()
    plt.plot(x, a, "b-o", label="A")
    plt.plot(x, b, "r--s", label="B")
    plt.xlabel("Day")
    plt.ylabel("Sales")
    plt.title("A vs B")
    plt.grid(True)
    plt.legend()
    plt.savefig(OUT / "exam3_two.png")
    plt.close()
    print("exam figures saved under", OUT)


def main() -> None:
    demo_plot_basic()
    demo_plot_styles()
    demo_scatter()
    demo_numpy_pandas()
    demo_pitfalls()
    demo_exam_style()
    print("\n[L06 examples OK]")


if __name__ == "__main__":
    main()
