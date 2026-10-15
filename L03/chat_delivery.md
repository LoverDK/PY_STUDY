# 每日 DSBA-Python · L03

**从文件到分析表：pandas 读入与表结构**

对应考纲 **b**（数据进入分析软件的入口）。语法快复结束，本课开始上库。  
**今日只讲**：`read_csv` / `read_json`，`head` / `info` / `describe`，列选取，布尔过滤。  
**明确不讲**：requests、pathlib/os、缺失值清洗（L05）、NumPy（L04）、seaborn、迭代器/类型标注/venv。  
示例数据在本课目录：`sales.csv`、`students.json`。

---

## 今日目标

1. 能把 CSV / JSON 读成 DataFrame，并说出 Series 与 DataFrame 的区别  
2. 用 `head` / `info` / `describe` / `shape` 快速摸底一张表  
3. 会选单列/多列；会写 `df[条件]`，组合条件用 `&` `|` 且加括号  
4. 完成三道机试风练习（见文末验收）

---

## 详实讲解

### 1. 是什么

| 对象 | 是什么 | 怎么得到 |
|------|--------|----------|
| **Series** | 一维带标签序列（「带索引的一列」） | `df["score"]` |
| **DataFrame** | 二维表：行 × 列 | `pd.read_csv` / `pd.read_json` |

```python
import pandas as pd
df = pd.read_csv("sales.csv", encoding="utf-8")   # → DataFrame
s = df["revenue"]                                 # → Series
```

读入时常用参数（机考偶尔考）：

| 参数 | 作用 | 例 |
|------|------|----|
| `encoding` | 编码 | `"utf-8"`（中文建议显式写） |
| `sep` | 分隔符 | 默认 `,`；制表符 `"\t"` |
| `header` | 列名行 | 无列名时 `header=None` |
| `usecols` | 只读部分列 | `usecols=["name","score"]` |

JSON 本课用 **对象数组** `[{...},{...}]`，`read_json` 后键变列名。

### 2. 为什么

考纲 **b** 要求数据能进分析软件并做预处理/分析。机考常见：

- 读表 → 打印行数/某列最大/前几行  
- `score >= 60` 筛行，再只留 `name`、`score`  
- JSON 里按专业 + 分数组合条件  

卡分点多半是：路径/编码、`and` 误用、单列多列括号。

### 3. 怎么写（简 → 繁）

**摸底**

```python
df = pd.read_csv("sales.csv", encoding="utf-8")
print(df.shape)      # (行, 列)
print(df.head())     # 前 5 行
print(df.info())     # 非空与 dtype
print(df.describe()) # 数值列分布
```

**列选取**

```python
stu = pd.read_json("students.json", encoding="utf-8")
stu["score"]                 # Series
stu[["name", "score"]]       # DataFrame（双层括号）
```

**布尔过滤**

```python
stu[stu["score"] >= 60]
stu[(stu["major"] == "统计") & (stu["score"] > 80)]   # 且
stu[(stu["major"] == "金融") | (stu["score"] < 60)]   # 或
stu.loc[stu["score"] >= 60, ["name", "score"]]        # 筛行+选列
```

**一条小流程**

```python
sales = pd.read_csv("sales.csv", encoding="utf-8")
mask = (sales["region"] == "华东") & (sales["revenue"] >= 5000)
print(sales.loc[mask, ["date", "product", "revenue"]])
```

### 4. 易错点（对照）

**坑 A：`and`/`or` 与缺括号**

```python
# 错
# stu[stu["score"] >= 60 and stu["major"] == "统计"]
# stu[stu["score"] >= 60 & stu["major"] == "统计"]

# 对
stu[(stu["score"] >= 60) & (stu["major"] == "统计")]
```

**坑 B：多列少一层括号**

```python
# 错 → KeyError
# stu["name", "score"]

# 对
stu[["name", "score"]]
```

另：改表时少用链式赋值，优先 `stu.loc[条件, "列"] = 值`（L05 会更多用到）。中文 CSV 记得 `encoding="utf-8"`，并在 `L03/` 目录运行以免找不到文件。

### 5. 何时用

| 需求 | 用 | 别用 |
|------|-----|------|
| 多列异构表 + 条件筛行 | DataFrame | 多层 for + 手拼 dict |
| 几个数算均值 | list / 下节 NumPy | 为几个数建表 |
| 规范 CSV/JSON 表 | `read_csv` / `read_json` | 自己 `split(",")`（除非禁库） |
| 单条配置 | dict | DataFrame |

---

## 考研风例题

**例 1**：读 `sales.csv`，打印行数与 `revenue` 最大值。

```python
import pandas as pd
df = pd.read_csv("sales.csv", encoding="utf-8")
print(df.shape[0])
print(int(df["revenue"].max()))
# 本课数据 → 10 与 35988
```

**例 2**：读 `students.json`，大数据专业且及格，按分数降序打印姓名。

```python
stu = pd.read_json("students.json", encoding="utf-8")
sub = stu[(stu["score"] >= 60) & (stu["major"] == "大数据")]
sub = sub.sort_values("score", ascending=False)
for name in sub["name"]:
    print(name)
# → 周八 / 李四
```

---

## 练习 + 验收（3 道）

完整题面在 `homework.md`。摘要：

1. **`sales_overview(csv_path) -> (nrows, ncols, revenue_max)`**  
   样例：`sales_overview("sales.csv")` → `(10, 5, 35988)`  
   **验收**：必须 `read_csv`；不得写死常数。

2. **`passed_names(json_path) -> list[str]`**  
   `score >= 60`，按分数降序的姓名。  
   样例 → `['周八', '张三', '陈一', '孙七', '李四', '赵五']`  
   **验收**：须布尔过滤；顺序一致；不含王二、钱六。

3. **`high_revenue_products(csv_path, region, threshold) -> list[str]`**  
   区域且 `revenue >= threshold` 的 `product`，保持原行序。  
   `high_revenue_products("sales.csv", "华东", 5000)` → `['笔记本', '键盘']`  
   **验收**：两条件都用；华北+10000 → `['笔记本']`。

请先做题；标准答案约 **15:30** 写入 `homework/answers.ipynb`。

运行课堂示例：在 `L03/` 下执行 `python examples.py`。

---

**下节预告 · L04 NumPy：数组、索引、广播与统计汇总**  
（仍属考纲 b；为向量化统计和与 pandas 列运算打底。）
