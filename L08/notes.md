# L08 Pandas 描述统计与 value_counts 深练

阶段：A · DSBA/Python/可视化/复杂度。
仓库路径：L08/。
范围：Series 数值摘要、describe、count/size、mean/median/std/quantile、字符串频数及占比、明确排序与空输入。
不讲：显著性检验、概率分布推导、模型训练；多条件筛选与 loc/iloc 留给 L09；计算机系统原理永不加入。

## 目标
能说清每个统计量回答的问题；区分总行数与有效样本数；手算均值、中位数和小样本分位数；明确标准差 ddof；按题面决定是否把缺失计入频数与占比分母；输出可稳定验收的摘要和频数表。

## 一、是什么：用少量数字描述一列数据

描述统计是在已有样本上做摘要，不自动代表总体规律。数值型列关注位置、离散程度和范围；类别列关注各值出现几次以及占多少。

- size 或 len(s)：总元素数，包含缺失。
- count()：非缺失元素数。
- mean()：有效数值之和除以有效数值数。
- median()：排序后的中间位置；偶数个有效数值取中间两个的平均。
- min()/max()：范围端点。
- std(ddof=1)：按 n-1 为分母的样本标准差；ddof=0 则用 n。
- quantile(q)：分位数；本课显式指定 interpolation="linear"。
- value_counts()：每个唯一值出现的次数，不是唯一值列表，也不是对值求和。

numeric describe 默认提供 count/mean/std/min/25%/50%/75%/max；其中 count 不包含缺失。类别描述通常是 count/unique/top/freq；top 只返回一个最高频值，并列最高频时不能当作题定字典序答案。数值编码也可能代表类别，不能因为某列是数字就认为均值有业务含义。

## 二、为什么：不说明统计口径，正确代码也可能答错问题

同样数据，平均分和及格占比可能回答完全不同的问题。先写清“统计谁、排除什么、除以多少、并列怎么排”，再选函数。

假设六条成绩是 [60,70,80,90,None,None]：总数 6，有效数 4，缺失率 2/6；平均分是 75，不是 300/6=50。缺失不是零分，默认填 0 会改变问题。

均值使用全部数值，容易受极端值影响；中位数用排序位置，相对不容易被少数极端值拉动。[10,10,10,10,100] 的均值 28、中位数 10，因此“典型值”应结合背景解释，不能只报一个均值。标准差大也不等于数据错误；可能确有差异，也可能单位混用，需结合原始数据检查。

频数占比的分母尤其要清楚。["A","A","B",None] 中，非缺失口径 A 为 2/3；包含缺失的总体口径 A 为 2/4。两者都可能合理，但不能混用。

## 三、怎么写：三组例题串讲

### 例题 1：数值摘要与手算核对
```python
import pandas as pd

scores = pd.Series([60,70,80,90,None,None], dtype="float64")
print("rows:", len(scores))          # 6
print("valid:", int(scores.count())) # 4
print(scores.describe())
print("mean:", scores.mean())        # 75.0
print("median:", scores.median())    # 75.0
print("sample std:", scores.std(ddof=1)) # 约 12.909944
print("population std:", scores.std(ddof=0)) # 约 11.180340
print(scores.quantile([0.25,0.5,0.75], interpolation="linear"))
# 25%:67.5，50%:75.0，75%:82.5
```

有效值与均值 75 的偏差平方为 225、25、25、225，和为 500；样本标准差 sqrt(500/3)，总体口径标准差 sqrt(500/4)。不是“哪个函数算错”，而是分母不同。

线性分位数：将有效值从小到大排好，以从 0 开始的位置 h=(n-1)q 找位置。q=0.25 时 h=0.75，位于 60 和 70 之间的 75% 处，所以为 67.5；不是自动挑第一个值，也不是“25% 的数据等于 67.5”。分位数有多种定义，机试应以题定插值方法为准。

DataFrame.describe 默认选取哪些列取决于列类型；要避免混合列歧义，可明确选列：df[["score","minutes"]].describe()。若某个数字列意外读成字符串，应先核查和转换，不能把文本 top 当成数值均值。不要强行在文本列上求 mean。

### 例题 2：频数、占比与缺失口径
```python
labels = pd.Series(["Python","SQL","Python",None,"C","SQL"], dtype="object")
counts = labels.value_counts()
shares_valid = labels.value_counts(normalize=True)
shares_all = labels.value_counts(normalize=True, dropna=False)

print(counts)
print(shares_valid) # Python=2/5，SQL=2/5，C=1/5
print(shares_all)   # Python=2/6，SQL=2/6，C=1/6，缺失=1/6
```

value_counts 默认排除缺失，normalize=True 返回比例而非百分数字符串。要显示百分比才乘 100，但函数验收通常应保留原始浮点比值。sort=False 不是按字母排序；sort_index() 是按类别索引排，sort_values() 通常是按计数排。

并列项顺序不依赖默认行为。若题目要求“频数降序、类别字典序升序”，显式构造表并排序：
```python
table = labels.value_counts().rename_axis("label").reset_index(name="count")
table = table.sort_values(["count","label"], ascending=[False,True])
print(table.reset_index(drop=True))
# Python:2，SQL:2，C:1
```

类别需要统一类型才好比较。本课字符串题输入限 str/None；大小写敏感，"A" 与 "a" 是不同类别，空字符串也是合法类别，不能擅自删除或 strip。

### 例题 3：完整报告先做核对，再写结论
```python
from io import StringIO
csv_text = """student,track,score,minutes
s1,Python,60,10
s2,SQL,70,15
s3,Python,80,20
s4,,90,25
s5,C,,30
s6,SQL,,40
"""
df = pd.read_csv(StringIO(csv_text))
print(df[["score","minutes"]].describe())
print(df["track"].value_counts(dropna=False))
print(df["score"].isna().mean()) # 2/6
```

六条记录，成绩四条有效、两条缺失；track 有一条缺失。不能先 df.dropna() 再假装总体仍是六条，因为那会同时删掉缺成绩或缺 track 的记录，改变两个统计问题的样本。

自检：数值 count+缺失数=总数；排除缺失的频数和=非缺失数；保留缺失的频数和=总数；非空分母下频率和约等于 1。浮点比较用容差，不要盲目 assert sum(ratios)==1。

结论可以写：“有效成绩均值和中位数均为 75，成绩缺失率为 1/3；非缺失 track 中 Python 与 SQL 并列最多。”不能据此声称缺失者成绩差，也不能把并列类别硬说成唯一第一。

## 四、易错点：至少掌握这六个

1. 把 len 当 count：总行数包含缺失，有效样本数不包含。报告同时列出二者，避免隐去缺失。
2. 混淆样本与总体标准差：显式 ddof。只有一个有效值时 ddof=1 的标准差无定义，不应强填 0；ddof=0 的单点标准差才是 0。
3. 用缺失当 0：除非业务定义就是零，否则不应 fillna(0) 再统计。全缺失时均值/中位数应按接口返回缺失标记，不是虚假的 0。
4. 把 normalize 当百分数：0.4 是 40%，不是 0.4%。dropna 改变分母，必须和报告文字一致。
5. 把频数默认并列顺序当稳定契约：需要明确二级排序；用 describe 的 top 无法满足“所有并列项”的题面。
6. 忽略空输入：空数据没有有效均值，空频数没有类别，不应访问 mode()[0]；有效数为 0 时不能除 0。
7. 字符串 "None" 与真正 None 混淆：前者是文本类别，后者是缺失。作业的缺失标签使用 None，不把缺失变成可能与真实文本冲突的占位字符串。
8. 先舍入再计算：会引入误差。计算保留精度，仅展示时格式化；验收用 math.isclose 或 assert_allclose。

## 五、何时用：建立“样本—类型—口径—校验”顺序

初看数值列，用 describe 获取范围与离散程度，再按业务选择均值或中位数。对类别列，用 value_counts 看分布与稀有类别，再核查缺失和并列。做质量检查时一起看 size/count/缺失率；只看均值无法发现“绝大多数记录缺失”。

昨天直方图看分布形态，今天统计表给精确摘要，两者互相补充，不能互相替代；相同均值可以对应不同分布。高频类别也不是“更好”的类别，仍要看业务定义。

要交付可验收结果，先固定输入范围和返回结构，再写边界行为。空表、全缺失、单点、并列、多种分母，往往比复杂语法更容易扣分。明天 L09 再系统学习多条件筛选与 loc/iloc，不在本课提前扩展。

## 三道练习摘要
1. summarize_scores：返回总数、有效数、缺失数、均值、中位数、样本标准差和四分位点。
2. category_profile：频数降序、字典序升序输出；缺失最后；分母包含全部记录。
3. pass_report：成绩阈值与及格报告，分别报告有效样本及总体口径，明确边界。

详见 homework.md。homework/answers.ipynb 按开课约定先占位，写明「约 9:30 写标准答案」；占位不等于标准答案已交付。

## 下节预告
L09 Pandas 多条件过滤与 loc/iloc 精熟。

## 官方参考
https://pandas.pydata.org/docs/reference/api/pandas.Series.describe.html
https://pandas.pydata.org/docs/reference/api/pandas.Series.std.html
https://pandas.pydata.org/docs/reference/api/pandas.Series.value_counts.html
