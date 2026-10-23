# L10 作业 · map / apply / 自定义列

使用 Python 与 Pandas，全程禁止文件读写。三题独立；返回新对象，不修改输入、索引或行顺序。输入索引唯一。题面未提及的类型/NaN/无穷处理不强制；缺失输入仅为 None 或 Pandas 缺失标记。数值均有限且不含 bool。列名固定且不存在输出列同名冲突。必须用断言验收，不接受只打印。

## 1. 课程码映射
```python
def label_courses(codes: pd.Series) -> pd.Series:
    ...
```
codes 为 object dtype，每个非缺失元素为 str。使用 Series.map(函数)：
"PY"→"Python"，"SQL"→"SQL"，"C"→"C"；其他非缺失字符串→"Unknown"；缺失→"Missing"。大小写敏感，不 strip、不 upper。返回 Series，name="course_name"，dtype="object"，保留原索引；空输入也遵守结构。

样例：
```python
codes = pd.Series(["PY","SQL","X",None,"py",""], index=[9,3,7,2,8,4], dtype="object")
# 输出 ["Python","SQL","Unknown","Missing","Unknown","Unknown"]
```
硬验收：已知/未知/缺失、真实文本 "None"、空字符串、大小写、单行/空 Series；索引顺序/name/dtype；输出与输入不是同一对象，输入不变。需静态检查核心转换使用 map，不能只用循环代替。

## 2. 成绩等级自定义列
```python
def add_score_band(df: pd.DataFrame) -> pd.DataFrame:
    ...
```
df 列顺序为 ["student","score"]；score 为 float64，可缺失。若任一非缺失 score 不在 [0,100]，先抛 ValueError，不得修改输入。返回原两列加 band，band 为 object dtype：
缺失→"Missing"，>=90→"Excellent"，>=60→"Pass"，其余→"Fail"。使用标量函数经 Series.map 或 Series.apply 生成 band。保留原索引和行序，空表也须有 band 列。

样例分数 [59,60,89,90,None]→["Fail","Pass","Pass","Excellent","Missing"]。
硬验收：0/59/60/89/90/100、缺失、全缺失、空表、单行；-1/101 抛 ValueError；新对象、原列值与 dtype、band dtype、固定列顺序和输入不变。

## 3. 订单实付与运费
```python
def add_order_totals(df: pd.DataFrame) -> pd.DataFrame:
    ...
```
df 列顺序 ["order_id","price","qty","discount"]。price/qty/discount 为 float64，每项有限数或缺失。qty 不要求整数。非缺失项必须 >=0，否则 ValueError；即使同一行另有缺失，也必须检查已有负值。
输出原列后追加 net、shipping，二者都 float64。
- 任一计算输入缺失：net 和 shipping 均缺失（pd.isna为True）；不按0补齐。
- 完整行 net=max(price*qty-discount,0.0)，discount 可以大于原金额。
- net>=100 运费0.0，否则8.0；边界100免运。
- net 可用向量化或 apply；shipping 必须用 DataFrame.apply(axis=1) 调用标量函数。空表显式创建两列以保证结构。
- 不修改输入；列顺序、索引、行序保持。

样例：
```python
# (price,qty,discount) → (net,shipping)
# (50,2,0) → (100,0)
# (50,2,1) → (99,8)
# (10,1,20) → (0,8)
# (None,2,0) → (缺失,缺失)
# (None,-1,0) → ValueError
```
硬验收：上述样例、零值、折扣超额、缺失各一列、全缺失、空表、单行、非默认乱序索引；任一负输入均抛错。通过 assert_frame_equal 检查原表不变，assert_series_equal/check_dtype 检查新增列；数值用容差1e-9，不用直接比较 NaN。需检查 axis=1 核心运费规则。

## 笔试追问
每题解释是什么/为什么/何时用；另答：普通字典map漏键如何表现？axis=0/1分别传入什么？赋外部Series时为什么长度相等仍可能错位？为何 apply 不是自动加速器？
答案路径 homework/answers.ipynb，开课先放占位「约 9:30 写标准答案」。
