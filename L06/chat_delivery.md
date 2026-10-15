# 每日 DSBA-Python · L06

**Matplotlib 折线与散点入门**

对应考纲 **b**。L03–L05 已会读表、清洗、分组汇总；本课把数字 **画成图**。  
**今日范围**：`matplotlib.pyplot`；`plt.plot`（折线）；`plt.scatter`（散点）；`xlabel`/`ylabel`/`title`/`grid`；多系列基础样式。  
**不讲**：seaborn；仪表盘；`hist`/`bar`（**L07**）；`savefig` 深参数与图例规范（L07）；sklearn；408。

**中文标签**：Windows 默认字体常显示为方框。作业与验收 **统一英文轴标签**。

---

## 今日目标

1. 会 `import matplotlib.pyplot as plt`；脚本无 GUI 时知道先 `matplotlib.use("Agg")`  
2. 会 `plt.plot(x, y)` 画折线，并加 `xlabel`/`ylabel`/`title`/`grid(True)`  
3. 会改颜色、线型、标记；能在一张图上画两条折线并 `legend()`（轻量）  
4. 会 `plt.scatter(x, y)`；分清何时用折线、何时用散点  
5. 知道 `x`/`y` 等长校验；脚本里 `savefig` + `close`；完成三道练习

---

## 详实讲解

### 1. 是什么

| 概念 | 定义 | 怎么看 |
|------|------|--------|
| **pyplot（plt）** | Matplotlib 的「当前图」式 API | `import matplotlib.pyplot as plt` |
| **Figure / Axes** | 画布 / 画布上的坐标系 | 初学用 plt 默认当前轴即可 |
| **折线 plot** | 按顺序把点连成线，看趋势 | `plt.plot(x, y)` |
| **散点 scatter** | 只画点不连线，看两变量关系 | `plt.scatter(x, y)` |
| **标签与网格** | 轴名、标题、网格线 | `xlabel`/`ylabel`/`title`/`grid(True)` |

```python
import matplotlib
matplotlib.use("Agg")   # 无显示器的脚本：先设后端
import matplotlib.pyplot as plt
import numpy as np

x = np.array([1, 2, 3, 4])
y = np.array([2, 3, 5, 4])
plt.plot(x, y)
plt.xlabel("x")
plt.ylabel("y")
plt.title("demo")
plt.grid(True)
plt.savefig("out/demo.png")
plt.close()
```

### 2. 为什么

考纲 **b** 的可视化在机考里经常落成：

- 给定序列画折线，并写上轴标签与标题  
- 给定点集画散点，观察相关  
- 同图两条折线（不同颜色/线型）  
- 打开网格便于读数  

易扣分：`x`/`y` 长度不一致；整张 DataFrame 丢进 `plot`；脚本不保存也不 `close`；该用散点却用折线乱连；中文标签变方框。

### 3. 怎么写（简 → 繁）

**最简折线**

```python
plt.plot([1, 2, 3, 4, 5], [2, 4, 3, 6, 5])
plt.xlabel("Day")
plt.ylabel("Sales")
plt.title("Sales over days")
plt.grid(True)
plt.savefig("out/plot_basic.png")
plt.close()
```

只传一个列表时，横轴自动是 `0,1,2,...`：`plt.plot([3, 1, 4, 1, 5])`。

**样式：颜色 / 线型 / 标记**

| 元素 | 例 |
|------|-----|
| 颜色 | `r` `g` `b` `k`；或 `color="tab:blue"` |
| 线型 | `-` 实线；`--` 虚线；`:` 点线 |
| 标记 | `o` 圆；`s` 方；`^` 三角 |

```python
x = [1, 2, 3, 4, 5]
plt.plot(x, [10, 12, 11, 15, 14], color="blue", linestyle="-", marker="o", label="A")
plt.plot(x, [9, 10, 12, 11, 13], color="red", linestyle="--", marker="s", label="B")
plt.xlabel("Day")
plt.ylabel("Sales")
plt.title("Two stores")
plt.grid(True)
plt.legend()
plt.savefig("out/two.png")
plt.close()
```

也可写格式串：`plt.plot(x, y, "b-o")`。作业推荐关键字写法，更清晰。

**散点**

```python
import numpy as np
rng = np.random.default_rng(0)
x = rng.normal(0, 1, 50)
y = 2 * x + rng.normal(0, 0.5, 50)
plt.scatter(x, y)
plt.xlabel("x")
plt.ylabel("y")
plt.title("Scatter demo")
plt.grid(True)
plt.savefig("out/scatter.png")
plt.close()
```

可选：`s` 控制点大小，`c` 控制颜色（本课轻触）。

**用 Pandas 取列再画**

```python
import pandas as pd
df = pd.DataFrame({"day": [1, 2, 3, 4], "sales": [10, 12, 9, 15]})
plt.plot(df["day"], df["sales"], marker="o")
# 不要指望 plt.plot(df) 一定按 day 画 —— 它常用行索引当 x，并画多列
```

**show vs 保存**

| 环境 | 做法 |
|------|------|
| Jupyter | `plt.show()` 或自动显示 |
| `.py` 脚本 | `savefig` + `close`（本课 examples 即如此） |

### 4. 易错点

| 错法 | 对法 |
|------|------|
| `len(x) != len(y)` 仍 plot | 先检查长度；或对 DataFrame 同一批行 `dropna` |
| 只 plot 不 savefig/close | 脚本里保存后 `plt.close()` |
| `plt.plot(df)` 期望只画一列 | `plt.plot(df["day"], df["sales"])` |
| 无序相关点用折线乱连 | 改用 `scatter` |
| 轴标签写中文，评分机方框 | 作业统一英文：`xlabel("Day")` |

```python
# 长度不一致 → ValueError
# plt.plot([1, 2, 3], [10, 20])

# 无序点
xu, yu = [3, 1, 4, 2], [2, 5, 1, 4]
# plt.plot(xu, yu)    # 通常不合适
plt.scatter(xu, yu)   # 合适
```

### 5. 何时用

| 需求 | 用 | 别用 |
|------|-----|------|
| 有序趋势（时间、天数） | **plot** | 无序点硬连线 |
| 两变量关系 / 分布 | **scatter** | 按行号折线乱连 |
| 让人读懂 | **xlabel/ylabel/title** | 裸图 |
| 便于估读 | **grid(True)** | 无故关网格 |
| 批量脚本出图 | **savefig+close** | 依赖弹窗 |

| A | B | 选 |
|---|---|-----|
| plot | scatter | 趋势 → plot；关系 → scatter |
| `"b-o"` | `color=`/`marker=` | 演示可用格式串；作业推荐关键字 |
| `plot(y)` | `plot(x,y)` | 横轴即 0..n-1 → 可只传 y；有业务 x → 必须两个 |

---

## 考研风例题

**例 1** · 一周销量折线（带标记 + 网格）

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

**例 2** · 广告费 vs 销量散点

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

**例 3** · 同图双折线 A/B

```python
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

x = [1, 2, 3, 4, 5]
plt.plot(x, [10, 11, 13, 12, 15], "b-o", label="A")
plt.plot(x, [9, 10, 10, 12, 13], "r--s", label="B")
plt.xlabel("Day")
plt.ylabel("Sales")
plt.title("A vs B")
plt.grid(True)
plt.legend()
plt.savefig("out/exam3_two.png")
plt.close()
```

---

## 三道练习与验收

**练习 1 · `plot_series(x, y, out_path) -> str`**  
等长折线（实线+圆点）；标签固定 `"x"`/`"y"`/`"series"`；`grid(True)`；保存后 close；返回 `out_path`。长度不等 → `ValueError`。  
**验收**：必须 `plot`；固定英文标签；文件存在且大小 > 0。

**练习 2 · `plot_scatter(x, y, out_path) -> str`**  
散点；标签 `"x"`/`"y"`/`"scatter"`；`grid(True)`；保存；返回路径。  
**验收**：必须 `scatter`（不得只用 plot 冒充）；长度校验。

**练习 3 · `plot_two_series(x, y1, y2, out_path) -> str`**  
蓝实线圆点 label `"A"`；红虚线方点 label `"B"`；标题 `"A vs B"`；必须 `legend()`。三者长度不全等 → `ValueError`。  
**验收**：双系列 + legend；禁止 seaborn。

题目全文与签名见本课目录 `homework.md`。标准答案约 **15:30** 写入 `homework/answers.ipynb`。

---

## 下节预告 · L07

Matplotlib 柱状 · 直方图 · 图例与保存（`bar` / `hist`、图例规范、`savefig` 参数）。
