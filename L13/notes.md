# L13 NumPy+Pandas 联用小卷（读表→数组统计）

## 课程定位

- **阶段**：A — DSBA / Python / 可视化 / 复杂度
- **主线**：用 Pandas 完成“读表、检查、选列”，再用 NumPy 完成“数组化、按轴统计、条件统计”
- **范围**：CSV 读取、数据类型与缺失值检查、`DataFrame.to_numpy`、`axis`、布尔掩码、`nan*` 统计、结果回填
- **本课不讲**：数据库、机器学习建模、复杂 Excel 清洗、计算机系统原理

## 学习目标

完成本课后，你应能：

1. 把 CSV 安全读成 DataFrame，并先检查形状、列名、类型、缺失值与唯一键。
2. 明确 Pandas 与 NumPy 的职责边界，知道何时保留标签，何时转换为数组。
3. 用 `axis=0` 和 `axis=1` 分别完成“按列”和“按行”统计。
4. 正确处理缺失值、布尔条件与分母，避免静默地产生错误结论。
5. 把数组统计结果重新对齐到原表，输出可核对的分析结果。

---

## 第一段：读表不是“读进来就算完”

### 是什么

`pandas.read_csv` 把二维文本表读成 DataFrame。DataFrame 同时保存值、列名、行索引和数据类型，适合承担数据入口与结构检查。

### 为什么

真实数据最危险的问题往往不是公式错，而是输入错：列名拼错、数字被读成字符串、主键重复、分数越界、关键列缺失。若不先验证，后面的平均值即使代码能运行，也可能没有业务意义。

### 怎么写

```python
from pathlib import Path
import pandas as pd

csv_path = Path(__file__).parent / "data" / "scores.csv"
df = pd.read_csv(csv_path)

required = {"student_id", "name", "midterm", "final"}
missing = required - set(df.columns)
if missing:
    raise ValueError(f"缺少列: {sorted(missing)}")

if df["student_id"].duplicated().any():
    raise ValueError("student_id 必须唯一")
```

随后检查：

```python
print(df.shape)
print(df.dtypes)
print(df.isna().sum())
print(df.head())
```

### 易错点

1. **直接依赖当前工作目录**：写 `pd.read_csv("data/scores.csv")` 时，从别的目录执行脚本可能找不到文件。应从 `__file__` 定位课程目录。
2. **把 `object` 当成可计算数字**：一列只要混入“缺考”等文本，就可能无法正确求均值。应使用 `pd.to_numeric(..., errors="coerce")` 后检查新产生的缺失值。
3. **只检查总行数，不检查主键**：重复学生会被统计两次，使平均分和通过率偏移。

### 何时用

所有“文件 → 分析”任务都应把结构检查放在第一步，尤其是自动报表、多人维护的数据文件和考试机试题。

---

## 第二段：Pandas 管标签，NumPy 管密集数值计算

### 是什么

Pandas 的强项是按列名选取、对齐和清洗；NumPy 的强项是同类型数组上的向量化计算。二者联用的关键接口是 `DataFrame.to_numpy`。

```python
score_cols = ["quiz", "midterm", "final"]
scores = df[score_cols].to_numpy(dtype=float, copy=True)
```

此时 `scores.shape == (学生数, 3)`：每一行是一名学生，每一列是一项考试。

### 为什么

在 DataFrame 中选列能显式表达业务含义；转成数组后，按轴求和、广播权重、布尔筛选等数值操作更直接。先选列再转换还能防止姓名等文本列混入数值矩阵。

### 怎么写

若三项权重为 20%、30%、50%：

```python
weights = np.array([0.2, 0.3, 0.5])
weighted = scores @ weights
```

矩阵乘法把每行与权重向量做点积，返回每名学生一个综合分。结果长度与 DataFrame 行数相同，可以安全回填：

```python
result = df.copy()
result["weighted_score"] = np.round(weighted, 2)
```

### 易错点

1. **整张表直接 `to_numpy`**：姓名与数字混合时数组常退化为 `object`，数值运算变慢或报错。
2. **权重顺序与列顺序不一致**：数学上能运行，但含义完全错。权重必须与 `score_cols` 一一对应。
3. **误以为转换总会复制**：某些情况下数组可能共享底层数据。需要隔离修改时明确写 `copy=True`，并且不要修改原表视图。

### 何时用

当计算主要是规则整齐的数值矩阵操作时使用 NumPy；当任务依赖列名、分组键、时间索引或连接关系时留在 Pandas。

---

## 第三段：axis 决定“沿哪个方向消去”

### 是什么

二维数组形状为 `(n_rows, n_cols)`。聚合会消去指定轴：

- `axis=0`：消去行轴，保留每一列的结果，即“各考试在所有学生中的统计”。
- `axis=1`：消去列轴，保留每一行的结果，即“每名学生跨考试的统计”。

```python
exam_mean = np.nanmean(scores, axis=0)     # 长度 3
student_mean = np.nanmean(scores, axis=1)  # 长度为学生数
```

### 为什么

“按行还是按列”是二维统计中最高频的错误源。不要死背横竖，而要先写清楚输入形状与期望输出长度，再决定轴。

### 怎么写

设 `scores.shape == (8, 3)`：

- 想得到 3 个考试均值，输出形状应为 `(3,)`，所以消去 8 名学生所在的第 0 轴。
- 想得到 8 个学生均值，输出形状应为 `(8,)`，所以消去 3 门考试所在的第 1 轴。

调试时用断言锁定语义：

```python
assert exam_mean.shape == (len(score_cols),)
assert student_mean.shape == (len(df),)
```

### 易错点

1. **把 `axis=0` 理解成“取第 0 行”**：axis 是聚合方向，不是索引位置。
2. **统计结果和标签错配**：长度都是 3 也可能把 `final` 的均值标成 `quiz`。结果标签必须沿用同一份 `score_cols`。
3. **忽略全缺失切片**：`np.nanmean` 遇到整行或整列全为 NaN 会产生 NaN 并警告，业务上应单独判断。

### 何时用

任何二维指标表、传感器矩阵、图片通道或批量样本统计都需要先明确轴语义。

---

## 第四段：缺失值与布尔掩码必须定义业务口径

### 是什么

NumPy 用 `np.nan` 表示浮点缺失值。`np.mean` 会让 NaN 传播；`np.nanmean` 忽略 NaN。布尔掩码则用 True/False 指定参与计算的元素或行。

```python
valid_final = ~np.isnan(scores[:, 2])
final_pass = scores[:, 2] >= 60
pass_rate = final_pass[valid_final].mean()
```

### 为什么

“缺考算不及格”与“缺考不进入分母”会得到不同通过率。函数选择只是实现，统计口径必须先写出来。本课示例规定：单项均值忽略缺失；期末通过率只在实际参加期末考试的人中计算。

### 怎么写

先建立有效样本掩码，再建立业务条件：

```python
final_scores = scores[:, 2]
valid = ~np.isnan(final_scores)
if valid.sum() == 0:
    pass_rate = float("nan")
else:
    pass_rate = np.mean(final_scores[valid] >= 60)
```

若要找“期末比期中至少提高 10 分”的学生：

```python
mid = scores[:, 1]
final = scores[:, 2]
improved = (~np.isnan(mid)) & (~np.isnan(final)) & ((final - mid) >= 10)
names = df.loc[improved, "name"].tolist()
```

### 易错点

1. **直接写 `(final_scores >= 60).mean()`**：NaN 与 60 比较得到 False，于是缺考被暗中计为未通过。
2. **用 Python 的 `and` 连接数组条件**：数组必须逐元素使用 `&`，并给每个比较加括号。
3. **分母为零仍相除**：全员缺考时需明确返回 NaN、0 或报错，不能任由除零结果进入报表。

### 何时用

通过率、异常筛选、满足多条件的名单、缺测传感器数据等任务都要用掩码明确有效样本与业务条件。

---

## 第五段：结果回填、排序与可复核输出

### 是什么

数组计算完成后，将与行一一对应的结果作为新列写入 DataFrame；将与列一一对应的结果构造成带标签的 Series。最终输出应保留标识列，使人能够追溯。

```python
result = df.copy()
result["average"] = np.round(np.nanmean(scores, axis=1), 2)
ranking = result.sort_values(
    ["average", "student_id"],
    ascending=[False, True],
    kind="mergesort",
)
```

### 为什么

裸数组 `[83.2, 76.5, ...]` 离开上下文后不可读。回填到带学生编号和姓名的表中，才构成可审计结果。并列时增加稳定的第二排序键，可以让结果每次一致。

### 怎么写

输出前做三类验收：

1. **形状验收**：新列长度等于原表行数。
2. **范围验收**：分数在 0–100，通过率在 0–1 或 0%–100%。
3. **守恒验收**：分析函数不修改输入表；排序后学生集合不变。

```python
assert len(result) == len(df)
assert result["student_id"].is_unique
assert set(result["student_id"]) == set(df["student_id"])
```

### 易错点

1. **先排序数组、后按原索引回填**：行顺序变化会导致成绩与学生错位。应先回填再整体排序，或显式携带索引。
2. **覆盖原始列**：把清洗或计算值直接写回原列，失去审计依据。优先创建副本和新列。
3. **浮点数直接判断相等**：验收计算结果时使用 `np.isclose`，展示时再 `round`。

### 何时用

排行榜、质量报表、成绩分析、运营指标导出等需要“机器可算、人能复核”的场景。

---

## 综合例题

读取 `data/scores.csv`，回答：

1. 三项考试各自均值是多少？
2. 每名学生按 20%/30%/50% 的加权分是多少？
3. 参加期末考试的学生中，通过率是多少？
4. 哪些学生期末较期中提高至少 10 分？

解题流程：

```text
读表 → 校验列/类型/主键/范围 → 选数值列 → to_numpy
→ 按 axis 统计 → 用掩码确定有效分母 → 回填标签 → 排序与断言
```

完整实现见 `examples.py`。

## 本课检查清单

- [ ] 是否先写清输入形状和输出形状？
- [ ] 是否只转换需要计算的数值列？
- [ ] 权重顺序是否与列顺序一致？
- [ ] 缺失值是否有明确业务口径？
- [ ] 布尔条件是否使用 `&` / `|` 和括号？
- [ ] 结果是否保留 student_id 等追溯字段？
- [ ] 是否用断言核对行数、唯一键和数值范围？

## 下节预告

**L14 算法复杂度入门：大 O 与常见对照**：学习如何估算程序随输入规模增长的时间与空间代价。