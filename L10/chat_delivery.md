# L10 Pandas apply / map / 自定义列

阶段 A：DSBA/Python/可视化/复杂度。仓库路径：L10/。
范围：Series.map 字典与函数映射、Series.apply 的标量函数、DataFrame.apply(axis=0/1)、向量化自定义列、assign、缺失与未知值、索引对齐和输入不变。
不讲：时间与排序去重（L11）、复杂分组转换、JIT/并行优化、完整特征工程或模型训练；不含计算机系统原理。

## 今日目标
能按输入粒度选工具；会写单值函数并正确传给 map/apply；能解释 axis=1 传入的是行、axis=0 传入的是列；能创建新列而保留行索引与顺序；能用断言核对阈值边界、缺失和未知类别。

## 一、是什么：把“处理一个值/一行”的规则应用到表

自定义列是从已有数据按明确规则计算出的新列，例如原价减优惠得到实付金额，课程代码转名称，成绩映射等级。新列不仅要数值正确，还要落在正确的记录上。

本课的对象必须说全：
- Series.map(dict)：用字典把一列中的每个值映射到目标值。
- Series.map(function)：对一列的单个元素应用函数。
- Series.apply(function)：本课仅讨论普通标量函数的逐元素用法，不能据此推断所有 apply 模式都相同。
- DataFrame.apply(function,axis=0)：默认逐列，函数收到一列 Series。
- DataFrame.apply(function,axis=1)：逐行，函数收到一行 Series。
- 向量化表达式：整列算术、比较与字符串方法，如 df["price"]*df["qty"]。
- assign：返回带新列的 DataFrame，用关键字指定列；可接收基于当前表的 callable。

同名方法在不同对象上语义可能不同。不要把 Series.map 与 DataFrame.map 混为一谈，本课 map 均明确指 Series.map。

## 二、为什么：选择粒度决定正确性与可读性

若规则只是单列字典查表，map 表达最直接；若是简单算术，整列运算更简洁；跨多列且有复杂业务分支时，逐行 apply 可以把规则组织成独立函数。apply 不是自动加速器，逐行调用 Python 函数通常有额外开销；能清楚表达的向量化计算应优先考虑，但不宣称任何数据规模下都一定更快。

先写清三个问题：输入是什么、缺失怎么办、输出类型是什么。
例：成绩 None 是“未提供”，并不是“不及格”；代码 X 是“未知类别”，与缺失代码不同。把它们都 fillna("Other") 会丢失信息。某题允许这样合并时可以做，题目要求区分时就不能做。

创建新列前也要想好是否允许改输入。课堂函数和本课作业约定返回新表，使用 copy 或 assign；函数内部避免悄悄修改调用者的表。

## 三、怎么写：从单列映射到跨列计算

### 例题1：字典映射与未知键
```python
import pandas as pd

codes = pd.Series(["PY","SQL","X",None], index=["s1","s2","s3","s4"], dtype="object")
names = codes.map({"PY":"Python","SQL":"SQL"})
print(names)
# s1 Python；s2 SQL；s3/s4 为缺失
```
普通字典未包含的键映射为缺失。这意味着仅看结果的缺失，无法区分“原数据缺失”与“字典没有这个键”。若业务必须区分，要在函数中先判缺失，再查表：
```python
mapping = {"PY":"Python","SQL":"SQL"}
def course_name(value):
    if pd.isna(value):
        return "Missing"
    return mapping.get(value, "Unknown")

print(codes.map(course_name).tolist())
# ["Python","SQL","Unknown","Missing"]
```
注意传 course_name，不要写 course_name()；前者是函数，后者会立即调用且这里缺少参数。na_action="ignore" 可跳过缺失输入，但那样缺失会保留下来，不会自动变成 "Missing"。缺失的业务替代值仍要由你明确决定。

### 例题2：单值规则与阈值顺序
```python
def grade(value):
    if pd.isna(value):
        return "Missing"
    if value >= 90:
        return "Excellent"
    if value >= 60:
        return "Pass"
    return "Fail"

scores = pd.Series([59,60,89,90,None], dtype="float64")
print(scores.map(grade).tolist())
print(scores.apply(grade).tolist())
# 两者在本例均为 ["Fail","Pass","Pass","Excellent","Missing"]
```
先判断最高阈值，再判断较低阈值，否则 >=60 会提前接住 90 分。边界 60 是 Pass，90 是 Excellent；缺失先单独处理，不能和零分混合。这只是标量分类例题，不代表 Series.apply 的所有行为都与 map 等价。

不要只写 lambda 来显得简短。规则包含缺失、多个阈值和异常时，具名函数更容易测试与解释。lambda 适合简单表达式，如 s.map(lambda x: x*2)。

### 例题3：简单跨列算术优先整列计算
```python
orders = pd.DataFrame(
    {"price":[10.0,20.0,None], "qty":[2,3,1]},
    index=["o3","o1","o8"],
)
result = orders.assign(amount=lambda d: d["price"]*d["qty"])
print(result["amount"].tolist()) # 20.0、60.0、缺失
```
assign 返回新表，原 orders 没有 amount 列。lambda 收到的是整个 DataFrame d，不是单个数或单行。此处价格缺失时 amount 也缺失，不能为了得到数字擅自当成0。

```python
result = orders.assign(
    amount=lambda d: d["price"]*d["qty"],
    fee=lambda d: d["amount"]*0.05,
)
```
这种写法中，后续计算可使用前面已经生成的 amount；仍需把列依赖写清楚。若是外部 Series 赋值，Pandas 通常按索引标签对齐：
```python
bonus = pd.Series([7,3], index=["o1","o3"])
result["bonus"] = bonus
# o3 得到3，o1得到7，o8缺失；不是按bonus显示顺序逐行塞入
```
因此新列长度相同也不能保证对应正确。不要随意 reset_index 或 to_numpy 来抹掉标签语义。

### 例题4：逐行 apply 与逐列 apply
```python
def shipping(row):
    if pd.isna(row["price"]) or pd.isna(row["qty"]):
        return float("nan")
    amount = row["price"]*row["qty"]
    return 0.0 if amount >= 50 else 5.0

result = orders.copy()
result["shipping"] = result.apply(shipping, axis=1)
print(result["shipping"].tolist()) # 5.0、0.0、缺失

numeric = pd.DataFrame({"a":[1,2],"b":[10,20]})
print(numeric.apply(lambda col: col.max()-col.min(), axis=0))
# a:1，b:10
```
axis=1 时 row["price"] 是这一行的价格；默认 axis=0 时函数收到整列，不能期待其中同时出现 price/qty 两个字段。默认 raw=False，所以这里传入的是带标签的 Series。

把函数作为“纯计算”使用：读取 row、返回结果，不在 row 上直接改字段或向外部列表追加。不要依赖调用次数、执行顺序或副作用来完成业务。

apply 的返回形状会受函数返回值以及输入影响。本课函数返回单个标量形成新列；空 DataFrame 的 apply 结果不宜靠猜，封装接口时显式处理空表并指定新列 dtype，例如：
```python
if result.empty:
    result["shipping"] = pd.Series(index=result.index, dtype="float64")
else:
    result["shipping"] = result.apply(shipping, axis=1)
```

## 四、易错点：至少掌握这些对照

1. map 字典漏键：结果变缺失，不能误以为原始数据就缺失。先检查源列，再分别定义 Missing/Unknown。
2. 忘记 axis=1：默认按列，row 函数却按行取字段会出错。明确对象与 axis。
3. 把函数名写成函数调用：map(grade) 才是把函数交给映射；map(grade()) 是立即调用。
4. 阈值从低往高判断：>=60 会截住高分。按互斥分支顺序写并测 59/60/89/90。
5. 用 value is None 检查所有缺失：进入 Pandas 后 None 可能表现为 NaN 或 pd.NA；标量规则用 pd.isna(value)。
6. 以为 apply 会修改原表：返回结果需要接收，再赋新列或 assign；函数内也不要修改传入 row。
7. 自定义函数返回不同类型：有的行返回数字，有的行返回列表/Series，会导致结果结构变化。先固定标量返回契约。
8. 用外部 Series 赋值忽略索引：按标签对齐，不是按肉眼显示顺序；错位可能没有报错却数据错误。
9. 空表没有显式输出结构：要求新列时仍要创建零长度且 dtype 正确的列，不能直接返回缺列的输入。
10. 把字符串拼接当缺失处理：str(None) 是文本 "None"，不等于保留缺失，应先判断再格式化。

## 五、何时用：先找最直接的表达

单列类别对照用 map(dict)；单列标量规则用 map(function)，需要 Series.apply 时明确其调用模式；简单整列算术用向量化；跨列复杂分支可用 apply(axis=1)；新增多列且不改输入可用 assign。
业务规则先写成可独立调用的小函数，拿单个边界值测明白，再放进整列操作。真正重要的是缺失、未知、阈值、类型与索引口径，而不是把所有处理都写成 apply。
自定义列的最后检查：行数、顺序、索引是否保持？新列名和 dtype 是否按约定？原输入是否不变？有无错误地填0或把未知合并为缺失？空表和单行能否返回相同结构？

## 三道练习摘要
1. label_courses：用 Series.map 函数区分已知、未知和缺失课程码。
2. add_score_band：从成绩创建等级列，校验分数范围，保持输入不变。
3. add_order_totals：计算实付与运费，练习 axis=1、向量化、缺失和空表结构。
完整接口、样例和硬验收见 homework.md。答案文件开课先占位：「约 9:30 写标准答案」，并不表示已经交付标准答案。

## 下节预告
L11 Pandas 时间与排序·去重。

## 官方参考
- https://pandas.pydata.org/docs/reference/api/pandas.Series.map.html
- https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.apply.html
