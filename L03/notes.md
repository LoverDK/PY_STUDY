# L03 从文件到分析表：pandas 读入与表结构

**对应考纲**：复旦管院 DS&BA / QFFE Python **b**  
（「数据从服务器端到分析软件的预处理、基本分析与可视化」——本课只打通「文件 → DataFrame → 初探与筛选」）

**定位**：语法快复结束，开始上库。本课是 pandas 入门：读 CSV/JSON、看表结构、选列、布尔过滤。  
**下节**：L04 NumPy（数组、广播、统计汇总）。完整清洗（缺失值/类型/分组合并）在 L05。

**明确不讲**：`requests`；`pathlib`/`os`；`isna`/`fillna`/`dropna`（L05）；NumPy（L04）；seaborn；`itertools`/`collections`；迭代器协议；类型标注；venv。  
`json`/`csv` 仅作为 pandas 能读入的数据格式出现，不单独开标准库专题。

**运行本课**：在 `L03/` 目录下 `pip install pandas`（若尚未安装），再 `python examples.py`。示例数据：`sales.csv`、`students.json`。

---

## 1. 是什么

### 1.1 pandas 在考纲 b 里扮演什么角色

官方写「分析软件」。Python 机考语境下，把表格式数据读进内存、做列运算与筛选，核心工具就是 **pandas**。本课先解决：

1. 磁盘上的 CSV / JSON → 内存里的表（DataFrame）
2. 快速摸清表有多大、有哪些列、数值列大致分布
3. 取出需要的列，按条件筛出行

### 1.2 两个核心对象

| 对象 | 直观理解 | 常见来源 |
|------|----------|----------|
| **Series** | 一维带标签的序列（像「带索引的一列」） | `df["score"]`；`pd.Series([...])` |
| **DataFrame** | 二维表：行 × 列；每列通常是一个 Series | `pd.read_csv(...)`；`pd.read_json(...)` |

可以把 DataFrame 想成「带列名的 Excel 工作表」，但操作是代码化的：选列、过滤、汇总都写成表达式，便于复现与机考评分。

```python
import pandas as pd

s = pd.Series([88, 57, 92], index=["陈一", "王二", "张三"], name="score")
# s 是 Series：索引是姓名，值是分数

df = pd.DataFrame({
    "name": ["陈一", "王二", "张三"],
    "score": [88, 57, 92],
})
# df 是 DataFrame：两列 name、score；默认行索引 0,1,2
```

### 1.3 读入函数（本课必会）

| 函数 | 读什么 | 典型结果 |
|------|--------|----------|
| `pd.read_csv(path)` | 逗号（或其它分隔符）分隔的文本表 | DataFrame |
| `pd.read_json(path)` | JSON（常见：对象数组 `[{...},{...}]`） | DataFrame |

常见关键字（机考偶尔考到，建议会用）：

| 参数 | 作用 | 例 |
|------|------|----|
| `encoding` | 文本编码 | `encoding="utf-8"`（中文 CSV 强烈建议显式写出） |
| `sep` | 字段分隔符 | 默认 `,`；若是制表符：`sep="\t"` |
| `header` | 哪一行当列名 | 默认第一行；没有列名时 `header=None` |
| `usecols` | 只读指定列 | `usecols=["name", "score"]`（省内存、题面只要两列时好用） |

---

## 2. 为什么（考纲与出题方式）

- **考纲点**：b —— 数据进入分析软件后的预处理入口。不先把表读对，后面的清洗、分组、画图都无从谈起。
- **考场常见问法**：
  1. 给定 `xxx.csv`，读入后打印前 5 行 / 行数列数 / 某列均值
  2. 选出 `score >= 60` 的行，再只保留 `name` 与 `score` 两列
  3. 读 JSON 数组，筛出 `major == "统计"` 且 `score > 80`
- **评分点往往卡在**：路径写错、忘了 `encoding`、布尔条件用了 Python 的 `and`/`or`（见易错点）、单列双括号搞混。

本课目标：拿到一份小表，**10 分钟内**能读入、摸底、按条件筛出结果表。

---

## 3. 怎么写（由简到繁）

下列示例假设当前工作目录是 `L03/`（与 `examples.py` 一致）。路径用相对路径：`sales.csv`、`students.json`。

### 3.1 读 CSV，并快速摸底

```python
import pandas as pd

df = pd.read_csv("sales.csv", encoding="utf-8")

print(df.shape)       # (行数, 列数)，如 (10, 5)
print(df.columns)     # Index(['date', 'region', 'product', 'units', 'revenue'], ...)
print(df.dtypes)      # 各列类型：object / int64 / float64 等
print(df.head())      # 默认前 5 行；df.head(3) 前 3 行
print(df.info())      # 非空计数、dtype、内存占用（机考「看一眼表」很有用）
print(df.describe())  # 数值列的 count/mean/std/min/四分位/max
```

**读结果时注意**：

- `head` 看「长什么样」；`info` 看「有没有空、类型对不对」；`describe` 看「数值列数量级是否离谱」。
- `shape[0]` 是行数，`shape[1]` 是列数；不要和 `len(df.columns)` 搞混用途——两者都能拿列数，但 `shape` 一次给出行列。

### 3.2 读 JSON（对象数组 → 表）

```python
stu = pd.read_json("students.json", encoding="utf-8")
print(stu.head())
print(stu.columns.tolist())  # ['sid', 'name', 'major', 'score', 'passed']
```

本课的 `students.json` 是 **JSON 数组**，每个元素是一行对象。pandas 会自动把键变成列名。  
（若将来遇到「一个大对象里嵌套列表」的 JSON，可能要指定 `orient`；机考小数据多数是数组形式，本课不展开。）

### 3.3 列选取

```python
# 单列 → Series
scores = stu["score"]
print(type(scores))          # <class 'pandas.core.series.Series'>
print(scores.mean())         # 列均值，后面 L05 会更多汇总

# 多列 → DataFrame（注意双层方括号）
sub = stu[["name", "score"]]
print(type(sub))             # DataFrame

# 只要部分列读入（考场表很大时）
df2 = pd.read_csv("sales.csv", encoding="utf-8", usecols=["region", "revenue"])
```

**记忆**：

- `df["col"]` → 一列（Series）
- `df[["col"]]` → 仍是 DataFrame，但只有一列
- `df[["a", "b"]]` → 多列 DataFrame

### 3.4 布尔过滤（筛选行）

核心句式：`df[条件]`，其中「条件」是与行数等长的布尔 Series。

```python
# 及格学生
passed = stu[stu["score"] >= 60]
print(passed)

# 统计专业且分数 > 80
hi_stat = stu[(stu["major"] == "统计") & (stu["score"] > 80)]
print(hi_stat)

# 金融 或 分数 < 60（挂科关注）
watch = stu[(stu["major"] == "金融") | (stu["score"] < 60)]
print(watch)

# 先筛行，再选列（机考高频组合）
out = stu[stu["score"] >= 60][["name", "score"]]
print(out)
```

**组合条件必须用 `&` / `|`，且每个比较两边加括号**：

```python
# 正确
stu[(stu["score"] >= 60) & (stu["major"] == "统计")]

# 错误示范见下一节
```

### 3.5 需要时用 loc / iloc（点到为止）

本课不做索引深挖；只为过滤后「按标签/位置取」时不至于懵：

```python
# loc：按标签（列名、索引标签）
print(stu.loc[stu["score"] >= 90, ["name", "score"]])

# iloc：按整数位置（第 0 行、前两列）
print(stu.iloc[0, 0])
print(stu.iloc[0:3, 0:2])   # 前 3 行、前 2 列
```

机考多数题用 `df[布尔]` + `[["列A","列B"]]` 就够；`loc` 在「条件 + 列清单」写在一起时更清晰。

### 3.6 一条「读入 → 摸底 → 筛选 → 输出」小流程

```python
import pandas as pd

sales = pd.read_csv("sales.csv", encoding="utf-8")
print("shape:", sales.shape)
print(sales.head(3))

# 华东地区、销售额 >= 5000 的记录，只看 date / product / revenue
mask = (sales["region"] == "华东") & (sales["revenue"] >= 5000)
result = sales.loc[mask, ["date", "product", "revenue"]]
print(result)
```

---

## 4. 易错点（至少 2 个，含正误对照）

### 坑 1：布尔组合误用 `and` / `or`

Python 的 `and`/`or` 不能直接作用在 Series 上。pandas 要求逐元素的 `&` / `|`，并且 **比较表达式要加括号**（因为 `|` `&` 优先级低于比较运算）。

```python
# 错误：TypeError 或逻辑完全不对
# stu[stu["score"] >= 60 and stu["major"] == "统计"]
# stu[stu["score"] >= 60 & stu["major"] == "统计"]  # 缺括号时运算顺序错乱

# 正确
stu[(stu["score"] >= 60) & (stu["major"] == "统计")]
```

### 坑 2：单列 / 多列方括号搞混

```python
# 错误：KeyError —— pandas 会把 ["name", "score"] 当成「某一个叫这个名字的列」
# stu["name", "score"]

# 正确：多列用双层括号
stu[["name", "score"]]
```

### 坑 3（加分提醒）：过滤后的「视图」与链式赋值

初学机考少考，但改表时常见警告：

```python
# 不推荐：链式取列再改，可能只改了副本
# stu[stu["score"] < 60]["passed"] = False

# 更稳：用 loc 一次写清行与列
stu.loc[stu["score"] < 60, "passed"] = False
```

本课作业以「筛选后打印/返回」为主，少做原地修改；养成 `loc` 习惯有利于 L05。

### 坑 4：路径与编码

```python
# 若在错误目录运行：FileNotFoundError
# 解决：cd 到 L03/ 再运行；或写清相对/绝对路径

# 中文乱码或 UnicodeDecodeError：显式 encoding="utf-8"
pd.read_csv("sales.csv", encoding="utf-8")
```

---

## 5. 何时用（对比表）

| 需求 | 更合适 | 不太合适 |
|------|--------|----------|
| 表格数据（多列异构：字符串+数值） | pandas DataFrame | 纯 `list[list]` 手写下标 |
| 只要几个数字做均值方差 | 列表 / 稍后 NumPy | 为几个数专门建 DataFrame |
| 「按条件筛行 + 选列」 | `df[mask][cols]` 或 `df.loc[mask, cols]` | 多层 `for` + 手工拼字典 |
| 键值对配置、单条记录 | `dict` | DataFrame（杀鸡用牛刀） |
| 文件是规范 CSV/JSON 表 | `read_csv` / `read_json` | 自己 `split(",")` 除非题面禁止库 |

**一句话**：有「列名 + 多行记录 + 条件筛选」→ 优先 pandas；纯算法小题（阶乘、递归）→ 继续用基础语法，不必硬上表。

---

## 6. 考研风例题（课堂演示）

### 例 1：读 CSV，输出行数与 `revenue` 列最大值

**题意**：读取 `sales.csv`，打印两行：第一行列数无关，按样例打印「行数」和「revenue 最大值」。

```python
import pandas as pd

df = pd.read_csv("sales.csv", encoding="utf-8")
print(df.shape[0])
print(int(df["revenue"].max()))
```

**样例输出（与本课数据一致）**：
```text
10
35988
```

### 例 2：读 JSON，筛出及格且专业为「大数据」的姓名，按分数降序

```python
import pandas as pd

stu = pd.read_json("students.json", encoding="utf-8")
sub = stu[(stu["score"] >= 60) & (stu["major"] == "大数据")]
sub = sub.sort_values("score", ascending=False)
for name in sub["name"]:
    print(name)
```

**样例输出**：
```text
周八
李四
```

（`sort_values` 本课仅作小工具；系统排序/分组在 L05。）

---

## 7. 练习与验收

见同目录 `homework.md`（三道，含样例 I/O 与硬性验收）。  
答案约 15:30 写入 `homework/answers.ipynb`——请先独立完成。

**下节预告 · L04**：NumPy 数组创建、索引切片、广播、`mean`/`sum`/`std` 与布尔索引；仍对应考纲 **b**，为后面和 pandas 列运算打底。
