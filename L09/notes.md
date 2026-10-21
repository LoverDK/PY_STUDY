# L09 Pandas 多条件过滤与 loc/iloc 精熟

阶段：A · DSBA/Python/可视化/复杂度  
仓库路径：`L09/`

本课范围：布尔掩码、`& | ~`、`isin`、`between`、缺失值条件、`loc` 标签选择、`iloc` 位置选择，以及筛选后索引保留。  
本课不讲：`apply/map`（L10）、时间处理（L11）、复杂查询引擎、模型训练；计算机系统原理永不加入。

## 学习目标

1. 能把中文筛选要求拆成逐项布尔条件，再用正确括号组合。
2. 能解释为什么 Pandas 条件不能写成普通 Python 的 `and/or/not`。
3. 分清标签与位置：`loc` 看索引/列名，`iloc` 看第几个。
4. 掌握两类切片端点：`loc` 标签切片通常包含终点，`iloc` 遵循 Python 左闭右开。
5. 正确处理缺失布尔条件、筛选后的原索引、空结果和越界位置。

## 一、是什么：过滤是“每一行是否保留”的向量化判断

对 DataFrame 写：

```python
df["score"] >= 80
```

得到的不是单个 `True`，而是一列与 `df.index` 对齐的布尔值。每一行都有一个判断结果，这列结果称为布尔掩码。再写：

```python
df.loc[df["score"] >= 80, ["student", "score"]]
```

含义是：用掩码决定哪些行保留，再用列标签决定输出哪些列。

三个核心操作符：

- `&`：逐元素“且”；
- `|`：逐元素“或”；
- `~`：逐元素“非”。

每个比较条件都应单独加括号：

```python
mask = (
    (df["score"] >= 80)
    & (df["track"].isin(["Python", "SQL"]))
    & (df["minutes"].between(10, 30, inclusive="both"))
)
```

`between(10, 30, inclusive="both")` 包含 10 和 30；`isin([...])` 判断每个元素是否属于给定集合。它们的价值不只是缩短代码，还把业务口径直接写进表达式。

## 二、为什么：标签、位置和逻辑优先级是三套不同规则

### 1. 为什么不能用 `and/or`

Python 的 `and` 需要把左右对象各自判断成单个真假；Pandas Series 包含很多行，无法自动决定“整列到底算真还是假”。因此多条件筛选使用逐元素 `&`、`|`，并加括号。

错误：

```python
df[(df["score"] >= 80) and (df["minutes"] <= 30)]
```

正确：

```python
df[(df["score"] >= 80) & (df["minutes"] <= 30)]
```

### 2. 为什么要区分 `loc` 与 `iloc`

假设索引是 `[101, 205, 310]`：

- `df.loc[205]` 找标签为 205 的行；
- `df.iloc[1]` 找第二行；
- `df.loc[1]` 不是找第二行，若标签 1 不存在会报错。

即使索引恰好是 `0,1,2`，两者看起来相同，也不能混淆概念。排序、过滤、删除后，索引标签可能不再连续，但位置会按当前显示顺序从零计数。

### 3. 为什么切片终点不同

`loc["r2":"r4"]` 是标签切片，通常包含终点 `"r4"`；`iloc[1:4]` 是位置切片，只取位置 1、2、3。Pandas 官方索引指南明确区分了这两类规则：`loc` 主要基于标签，整数标签不是位置；标签切片的两端通常都包含。  
官方参考：https://pandas.pydata.org/docs/user_guide/indexing.html

## 三、怎么写：从题意到可验证结果

### 例题 1：三条件交集

```python
from io import StringIO
import pandas as pd

text = """student,track,score,minutes
s1,Python,78,25
s2,SQL,88,32
s3,Python,92,20
s4,C,85,28
s5,SQL,,18
s6,Python,88,30
"""

df = pd.read_csv(StringIO(text), index_col="student")

mask = (
    df["score"].notna()
    & (df["score"] >= 80)
    & df["track"].isin(["Python", "SQL"])
    & df["minutes"].between(20, 30, inclusive="both")
)

result = df.loc[mask, ["track", "score", "minutes"]]
print(result)
# s3 Python 92 20
# s6 Python 88 30
```

这里先用 `notna()` 明确排除缺失成绩。比较 `NaN >= 80` 通常已经得到 False，但显式写出缺失规则更利于审查，也避免以后换成可空布尔类型时语义变得含糊。

`between` 的边界 20 和 30 都被保留，因此 s3、s6 入选。筛选不会自动重排，结果保持原表相对顺序。

### 例题 2：“且”与“或”混合

要求：保留 Python 方向且成绩至少 85，或者 SQL 方向且用时不超过 20 分钟。

```python
mask = (
    ((df["track"] == "Python") & (df["score"] >= 85))
    | ((df["track"] == "SQL") & (df["minutes"] <= 20))
)
result = df.loc[mask, ["track", "score", "minutes"]]
```

括号体现业务分组：

```text
(Python 且 score>=85) 或 (SQL 且 minutes<=20)
```

若写成：

```python
(df["track"] == "Python") & (
    (df["score"] >= 85) | (df["track"] == "SQL")
) & (df["minutes"] <= 20)
```

就已经变成另一道题。最稳妥的方法是先把中文条件画成小分组，再翻译成表达式。

### 例题 3：同一张表上的标签与位置

```python
small = pd.DataFrame(
    {
        "track": ["Python", "SQL", "C", "Python"],
        "score": [78, 88, 85, 92],
        "minutes": [25, 32, 28, 20],
    },
    index=["r1", "r3", "r7", "r9"],
)

print(small.loc["r3":"r7", ["score", "minutes"]])
# 标签 r3、r7 均包含

print(small.iloc[1:3, 1:3])
# 位置第 2~3 行、位置第 2~3 列；终点 3 不包含
```

两段结果在这个例子中数值相同，但理由不同：

- `loc` 使用标签 `"r3":"r7"` 和列名；
- `iloc` 使用整数位置 `1:3`。

如果标签顺序不是按字典序排列，标签切片仍按当前索引中的起止位置截取，不会替你排序。若起止标签不存在或索引重复，行为需要额外检查；本课作业限定唯一索引。

### 例题 4：筛选后取前两行

```python
qualified = df.loc[df["score"] >= 80, ["track", "score"]]
first_two = qualified.iloc[:2]
```

先 `loc` 按业务条件筛选，再 `iloc` 取当前结果的前两行。此时 `first_two.index` 仍是原始学生标签，不会自动变成 0、1。

只有题目明确要求连续新索引时才调用：

```python
first_two.reset_index()
```

不要为了“看起来整齐”擅自重置，因为索引标签可能正是记录身份。

## 四、易错点：从报错到静默错答

1. **用 `and/or/not` 组合 Series。**  
   这通常直接报“Series 的真值不明确”。改为 `& | ~`，每个比较加括号。

2. **漏括号导致运算优先级错误。**  
   不要写 `df["score"] >= 80 & df["minutes"] <= 30`。应写 `(df["score"] >= 80) & (df["minutes"] <= 30)`。

3. **把整数标签当位置。**  
   `df.loc[5]` 是标签 5，不是第六行。要第六行用 `df.iloc[5]`。

4. **把两种切片都当左闭右开。**  
   `iloc[1:4]` 不含位置 4；`loc["a":"d"]` 通常含标签 d。做题前先标注“标签”还是“位置”。

5. **布尔掩码来自另一张表，索引没对齐。**  
   `loc` 使用标签语义；掩码的索引与目标表不一致时可能报错或产生非预期。最稳妥的是由同一 DataFrame 生成掩码，并在组合前检查 `mask.index.equals(df.index)`。

6. **用链式索引赋值。**  
   `df[df["score"]>=80]["level"]="high"` 可能不会可靠修改原表。若确实要赋值，应写 `df.loc[df["score"]>=80, "level"]="high"`。本课作业只读取，不要求修改。

7. **筛选后误以为索引自动连续。**  
   `iloc` 看结果当前位置，`loc` 看保留下来的原标签。除非接口要求，不要自动 `reset_index()`。

8. **忽略空结果与空位置列表。**  
   没有命中时返回列结构正确的空 DataFrame，而不是 `None`；位置列表为空时也应返回零行、指定列的结果。

## 五、何时用：选择工具的决策顺序

- 按业务条件选行：构造布尔掩码，再用 `loc[mask, columns]`。
- 按记录标签或列名选择：用 `loc`。
- 按“第几行、第几列”选择：用 `iloc`。
- 只判断单个标量：可以用 `at/iat`，但不在本课作业范围。
- 复杂条件先拆为命名掩码，便于逐项打印和测试；短条件也应保持括号清晰。

生产代码里，明确的 `loc/iloc` 比含义模糊的链式 `[]` 更容易审查。官方文档也将 `loc` 定义为主要按标签选择、也支持布尔数组，将 `iloc` 定义为按整数位置选择。  
官方参考：
- https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.loc.html
- https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.iloc.html

## 三道练习摘要

1. `filter_candidates`：成绩、方向、用时三条件筛选，验证边界、缺失和原顺序。
2. `select_label_block`：用 `loc` 按起止标签选闭区间，并限定输出列。
3. `take_positions`：用 `iloc` 按位置列表取行，支持负位置，禁止越界，保留原索引。

完整题面见 `homework.md`。开课时 `homework/answers.ipynb` 仅为占位，写明“约 9:30 写标准答案”，不代表答案已交付。

## 下节预告

L10 Pandas apply / map / 自定义列。
