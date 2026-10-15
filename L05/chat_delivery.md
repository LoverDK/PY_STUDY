# 每日 DSBA-Python · L05

**Pandas：缺失值、类型、分组与合并**

对应考纲 **b**。L03 已会读表与过滤；L04 已会 NumPy。本课把表 **洗干净、按组汇总、多表拼起来**。  
**今日范围**：`isna`/`fillna`/`dropna`；`astype`（辅 `to_numeric`）；`groupby`/`agg`；`merge`/`concat`。  
**不讲**：SQL 专题；多级索引深挖；`requests`；`pathlib`/`os`；seaborn；sklearn。

---

## 今日目标

1. 会用 `isna`/`notna` 按列、按行统计缺失  
2. 会 `fillna`（常数/均值/前向）与 `dropna`（`how`/`subset`），并知道必须赋值接回  
3. 会 `astype`；脏数据会用 `pd.to_numeric(..., errors="coerce")` 兜底  
4. 会 `groupby` + `mean`/`sum`/`count`/`size`/`agg`；知道 `as_index=False`  
5. 会 `concat` 叠行与 `merge` 的 inner/left/outer；完成三道练习

---

## 详实讲解

### 1. 是什么

| 概念 | 定义 | 怎么看 |
|------|------|--------|
| **缺失值** | 无效空单元格，常见 `NaN`/`None` | `df.isna()` |
| **dtype / astype** | 列类型；强制转换 | `df.dtypes`；`.astype(...)` |
| **groupby** | 按键分组，挂聚合才出结果 | `df.groupby("major")` |
| **merge** | 按键横向 JOIN | `pd.merge(..., on=..., how=...)` |
| **concat** | 沿轴堆叠（默认上下叠行） | `pd.concat([...], axis=0)` |

```python
import pandas as pd
df = pd.read_csv("scores.csv", encoding="utf-8")
print(df.isna().sum())      # 每列缺失个数
g = df.groupby("major")     # 还不是结果表
```

空字段读入后，整数列常被提升为 **float64**（因为普通 int 存不了 NaN）。

### 2. 为什么

考纲 **b** 的预处理/基本分析在机考里经常落成：

- 各列缺失数；填 0 / 填均值后再平均  
- 丢关键列为空的行，再按专业汇总  
- 两表按 id **左连接**  
- 同结构表上下 `concat`  
- 金额列是字符串，转数值再求和

易扣分：`fillna` 未赋值、`groupby` 索引当列选、`merge` 键不唯一行数暴涨、`astype` 遇 `"x"` 直接崩。

### 3. 怎么写（简 → 繁）

**检测缺失**

```python
df.isna()                  # 同形状布尔表
df.isna().sum()            # 每列缺失数
df.isna().sum(axis=1)      # 每行缺失数
df[df["score"].notna()]    # 只留 score 非空
# isnull ≡ isna
```

**fillna / dropna**

```python
df["score"] = df["score"].fillna(0)
df["score"] = df["score"].fillna(df["score"].mean())
pd.Series([1.0, None, 4.0]).ffill()     # 前向填

df.dropna()                             # 任空删行
df.dropna(subset=["score"])             # 只看 score
df.dropna(how="all")                    # 全空才删
# 必须赋值：df = df.dropna(...) 或列接回
```

**astype**

```python
df["score"].dropna().astype(int)
# 脏数据：
pd.to_numeric(pd.Series(["10", "x"]), errors="coerce")  # → 10, NaN
```

**groupby**

```python
work = df.dropna(subset=["score"])
work.groupby("major")["score"].mean()
work.groupby("major").size()            # 组内行数
work.groupby("major")["score"].count()  # 非缺失个数
work.groupby("major").agg(
    avg_score=("score", "mean"),
    n=("score", "count"),
    total_credits=("credits", "sum"),
)
work.groupby("major", as_index=False)["score"].mean()
```

**concat / merge**

```python
pd.concat([a, b], axis=0, ignore_index=True)   # 上下叠，重建索引
pd.concat([a, c], axis=1)                      # 按索引左右贴

pd.merge(orders, customers, on="customer_id", how="inner")
pd.merge(orders, customers, on="customer_id", how="left")
pd.merge(orders, customers, on="customer_id", how="outer")
# 键名不同：left_on=..., right_on=...
```

| how | 含义 |
|-----|------|
| inner | 两边都有的键 |
| left | 保留左表全部 |
| outer | 键的并集 |

### 4. 易错点

| 错法 | 对法 |
|------|------|
| `df["score"].fillna(0)` 不接回 | `df["score"] = df["score"].fillna(0)` |
| `g = groupby...mean()` 后写 `g["major"]` | 用 `as_index=False` 或 `reset_index()` |
| 键不唯一就 merge，行数变成 4、8… | 先确认唯一性或 `drop_duplicates` |
| `concat` 后 `loc[0]` 拿到两行 | `ignore_index=True` |
| `Series(["10","x"]).astype(int)` | `to_numeric(..., errors="coerce")` 再处理 |

### 5. 何时用

| 需求 | 用 | 别用 |
|------|-----|------|
| 保留行、空当常数/均值 | fillna / ffill | 一上来全删 |
| 关键列空则整行不可信 | dropna(subset=...) | 盲目填 0 还拿去当真实分 |
| 按类汇总 | groupby + agg | 手写双重循环 |
| 按业务键拼表 | merge | 无键硬 concat(axis=1) |
| 同结构上下接 | concat(axis=0) | 硬 merge |

| A | B | 选 |
|---|---|-----|
| fillna | dropna | 要样本 → 填；要完整记录 → 删 |
| size | count | 行数 → size；某列非空数 → count |
| merge inner | left | 只要匹配上 → inner；以左名单为准 → left |

---

## 考研风例题

**例 1** · score 缺失填列均值，再按 major 看均分

```python
import pandas as pd
df = pd.read_csv("scores.csv", encoding="utf-8")
df["score"] = df["score"].fillna(df["score"].mean())
print(df.groupby("major")["score"].mean().round(2))
```

**例 2** · 订单左连客户；paid 按 city 汇总 amount（空金额当 0）

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

## 三道练习与验收

**练习 1 · `filled_score_mean(csv_path) -> float`**  
score 缺失填「填充前」列均值，返回填充后整列均值。  
样例：本课 `scores.csv` → 约 `68.8333`（误差 ≤ 1e-6）  
**验收**：必须 fillna 用列均值；返回 float。

**练习 2 · `major_stats(df) -> DataFrame`**  
先 `dropna(subset=["score"])`，再按 major 得到列 `major, avg_score, n, total_credits`。  
样例：计科 `avg_score=75.5`, `n=2`  
**验收**：必须 groupby+agg（或等价聚合）；列名齐全。

**练习 3 · `paid_amount_by_city(orders_csv, customers_csv) -> dict[str,float]`**  
amount 填 0；orders 左连 customers；只计 paid；按 city 求和；无城市 → `"UNKNOWN"`。  
样例：上海 120.5，北京 80.0，UNKNOWN 200.0  
**验收**：必须 left merge；禁止只用 concat 冒充按键合并。

题目全文与签名见本课目录 `homework.md`。标准答案约 **15:30** 写入 `homework/answers.ipynb`。

---

## 下节预告 · L06

基本分析与 Matplotlib 可视化（描述统计复习 + 折线 / 柱状 / 散点入门）。
