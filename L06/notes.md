# L06 Matplotlib 折线与散点入门

对应考纲 **b**（基本分析与可视化）。L03–L05 已会用 Pandas/NumPy 把表读进来、洗干净、按组汇总；本课开始把数字 **画成图**，让趋势与关系一眼可见。

**今日只讲**：`matplotlib.pyplot` 入门；`plt.plot`（折线）；`plt.scatter`（散点）；`xlabel` / `ylabel` / `title` / `grid`；多系列折线的基础样式（颜色、线型、标记）；figure/axes 直觉轻触。  
**明确不讲**：seaborn；仪表盘；`hist` / `bar`（留给 **L07**）；`legend` 深讲与 `savefig` 系统保存（L07）；sklearn；408；`itertools`/`collections`/`pathlib`；标准库 `json`/`math`/`re`/`os` 专题；迭代器/`yield`；类型标注专题；venv；Dataset/Trainer。

**运行本课**：在 `L06/` 目录下 `python examples.py`（需已安装 `matplotlib`、`numpy`；可选 `pandas`）。无图形界面时脚本已设 `Agg` 后端，会把图存到 `out/` 并 `plt.close()`，不会卡住。

**中文标签提醒**：Windows 默认字体常无法显示中文，轴标题可能变成方框（口口）。本课作业与验收 **统一用英文标签**；课堂笔记示例若写中文，仅作说明，上机请改英文或自行配置字体。

---

## 1. 是什么

| 概念 | 准确定义 | 一眼识别 |
|------|----------|----------|
| **matplotlib** | Python 最常用的二维绑图库；考纲 **b** 可视化默认它 | `import matplotlib.pyplot as plt` |
| **pyplot（plt）** | 提供「当前图」式 API：像 MATLAB 一样连续调用 `plot`/`xlabel`/`show` | 几乎所有入门代码都是 `plt.xxx` |
| **Figure** | 整张画布（窗口/图片文件） | `plt.figure()`；一张图一个 Figure |
| **Axes** | 画布上的一个坐标系（真正画曲线的那块区域） | 一张 Figure 可有多个 Axes；初学可先忽略，用 pyplot 默认的「当前 Axes」 |
| **折线图 `plot`** | 把点按给定顺序用线段连起来，强调 **顺序/趋势** | `plt.plot(x, y)` |
| **散点图 `scatter`** | 只画点、默认不连线，强调 **两个变量的关系/分布** | `plt.scatter(x, y)` |
| **标签与网格** | 坐标轴名、图标题、背景网格线，让图可读 | `xlabel`/`ylabel`/`title`/`grid(True)` |

```python
import matplotlib
matplotlib.use("Agg")          # 无显示器/脚本环境：先设后端再 import pyplot
import matplotlib.pyplot as plt
import numpy as np

x = np.array([1, 2, 3, 4])
y = np.array([2, 3, 5, 4])
plt.plot(x, y)                 # 折线
plt.xlabel("x")
plt.ylabel("y")
plt.title("demo")
plt.grid(True)
# 交互环境：plt.show()
# 脚本环境：plt.savefig("out/demo.png"); plt.close()
```

**Figure vs Axes（轻触即可）**：

- `plt.plot(...)` 实际是在「当前 Figure 的当前 Axes」上画。
- 初学阶段用 pyplot 状态机就够：`plot` → 加标签 → `show`/`savefig` → `close`。
- 以后做子图（一行两列）会显式拿 `ax`；L07 及以后再加深。

---

## 2. 为什么（考纲与考法）

考纲 **b** 写「基本分析与可视化」。机考/评估常见问法：

- 给定两组等长序列，画折线，并加上 `xlabel`/`ylabel`/`title`
- 给定 `(x, y)` 点集，画散点，观察是否大致线性相关
- 同一张图上画两条折线（如 train loss / val loss），用不同颜色或线型区分
- 打开网格，便于读坐标
- （本课作业）写成函数：输入数组 → 画图 → 返回 Figure 或保存路径，便于自动验收

卡分点几乎总是：`x` 与 `y` 长度不一致；把 DataFrame 整表塞进 `plot` 却期望只画一列；脚本里既不 `show` 也不 `savefig`/`close` 导致「没图」或进程挂起；中文标签在评分机上变方框；`plot` 与 `scatter` 用反（时间序列却用散点、相关关系却用折线乱连）。

---

## 3. 怎么写（简 → 繁）

下列示例可在 `L06/` 下运行；脚本版见 `examples.py`。

### 3.1 导入与后端

```python
import matplotlib
matplotlib.use("Agg")   # 必须在 import pyplot 之前（若环境无 GUI）
import matplotlib.pyplot as plt
import numpy as np
# 可选：用 pandas 准备序列
import pandas as pd
```

课堂交互（Jupyter / 带界面的 IDE）通常直接：

```python
import matplotlib.pyplot as plt
```

不必每次写 `Agg`；**写 `.py` 脚本批量出图**时建议 `Agg` + `savefig` + `close`。

### 3.2 最简折线：`plt.plot`

```python
x = [1, 2, 3, 4, 5]
y = [2, 4, 3, 6, 5]
plt.plot(x, y)
plt.xlabel("Day")
plt.ylabel("Sales")
plt.title("Sales over days")
plt.grid(True)
plt.savefig("out/plot_basic.png")
plt.close()
```

只传一个序列时，横轴自动为 `0, 1, 2, ...`：

```python
plt.plot([3, 1, 4, 1, 5])   # x = 0..4
plt.close()
```

### 3.3 折线样式：颜色、线型、标记

常用简写（可组合在一个格式字符串里，也可分开关键字）：

| 元素 | 常见取值 | 含义 |
|------|----------|------|
| 颜色 | `r` `g` `b` `k` `c` `m` `y`；或 `color="tab:blue"` | red/green/blue/black/... |
| 线型 | `-` 实线；`--` 虚线；`:` 点线；`-.` 点划 | `linestyle` |
| 标记 | `o` 圆；`s` 方；`^` 三角；`.` 小点 | `marker` |

```python
x = np.arange(1, 8)
y1 = np.array([10, 12, 11, 15, 14, 18, 17])
y2 = np.array([9, 10, 12, 11, 13, 14, 16])

plt.plot(x, y1, "b-o", label="store_A")       # 蓝实线+圆点
plt.plot(x, y2, "r--s", label="store_B")      # 红虚线+方点
plt.xlabel("Day")
plt.ylabel("Sales")
plt.title("Two stores")
plt.grid(True)
plt.legend()                                   # 多系列时看一眼即可；深讲留给 L07
plt.savefig("out/plot_two_series.png")
plt.close()
```

等价的关键字写法（更清晰，推荐作业用）：

```python
plt.plot(x, y1, color="blue", linestyle="-", marker="o", label="store_A")
plt.plot(x, y2, color="red", linestyle="--", marker="s", label="store_B")
```

### 3.4 散点：`plt.scatter`

```python
rng = np.random.default_rng(0)
x = rng.normal(0, 1, 50)
y = 2 * x + rng.normal(0, 0.5, 50)

plt.scatter(x, y)
plt.xlabel("x")
plt.ylabel("y")
plt.title("Scatter demo")
plt.grid(True)
plt.savefig("out/scatter_basic.png")
plt.close()
```

可选：点大小 `s`、颜色 `c`（本课轻触，不要求掌握色条）：

```python
sizes = np.abs(y) * 30
plt.scatter(x, y, s=sizes, c=y, cmap="viridis", alpha=0.8)
plt.colorbar()   # 可选
plt.close()
```

### 3.5 标签、标题、网格（必会）

```python
plt.plot(x, y)
plt.xlabel("Hours studied")      # 横轴名
plt.ylabel("Exam score")         # 纵轴名
plt.title("Hours vs Score")      # 图标题
plt.grid(True)                   # 打开网格；plt.grid(False) 关闭
# plt.grid(True, linestyle="--", alpha=0.5)  # 可微调
```

**作业约定**：轴标签与标题一律英文，避免评分环境中文字体缺失。

### 3.6 用 NumPy / Pandas 准备数据再画

```python
# NumPy
t = np.linspace(0, 2 * np.pi, 100)
plt.plot(t, np.sin(t), label="sin")
plt.plot(t, np.cos(t), label="cos")
plt.legend()
plt.close()

# Pandas：从列取序列
df = pd.DataFrame({"day": [1, 2, 3, 4], "sales": [10, 12, 9, 15]})
plt.plot(df["day"], df["sales"], marker="o")
plt.xlabel("day")
plt.ylabel("sales")
plt.close()

# 注意：plt.plot(df) 会按「数值列」各自画线，且用索引当 x —— 常不是你想要的
```

### 3.7 `show` vs 保存 vs `close`（本课策略）

| 环境 | 建议 |
|------|------|
| Jupyter / 交互 | `plt.show()` 或单元格自动显示 |
| `.py` 脚本（本课 examples） | `plt.savefig(...)` + `plt.close()` |
| 机试函数题 | 按题面：有的要求 `return fig`，有的要求保存到给定路径 |

`plt.close()` 释放当前图，避免循环画多张时内存涨、图叠在一起。系统保存参数（dpi、bbox）留给 **L07**。

---

## 4. 易错点（至少两个，含对照）

### 坑 1：`x` 与 `y` 长度不一致

```python
x = [1, 2, 3]
y = [10, 20]           # 长度 2
# plt.plot(x, y)       # ValueError: x and y must have same first dimension
```

**对法**：画之前检查 `len(x) == len(y)`；从 DataFrame 取列时注意是否因 `dropna` 导致两列长度不再对齐——应对 **同一批行** 一起过滤：

```python
sub = df[["day", "sales"]].dropna()
plt.plot(sub["day"], sub["sales"])
```

### 坑 2：脚本里既不 `show` 也不 `savefig`，或忘了 `close`

```python
# 错：函数返回了，图在内存里，磁盘没有文件，交互窗口也可能没弹
plt.plot([1, 2, 3], [1, 4, 9])
# 没有 show / savefig

# 对（脚本）：
plt.plot([1, 2, 3], [1, 4, 9])
plt.savefig("out/ok.png")
plt.close()
```

循环里若只 `plot` 不 `close`，后面的图可能画在同一张 Figure 上，线叠在一起。

### 坑 3：把整张 DataFrame 直接 `plt.plot(df)` 却期望只画一列

```python
df = pd.DataFrame({"day": [1, 2, 3], "a": [1, 2, 3], "b": [3, 2, 1]})
plt.plot(df)    # 会画多条线，x 轴是行索引 0,1,2，不是 day
plt.close()

# 对：明确指定 x 与 y
plt.plot(df["day"], df["a"])
plt.close()
```

### 坑 4：该用散点却用折线（或反过来）

```python
# 无序的相关点：折线会按行号乱连，看起来像乱麻
x = [3, 1, 4, 2]
y = [2, 5, 1, 4]
plt.plot(x, y)       # 通常错误的可视化选择
plt.scatter(x, y)    # 正确：只看分布/关系
```

时间序列、按 day/hour 已排序的趋势 → **`plot`**。  
身高-体重、广告费-销量等二元关系（点无「必须连接」的顺序）→ **`scatter`**。

### 坑 5：中文标签在 Windows 上显示为方框

```python
plt.xlabel("天数")   # 默认字体可能变成 □□
# 作业请写：
plt.xlabel("Day")
```

若必须在本机显示中文，需配置字体（如微软雅黑），**不在本课考试范围**，作业统一英文即可。

---

## 5. 何时用（对比）

| 需求 | 用 | 别用 |
|------|-----|------|
| 展示随时间/序号变化的趋势 | **`plt.plot`** | 无序点硬连成折线 |
| 展示两变量关系、相关性、聚类感 | **`plt.scatter`** | 用折线按行号乱连 |
| 让阅卷人读懂轴含义 | **`xlabel`/`ylabel`/`title`** | 裸图无字 |
| 方便估读数值 | **`grid(True)`** | 密图还关网格（除非题面禁止） |
| 脚本批量出图 | **`savefig` + `close`** | 依赖弹窗 `show`（无界面会挂） |

| A | B | 怎么选 |
|---|---|--------|
| `plot` | `scatter` | 有序趋势 → plot；关系/分布 → scatter |
| 格式串 `"b-o"` | `color=`/`linestyle=`/`marker=` | 快速演示可用格式串；作业推荐关键字，可读 |
| `plt.plot(y)` | `plt.plot(x, y)` | 横轴就是 0..n-1 时可以只传 y；有业务横轴必须传 x |
| 一张图多条线 | 多张图 | 可比系列（同单位）→ 同图多 `plot`；单位/含义差太远 → 分开画 |

---

## 6. 课堂例题（考研风）

**例 1** 给定一周每日销量，画折线（带标记），英文轴标签，打开网格。

```python
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

days = [1, 2, 3, 4, 5, 6, 7]
sales = [20, 22, 19, 25, 24, 28, 27]
plt.plot(days, sales, color="steelblue", marker="o")
plt.xlabel("Day")
plt.ylabel("Sales")
plt.title("Weekly sales")
plt.grid(True)
plt.savefig("out/exam1_weekly.png")
plt.close()
```

**例 2** 给定广告支出与销量的若干观测，画散点；目视是否大致正相关。

```python
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ad = np.array([1, 2, 3, 4, 5, 6])
sales = np.array([10, 12, 15, 14, 18, 20])
plt.scatter(ad, sales, color="darkorange")
plt.xlabel("Ad spend")
plt.ylabel("Sales")
plt.title("Ad vs Sales")
plt.grid(True)
plt.savefig("out/exam2_scatter.png")
plt.close()
```

**例 3** 同一张图画两条折线（A/B 店），不同线型。

```python
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

x = [1, 2, 3, 4, 5]
a = [10, 11, 13, 12, 15]
b = [9, 10, 10, 12, 13]
plt.plot(x, a, "b-o", label="A")
plt.plot(x, b, "r--s", label="B")
plt.xlabel("Day")
plt.ylabel("Sales")
plt.title("A vs B")
plt.grid(True)
plt.legend()
plt.savefig("out/exam3_two.png")
plt.close()
```

---

## 下节预告

**L07**：Matplotlib 柱状 · 直方图 · 图例与保存（`bar`/`hist`、图例规范、`savefig` 参数）。
