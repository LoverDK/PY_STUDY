# L05 Pandas：缺失值、类型、分组与合并

对应考纲 **b**（数据进入分析软件后的预处理与基本分析）。L03 已会 `read_csv` / 选列 / 布尔过滤；L04 已会 NumPy 向量化。本课把表 **洗干净、按组汇总、多表拼起来**。

**今日只讲**：`isna`/`fillna`/`dropna`；`astype`（辅以 `to_numeric`）；`groupby`/`agg`；`merge`/`concat`。  
**明确不讲**：SQL 专题；多级索引深挖；`requests`；`pathlib`/`os`；seaborn；sklearn；类型标注；venv；迭代器协议。

**运行本课**：在 `L05/` 目录下 `python examples.py`（需已安装 pandas）。样例：`scores.csv`、`orders.csv`、`customers.csv`。

---

## 1. 是什么

| 概念 | 准确定义 | 一眼识别 |
|------|----------|----------|
| **缺失值** | 单元格「没有有效值」。读入后常见为 `NaN`（浮点空）或 `None`；空字符串有时也会被当成缺失 | `df.isna()` 为 True 的位置 |
| **dtype / astype** | 每列有一个类型（`int64`/`float64`/`object`/`string` 等）；`astype` 强制转换整列类型 | `df.dtypes`；`df["x"].astype(int)` |
| **groupby 对象** | 按一列（或多列）把行分成若干组，**尚未**立刻算出结果；挂上 `sum`/`mean`/`agg` 才出表 | `df.groupby("major")` 打印像分组描述 |
| **merge** | 按键列把两张表 **横向对齐拼接**（类似 SQL JOIN） | `pd.merge(left, right, on=...)` |
| **concat** | 把多张表 **沿轴堆叠**（默认上下叠行；也可左右拼列） | `pd.concat([df1, df2], axis=0)` |

```python
import pandas as pd

df = pd.read_csv("scores.csv", encoding="utf-8")
print(df.isna())          # 与 df 同形状的 True/False 表
print(df.dtypes)          # 各列类型；空分数字段常使 score 变成 float64
g = df.groupby("major")   # GroupBy 对象，还不是结果表
```

**NaN 从哪来**：CSV 里空字段、显式 `NA`/`NaN`、以及用 `None` 构造的 Series，读入或运算后常变成 `float` 列上的 `NaN`。注意：字符串 `"NA"` 是否被识别为缺失取决于读入参数；本课样例用的是真正的空字段。

---

## 2. 为什么（考纲与考法）

考纲 **b** 写「预处理、基本分析」。机考/评估常见问法：

- 统计每列缺失个数；把某列缺失填成 0 或列均值后再算平均  
- 丢掉「关键列为空」的行，再按专业 `groupby` 求平均分、人数  
- 学生表与成绩表按 `id` **左连接**，保留所有学生  
- 上下学期两张结构相同的表 `concat` 成一张再分析  
- 金额列读成了字符串，要转成数值再求和

卡分点几乎总是：`fillna` 写了但没接回赋值、`groupby` 后列名/索引搞不清、`merge` 键名不一致却硬 `on`、`how` 选错导致行数暴涨或丢行、`astype` 遇脏数据直接报错。

---

## 3. 怎么写（简 → 繁）

下列示例假设当前工作目录是 `L05/`。

### 3.1 检测缺失：`isna` / `isnull` / `notna`

`isna` 与 `isnull` **完全等价**（同一函数的别名）；`notna` 是其反面。

```python
import pandas as pd

df = pd.read_csv("scores.csv", encoding="utf-8")

print(df.isna())                 # 逐格 True/False
print(df["score"].isna())        # 单列：哪些行缺失
print(df.isna().sum())           # 每列缺失个数（对布尔按列求和）
print(df.isna().sum(axis=1))     # 每行缺失个数
print(df.notna().all(axis=1))    # 哪些行「完全没有缺失」
```

机考常要：「打印各列缺失数」→ `df.isna().sum()`；「筛出 score 非空的行」→ `df[df["score"].notna()]`。

### 3.2 处理缺失：`fillna` 与 `dropna`

**填充**（保留行，用某值顶上）：

```python
# 常数填充
filled0 = df["score"].fillna(0)

# 用列均值填充（先算均值再填；均值会自动跳过 NaN）
mean_score = df["score"].mean()
filled_mean = df["score"].fillna(mean_score)

# 前向填充：用「上一个非空值」往下填（时间序列题常见）
# 注意：新版 pandas 推荐 ffill()；fillna(method="ffill") 已逐步弃用
s = pd.Series([1.0, None, None, 4.0])
print(s.ffill())                 # 1.0, 1.0, 1.0, 4.0

# 整表：只填指定列
df2 = df.copy()
df2["score"] = df2["score"].fillna(0)
df2["credits"] = df2["credits"].fillna(df2["credits"].median())
```

**删除**（丢掉含缺失的行或列）：

```python
# 默认：任一格缺失就删整行
clean = df.dropna()

# how="all"：仅当「整行全空」才删
df.dropna(how="all")

# subset：只看这些列是否缺失
df.dropna(subset=["score"])           # score 为空的行删掉
df.dropna(subset=["score", "credits"], how="any")  # 两列任一空就删
```

**赋值提醒**：`fillna` / `dropna` 默认返回**新对象**，原 `df` 不变。必须写：

```python
df = df.dropna(subset=["score"])
# 或 df.dropna(subset=["score"], inplace=True)  —— 课上更推荐显式赋值，少用 inplace
```

### 3.3 类型转换：`astype`（及实用技巧 `to_numeric`）

```python
df = pd.read_csv("scores.csv", encoding="utf-8")

# 先去掉 score 缺失，才能稳妥转 int（有 NaN 的列不能变成普通 int64）
s = df["score"].dropna()
print(s.astype(int))              # float → int

# 整列转字符串
print(df["major"].astype(str))

# 构造脏数据演示：混合数字与脏字符
raw = pd.Series(["10", "20", "x", "30"])
# raw.astype(int)                 # 会 ValueError：无法解析 "x"

# 实用技巧（主体仍是 astype；脏数据时用这个兜底）：
num = pd.to_numeric(raw, errors="coerce")   # 无法解析的变成 NaN
print(num)                                  # 10, 20, NaN, 30
print(num.fillna(0).astype(int))            # 再填 0 后转 int
```

**为何有空值时分数列常是 float64**：整数类型一般不能存 NaN，pandas 会把该列提升为浮点。要「整数且允许缺失」需可空整数类型（如 `"Int64"`，大写 I），机考较少强求；通常流程是：**先处理缺失，再 `astype(int)`**。

### 3.4 分组：`groupby` + 聚合

```python
df = pd.read_csv("scores.csv", encoding="utf-8")
# 分析前常先处理缺失，避免均值被 NaN 干扰（mean 默认跳过 NaN，但 count 会变）
work = df.dropna(subset=["score"]).copy()

# 单列聚合：每个专业的平均分
print(work.groupby("major")["score"].mean())

# size：每组有多少行（含该组内其它列的缺失行也会计）
print(work.groupby("major").size())

# count：每组内「非缺失」的个数（按列）
print(work.groupby("major")["score"].count())

# agg：一次算多个指标；可对多列分别指定
print(
    work.groupby("major").agg(
        avg_score=("score", "mean"),
        n=("score", "count"),
        total_credits=("credits", "sum"),
    )
)

# 多列分组
print(work.groupby(["major"])["score"].agg(["mean", "min", "max"]))
```

`groupby` 之后默认把分组键放进 **索引**。若后面还要当普通列用（例如再 merge），加：

```python
result = work.groupby("major", as_index=False)["score"].mean()
# 或 .reset_index()
```

### 3.5 合并：`concat` 与 `merge`

**concat —— 堆叠**

```python
a = pd.DataFrame({"id": [1, 2], "v": [10, 20]})
b = pd.DataFrame({"id": [3, 4], "v": [30, 40]})

# 上下叠行（列名对齐；缺的列补 NaN）
print(pd.concat([a, b], axis=0, ignore_index=True))

# 左右拼列（按索引对齐）
c = pd.DataFrame({"w": [100, 200]})
print(pd.concat([a, c], axis=1))
```

`ignore_index=True` 会重建 0..n-1 行号，避免两张表原来都是 0,1 叠完出现重复索引。

**merge —— 按键对齐（JOIN）**

```python
customers = pd.read_csv("customers.csv", encoding="utf-8")
orders = pd.read_csv("orders.csv", encoding="utf-8")

# 内连接：两边键都匹配才保留
print(pd.merge(orders, customers, on="customer_id", how="inner"))

# 左连接：保留左表全部行；右表无匹配则右列 NaN
print(pd.merge(orders, customers, on="customer_id", how="left"))

# 外连接：两边键的并集
print(pd.merge(orders, customers, on="customer_id", how="outer"))

# 键名不同时：
# pd.merge(left, right, left_on="cid", right_on="customer_id", how="left")
```

| how | 保留谁 | 直觉 |
|-----|--------|------|
| `inner` | 两边都有的键 | 交集 |
| `left` | 左表全部 | 左为主，右来贴 |
| `right` | 右表全部 | 右为主 |
| `outer` | 两边键并集 | 并集，对不上的补 NaN |

---

## 4. 易错点（至少两个，含对照）

### 坑 1：`fillna` / `dropna` 链式写了但没赋值

```python
df = pd.read_csv("scores.csv", encoding="utf-8")

# 错：以为 df 已被填充；其实返回值被丢掉了
df["score"].fillna(0)
print(df["score"].isna().sum())   # 缺失数依旧 > 0

# 对：接回列，或整表赋值
df["score"] = df["score"].fillna(0)
# 或 df = df.fillna({"score": 0})
```

### 坑 2：`groupby` 后把索引当成普通列去选

```python
work = df.dropna(subset=["score"])
g = work.groupby("major")["score"].mean()
# g 是 Series，索引是 major
# 错：g["major"]  —— 没有这一列
# 对：g.index；或
g_df = work.groupby("major", as_index=False)["score"].mean()
print(g_df["major"])
```

### 坑 3：`merge` 一对多 / 多对多导致行数膨胀（笛卡尔积感）

```python
left = pd.DataFrame({"k": [1, 1], "a": ["x", "y"]})
right = pd.DataFrame({"k": [1, 1], "b": ["p", "q"]})
print(pd.merge(left, right, on="k"))
# 2×2 = 4 行！不是 2 行
# 考场若键不唯一，先 drop_duplicates 或确认业务是否允许多对多
```

### 坑 4：`concat` 后索引重复，再用 `loc[0]` 拿到多行

```python
a = pd.DataFrame({"v": [1, 2]})
b = pd.DataFrame({"v": [3, 4]})
c = pd.concat([a, b], axis=0)       # 索引：0,1,0,1
print(c.loc[0])                    # 两行，不是一行
c2 = pd.concat([a, b], ignore_index=True)
print(c2.loc[0])                   # 只有一行
```

### 坑 5：`astype` 遇脏数据直接崩

```python
raw = pd.Series(["10", "20", "x"])
# raw.astype(int)  → ValueError
safe = pd.to_numeric(raw, errors="coerce")  # 变 NaN 再决定 fillna / dropna
```

---

## 5. 何时用（对比）

| 需求 | 用 | 别用 |
|------|-----|------|
| 空值用常数/均值顶上，尽量保留行 | **fillna** / **ffill** | 一上来就 `dropna` 删光 |
| 某关键列为空的行不可信，直接丢掉 | **dropna(subset=...)** | 用 0 填关键列还拿去算均值（除非题面要求） |
| 按类别汇总（均值、求和、计数） | **groupby + agg** | 手写多层 for 扫 DataFrame |
| 两表按键对齐加列 | **merge** | 盲目 `concat(axis=1)`（那是按索引拼，不是按业务键） |
| 同结构多段数据上下接 | **concat(axis=0)** | 用 merge（没有「键连接」语义时别硬 JOIN） |

| A | B | 怎么选 |
|---|---|--------|
| `fillna(0)` | `dropna` | 题要「保留样本、空当 0」→ 填；题要「只分析完整记录」→ 删 |
| `groupby.size()` | `groupby(...)[col].count()` | size=组内行数；count=该列非缺失个数 |
| `merge(..., how="inner")` | `how="left"` | 只要两边都匹配 → inner；以左表名单为准 → left |
| `merge` | `concat(axis=1)` | 有业务键（id）→ merge；仅按行号左右贴 → concat |

---

## 6. 课堂例题（考研风）

**例 1** 读 `scores.csv`，将 `score` 缺失填为该列非缺失均值，再按 `major` 输出平均分（保留 2 位小数的 Series 即可在交互里查看；函数题见作业）。

```python
import pandas as pd

df = pd.read_csv("scores.csv", encoding="utf-8")
df["score"] = df["score"].fillna(df["score"].mean())
print(df.groupby("major")["score"].mean().round(2))
```

**例 2** 订单左连接客户；筛 `status == "paid"`，按 `city` 汇总 `amount` 之和（先把 amount 缺失当 0）。

```python
import pandas as pd

orders = pd.read_csv("orders.csv", encoding="utf-8")
customers = pd.read_csv("customers.csv", encoding="utf-8")
orders["amount"] = orders["amount"].fillna(0)
merged = pd.merge(orders, customers, on="customer_id", how="left")
paid = merged[merged["status"] == "paid"].copy()
paid["city"] = paid["city"].fillna("UNKNOWN")  # groupby 会丢掉键为 NaN 的组
print(paid.groupby("city", as_index=False)["amount"].sum())
```

---

## 下节预告

**L06**：基本分析与 Matplotlib 可视化（描述统计复习 + 折线/柱状/散点入门）。
