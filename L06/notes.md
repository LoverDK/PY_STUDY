# L06 Matplotlib 折线与散点入门

阶段 A：DSBA/Python/可视化/复杂度。L03–L05 已会用 Pandas/NumPy 把表读进来、洗干净、按组汇总；本课开始把数字 **画成图**，让趋势与关系一眼可见。

**今日只讲**：`matplotlib.pyplot` 入门；`plt.plot`（折线）；`plt.scatter`（散点）；`xlabel` / `ylabel` / `title` / `grid`；多系列折线的基础样式（颜色、线型、标记）；figure/axes 直觉轻触。  
**明确不讲**：seaborn；仪表盘；`hist` / `bar`（留给 **L07**）；`legend` 深讲与 `savefig` 系统保存（L07）；sklearn；408；`itertools`/`collections`/`pathlib`；标准库 `json`/`math`/`re`/`os` 专题；迭代器/`yield`；类型标注专题；venv；Dataset/Trainer。

**运行本课**：在 `L06/` 目录下 `python examples.py`（需已安装 `matplotlib`、`numpy`、`pandas`）。无图形界面时脚本已设 `Agg` 后端，会把图存到 `out/` 并 `plt.close()`，不会卡住。

**中文标签提醒**：Windows 默认字体常无法显示中文，轴标题可能变成方框（口口）。本课作业与验收 **统一用英文标签**；课堂笔记示例若写中文，仅作说明，上机请改英文或自行配置字体。

---

## 1. 是什么

| 概念 | 准确定义 | 一眼识别 |
|------|----------|----------|
| **matplotlib** | Python 最常用的二维绘图库；考纲 **b** 可视化默认它 | `import matplotlib.pyplot as plt` |
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


---

# 本次授课补充：数据配对、选图理由与验收

## 一、是什么：图是数据含义的编码

Matplotlib 是 Python 的绘图库，pyplot 是常见的入门接口，惯例写成 import matplotlib.pyplot as plt。Figure 是整张画布，Axes 是画布上的一个坐标系；注意 Axes 不是单指某一根 x 轴或 y 轴。

plot(x, y) 把第 i 个横坐标和第 i 个纵坐标配成点，再按输入顺序连接。scatter(x, y) 表达同样的点对，但不主动连接，因而不暗示前后顺序。它们都不是“把两列数字随便扔进去”：同一位置上的 x/y 必须描述同一个观测。

例如 day=[1,2,3]、sales=[20,22,19] 表示三天销量。折线强调随天数先升后降；若 x 表示不同顾客的广告曝光次数、y 表示各自消费额，顾客行号通常没有需要连接的意义，应优先散点。

## 二、为什么：先明确问题，再决定画法

表格适合查精确数值，图适合发现整体趋势、异常观测和两变量关系。图不是表格的替代品，更不能凭漂亮的走势直接下统计结论。

“这十天销量如何变化？”关注有序变化，选折线；“广告费较高的样本是否通常销量也高？”关注关系，选散点。散点向右上延伸只能提示样本中存在正向关联，不能证明提高广告费必然导致销量上升；季节、价格、样本选择都可能影响结果。

同图双折线适合比较同横轴、同单位的两组观测，如 A/B 店销量。若把销量与温度直接放在同一纵轴，量纲不同会混淆读者，本课先分别画图。

标签要交代变量和单位，标题要交代对象或问题；网格帮助估读，但不能补救错误坐标。颜色用于区分系列，线型和标记还能让黑白打印下的系列可辨认。

## 三、怎么写：准备数据 → 新建图 → 绘制 → 标注 → 输出 → 关闭

下面是完整的交互式例题：一周销量走势与广告费—销量关系。两张图各自创建，避免内容叠加；它不要求写入任何磁盘文件。

```python
import matplotlib.pyplot as plt

days = [1, 2, 3, 4, 5, 6, 7]
sales = [20, 22, 19, 25, 24, 28, 27]
ad = [1, 2, 3, 4, 5, 6]
ad_sales = [10, 12, 15, 14, 18, 20]

if len(days) != len(sales):
    raise ValueError("days and sales must have equal length")
fig = plt.figure()
plt.plot(days, sales, color="steelblue", linestyle="-", marker="o")
plt.xlabel("Day")
plt.ylabel("Sales (units)")
plt.title("Weekly sales")
plt.grid(True)
plt.show()
plt.close(fig)

if len(ad) != len(ad_sales):
    raise ValueError("ad and sales must have equal length")
fig = plt.figure()
plt.scatter(ad, ad_sales, color="darkorange")
plt.xlabel("Ad spend")
plt.ylabel("Sales (units)")
plt.title("Ad spend vs Sales")
plt.grid(True)
plt.show()
plt.close(fig)
```

第一张图第 3 天回落，但第 7 天销量比第 1 天高，不能据此声称“每天都增长”。第二张图整体向右上延伸，第 4 个样本却低于第 3 个：关联不等于每一点严格单调，更不等于因果。

plot 的 color 控制颜色，linestyle="-" 表示实线、"--" 表示虚线，marker="o" 为圆点、"s" 为方点。plot(x,y,"b-o") 是蓝色实线圆点的简写，初学封装函数时用关键字更清楚。只写 plot(y) 时横轴默认 0 到 n-1；若业务横轴是第 1 到第 7 天，不应省略 x。

双系列示例：

```python
import matplotlib.pyplot as plt

x = [1, 2, 3, 4]
a = [10, 11, 13, 12]
b = [9, 10, 10, 12]
if not (len(x) == len(a) == len(b)):
    raise ValueError("length mismatch")
fig = plt.figure()
plt.plot(x, a, color="blue", linestyle="-", marker="o", label="A")
plt.plot(x, b, color="red", linestyle="--", marker="s", label="B")
plt.xlabel("Day")
plt.ylabel("Sales")
plt.title("A vs B")
plt.grid(True)
plt.legend()
plt.show()
plt.close(fig)
```

label 是系列名称；legend() 才把系列名称展示出来。不要只依赖红蓝颜色区分，线型和标记也不同更稳妥。

已有 Pandas 表时，先对成对列共同清洗，再按业务顺序画：

```python
sub = df[["day", "sales"]].dropna().sort_values("day")
plt.plot(sub["day"], sub["sales"], marker="o")
```

这里 df 应是已读入的 DataFrame。若日期是字符串，应先按真实日期含义转换，不要让字符串排序造成“1,10,2”的顺序。也不要为让图好看按 sales 排序，那会破坏时间顺序。

作业函数按题面保存 PNG：在无显示器脚本中先 import matplotlib，再 matplotlib.use("Agg")，最后导入 pyplot；绘制后 savefig(out_path)，然后 close 当前函数创建的 Figure，返回原样路径字符串。Agg 不会弹窗，适合批量渲染；交互学习可以 show。savefig 必须在 close 之前。保存目录须存在；样例脚本会准备自己的 out/。这里说明的是供你运行的代码契约，本次课件交付本身不在本地生成图。

## 四、易错点：会出图不等于图正确

1. 长度相同却配错观测。分别对 x/y dropna 后，长度甚至可能碰巧相同，但行对应已错。正确做法是对两列共同筛选，再同时取列。长度校验只能发现数量错误，不能发现语义错配。
2. 误以为 plot 自动按 x 排序。x=[3,1,2] 时它按 3→1→2 连线。时间趋势应把整对观测一起按时间排序；无序样本关系应换 scatter，不能只排序 x 而不调整 y。
3. 用 plot(df) 期待自动挑 day 当横轴。直接传二维数值表时通常按索引为多列画线。应显式写 plot(df["day"],df["sales"])。
4. 图越画越多、曲线叠加。pyplot 操作当前图；每张独立图先 figure，完成后 close(fig)。函数只关闭自己创建的图，不要随意 close("all") 干扰调用者。
5. 保存空图或找不到目录。先绘图和标注，再保存，最后关闭；父目录不存在时应由调用约定明确创建。本课只要求长度不匹配抛 ValueError，不要把所有异常都吞掉并假装成功。
6. 中文显示方框。常见原因是环境缺合适字体，并非绘图数据坏了；本课验收统一英文标签。透明度 alpha 影响重叠点可见性，scatter 的 s 表示标记面积而不是半径，切勿把面积增加误读成半径同比增加。

## 五、何时用：用问题检验选择

有序横轴下看变化，用 plot；无必须连接顺序的二维观测看关系，用 scatter。时间序列也可用散点强调离散采样，因此选择是表达目的，不是“时间数据绝不能 scatter”的硬规则。若连线会暗示不存在的连续过程，宁可只标出观测点并说明采样方式。

读图时依次问：横纵轴变量与单位是什么？每个点对应哪个观测？连线顺序是否有业务意义？坐标范围是否夸大波动？是否有异常或重叠点？是否把样本关联误说成因果？这些检查比换配色更重要。

机试封装顺序：先看函数签名和固定字符串，再校验长度、创建独立图、调用正确图元、补齐标签/标题/网格、按需 legend、保存并关闭、返回题定路径。除检查输出文件，还要检查图元、样式和异常行为；一张非空 PNG 不能证明题目做对。

## 三道练习摘要与硬验收

题目完整版本以 L06/homework.md 为准，本次保留原三道题的接口与评分要求。

1. plot_series(x,y,out_path)：实线圆点折线，标签 x/y、标题 series、网格；保存并关闭，返回原路径。长度不等必须 ValueError。
2. plot_scatter(x,y,out_path)：必须调用 scatter，标签 x/y、标题 scatter、网格；保存并关闭、返回路径，长度不等必须 ValueError。
3. plot_two_series(x,y1,y2,out_path)：蓝实线圆点 A、红虚线方点 B，标签 x/y、标题 A vs B、网格、图例；保存关闭并返回路径，三者长度不全等必须 ValueError。

共同验收：PNG 可解码且尺寸为正；正常/单点/等长空序列按题面契约完成，输入不被修改；异常长度不创建输出文件、不泄漏新 Figure；既有 Figure 不受影响；图元数量、数据、指定样式与固定文字逐项核对。输入限定为有限数值的一维列表或数组，输出为 .png 字符串路径且父目录已存在；不要求处理生成器、非数值输入或自动创建任意父目录。

标准答案：homework/answers.ipynb 当前为占位，约 9:30 写标准答案。

## 下节预告

L07 Matplotlib 柱状·直方图·图例与保存。今天先分清趋势和关系，下次学习类别比较、数值分布以及更规范的图例与保存。
