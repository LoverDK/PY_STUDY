# L08 作业 · 3 道机试/笔试风题

使用 Python 与 Pandas，禁止文件读写，不修改输入。输入都是普通列表。数值输入仅为有限 int/float（不含 bool）或 None；字符串输入仅 str 或 None，不要求处理 NaN/无穷及其他类型。非法范围检查按题面完成。返回值用 Python 原生 int/float/str/None/list/dict，不把 NaN 放进返回结果。不强制四舍五入，浮点用容差 1e-9 验收。

## 1. 数值摘要
```python
def summarize_scores(values: list) -> dict:
    ...
```
必须使用 Pandas 完成摘要。返回且仅返回以下键：
- total:int，包含 None 的总数；valid:int，非缺失数；missing:int。
- mean、median、std、q25、q75：float 或 None。
std 明确 ddof=1；q25/q75 明确 interpolation="linear"。valid=0 时五个统计量全 None；valid=1 时 std=None，其他统计量为该值。不得把缺失当 0。

样例：
```python
summarize_scores([60,70,80,90,None,None])
# {"total":6,"valid":4,"missing":2,"mean":75.0,"median":75.0,
#  "std":12.909944487358056,"q25":67.5,"q75":82.5}
summarize_scores([])
# total/valid/missing 均 0，五个统计量均 None
summarize_scores([None,5])
# total=2,valid=1,missing=1,mean=median=q25=q75=5.0,std=None
```
硬验收：样例、全缺失、单有效值、常数列、负数及无序值；返回键集合/类型/缺失标记；输入不变。笔试解释为何 ddof=1 单点不能报告 0。

## 2. 带缺失的类别频数报告
```python
def category_profile(labels: list) -> list:
    ...
```
用 Pandas 计数，返回记录列表，每条且仅含：
{"label": str或None, "count": int, "ratio": float}。
非缺失类别按 count 降序，再按原字符串 Python 字典序升序；缺失合并成一条 label=None，始终最后（不论其频数）。ratio=count/len(labels)，分母包含缺失。大小写敏感，空字符串是合法类别，不 trim、不 lower、不删除。空输入返回 []，无缺失时不要添加零计数缺失行。

样例：
```python
category_profile(["B","A","B",None,"A","C"])
# [{"label":"A","count":2,"ratio":2/6},
#  {"label":"B","count":2,"ratio":2/6},
#  {"label":"C","count":1,"ratio":1/6},
#  {"label":None,"count":1,"ratio":1/6}]
category_profile([None,None])
# [{"label":None,"count":2,"ratio":1.0}]
category_profile(["None",None,""])
# label 顺序为 ""、"None"、None，各 count=1，ratio=1/3
```
硬验收：并列次序、缺失频数最大仍放最后、空列表、全缺失、大小写、真实 "None" 文本与缺失区别；计数和=总数，非空时比例和约为1；数据不被改写。笔试比较 dropna=True/False 对分母的影响。

## 3. 及格率双口径报告
```python
def pass_report(scores: list, threshold: float = 60.0) -> dict:
    ...
```
scores 有效成绩须在闭区间 [0,100]，threshold 也在 [0,100]，否则 ValueError；None 是缺失，不及格判断不得把 None 当0。使用 Pandas 完成统计。成绩 >= threshold 为及格。

返回且仅返回：
total:int，valid:int，missing:int，passed:int，
pass_rate_valid:float或None（passed/valid），
pass_rate_all:float或None（passed/total），
passed_mean:float或None（仅及格成绩均值）。
分母=0时相应比率 None；没有及格成绩时 passed_mean=None。空输入 passed=0、计数全0、两个比率与passed_mean均None。pass_rate_all 将缺失保留在分母中，只是报告口径，不意味着认定缺失者实际不及格。

样例：
```python
pass_report([60,59,None,100],60)
# {"total":4,"valid":3,"missing":1,"passed":2,
# "pass_rate_valid":2/3,"pass_rate_all":0.5,"passed_mean":80.0}
pass_report([None,None])
# total=2,valid=0,missing=2,passed=0,
# pass_rate_valid=None,pass_rate_all=0.0,passed_mean=None
pass_report([0,100],0)
# passed=2,两种比率均1.0,passed_mean=50.0
```
硬验收：空、全缺失、无及格、全及格、成绩等于阈值、阈值0/100、非法成绩 -1/101、非法阈值 -1/101；检查键集合与原生类型，输入不变。笔试说明“总体口径及格率”与“把缺失认定为不及格”的区别。

## 提交与自检
三题互相独立，答案文件 homework/answers.ipynb。测试不能只 print，需断言结构、类型、边界和异常；均值等用容差；None 用 is None。不要把“NaN != NaN”误当普通数字比较。
标准答案文件开课先占位：「约 9:30 写标准答案」。
